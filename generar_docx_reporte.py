"""Genera el reporte U5 completo con la identidad visual de ACT-F04."""

import os
import re
import tempfile
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

BASE_DIR = Path(__file__).resolve().parent
EVIDENCE_DIR = BASE_DIR / "evidencias"
TEMPLATE_PATH = EVIDENCE_DIR / "ACT-F04-EQUIPO8_PLANTILLA.docx"
CONTENT_PATH = EVIDENCE_DIR / "EVIDENCIAS_GUIA_PLANTILLA.md"
CAPTURAS_DIR = EVIDENCE_DIR / "capturas"
DOCX_OUT = EVIDENCE_DIR / "Reporte_Evidencias_U5.docx"
LOCKED_OUTPUT = EVIDENCE_DIR / "Reporte_Evidencias_U5_Formato_ACT-F04.docx"
NAVY = "0F2C56"
BLUE = "4F81BC"
PALE = "F2F6FB"
BORDER = "B7C9DD"
BODY_COLOR = RGBColor(0x22, 0x22, 0x22)
IMAGE_PATTERN = re.compile(r"!\[(.*?)\]\((.*?)\)")
INLINE_PATTERN = re.compile(r"(\*\*.+?\*\*|`.+?`|\*.+?\*)")
TABLE_SEPARATOR = re.compile(r"\|?[\s:|-]+\|?")
EXPECTED_IMAGE_COUNT = 12


def element_text(element):
    return "".join(element.xpath(".//w:t/text()"))


def set_cell_shading(cell, fill):
    properties = cell._tc.get_or_add_tcPr()
    shading = properties.find(qn("w:shd"))
    if shading is None:
        shading = OxmlElement("w:shd")
        properties.append(shading)
    shading.set(qn("w:val"), "clear")
    shading.set(qn("w:color"), "auto")
    shading.set(qn("w:fill"), fill)


def set_cell_borders(cell, color=BORDER, size="6"):
    properties = cell._tc.get_or_add_tcPr()
    borders = properties.first_child_found_in("w:tcBorders")
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        properties.append(borders)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        border = borders.find(qn(f"w:{edge}"))
        if border is None:
            border = OxmlElement(f"w:{edge}")
            borders.append(border)
        border.set(qn("w:val"), "single")
        border.set(qn("w:sz"), size)
        border.set(qn("w:color"), color)


def set_cell_margins(cell, top=70, start=80, bottom=70, end=80):
    properties = cell._tc.get_or_add_tcPr()
    margins = properties.first_child_found_in("w:tcMar")
    if margins is None:
        margins = OxmlElement("w:tcMar")
        properties.append(margins)
    for edge, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        element = margins.find(qn(f"w:{edge}"))
        if element is None:
            element = OxmlElement(f"w:{edge}")
            margins.append(element)
        element.set(qn("w:w"), str(value))
        element.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    properties = row._tr.get_or_add_trPr()
    header = OxmlElement("w:tblHeader")
    header.set(qn("w:val"), "true")
    properties.append(header)


def add_inline(paragraph, text, base_size=11, color=BODY_COLOR):
    text = text.replace(r"\|", "|")
    position = 0
    for match in INLINE_PATTERN.finditer(text):
        if match.start() > position:
            _add_text_run(paragraph, text[position : match.start()], base_size, color)

        token = match.group()
        if token.startswith("**"):
            run = _add_text_run(paragraph, token[2:-2], base_size, color)
            run.bold = True
        elif token.startswith("`"):
            run = _add_text_run(paragraph, token[1:-1], base_size - 1, color)
            run.font.name = "Consolas"
        else:
            run = _add_text_run(paragraph, token[1:-1], base_size, color)
            run.italic = True
        position = match.end()

    if position < len(text):
        _add_text_run(paragraph, text[position:], base_size, color)


def _add_text_run(paragraph, text, size, color):
    run = paragraph.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(size)
    run.font.color.rgb = color
    return run


def replace_paragraph(paragraph, label, value):
    paragraph.clear()
    label_run = paragraph.add_run(label)
    label_run.bold = True
    label_run.font.name = "Arial"
    value_run = paragraph.add_run(f" {value}")
    value_run.font.name = "Arial"


def replace_cell_paragraphs(cell, lines):
    paragraphs = cell.paragraphs
    if not paragraphs:
        raise ValueError("La celda de identificación no tiene párrafos editables.")
    template = paragraphs[0]._p
    for paragraph in paragraphs[1:]:
        paragraph._p.getparent().remove(paragraph._p)
    paragraph = paragraphs[0]
    paragraph.clear()
    for index, text in enumerate(lines):
        if index:
            paragraph.add_run().add_break()
        run = paragraph.add_run(text)
        run.font.name = "Arial"
        if index == 0:
            run.bold = True
    if template is None:
        raise ValueError("No se pudo conservar el formato de la celda.")


def update_metadata(document):
    if not document.tables:
        raise ValueError("La plantilla ACT no contiene la tabla institucional de identificación.")
    table = document.tables[0]
    replace_paragraph(table.cell(1, 0).paragraphs[0], "Nombre del curso:", "Componentes en Lógica de Negocios")
    replace_paragraph(table.cell(1, 1).paragraphs[0], "Nombre del profesor:", "Dr. Miguel Ángel Gómez Marroquín")
    replace_paragraph(table.cell(2, 0).paragraphs[0], "Unidad:", "5")

    activity_cell = table.cell(2, 1)
    replace_paragraph(activity_cell.paragraphs[0], "Actividad:", "Reporte de Evidencias U5")
    hyperlink = activity_cell.paragraphs[2]._p.find(qn("w:hyperlink"))
    if hyperlink is None:
        raise ValueError("La celda de repositorio perdió el vínculo de la plantilla.")
    target = "https://github.com/"
    text_nodes = hyperlink.xpath(".//w:t")
    if not text_nodes:
        raise ValueError("El vínculo del repositorio no contiene texto editable.")
    text_nodes[0].text = "PENDIENTE: URL REAL DEL REPOSITORIO DEL EQUIPO"
    for text_node in text_nodes[1:]:
        text_node.text = ""
    relationship_id = hyperlink.get(qn("r:id"))
    if relationship_id not in document.part.rels:
        raise ValueError("No se encontró la relación del vínculo de repositorio.")
    document.part.rels[relationship_id]._target = target

    replace_paragraph(table.cell(3, 0).paragraphs[0], "Fecha:", "01/11/2026")
    bibliography = table.cell(4, 0)
    citations = [
        "Bibliografía (Formato APA)",
        "pytest-dev. (s. f.). Get started — pytest documentation. https://docs.pytest.org/en/stable/getting-started.html",
        "SQLAlchemy. (s. f.). Working with transactions and the DBAPI. https://docs.sqlalchemy.org/en/20/orm/session_transaction.html",
        "Python Software Foundation. (s. f.). unittest.mock — mock object library. https://docs.python.org/3/library/unittest.mock.html",
        "Gómez Marroquín, M. A. (2026). CLN_U5 Manual de Calidad y Pruebas Automatizadas [Material de clase]. FIME, UANL.",
    ]
    replace_cell_paragraphs(bibliography, citations)


def remove_template_body(document):
    body = document._element.body
    metadata_table = document.tables[0]._tbl
    first_section = None
    for paragraph in body.findall(qn("w:p")):
        section_properties = paragraph.find(f"{qn('w:pPr')}/{qn('w:sectPr')}")
        if section_properties is not None:
            first_section = deepcopy(section_properties)
            break
    if first_section is None:
        raise ValueError("No se encontró la configuración original de página y encabezado ACT-F04.")

    final_section = body.sectPr
    for child in list(body):
        if child is metadata_table or child is final_section:
            continue
        body.remove(child)
    body.remove(final_section)
    body.append(first_section)


def add_document_heading(document, text, level):
    paragraph = document.add_paragraph()
    paragraph.paragraph_format.keep_with_next = True
    if level == 1:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.space_before = Pt(12)
        paragraph.paragraph_format.space_after = Pt(3)
        run = paragraph.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x0F, 0x2C, 0x56)
    elif level == 2:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.space_after = Pt(8)
        run = paragraph.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(0x70, 0x70, 0x70)
    elif level == 3:
        paragraph.style = document.styles["Heading 1"]
        run = paragraph.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x0F, 0x2C, 0x56)
        paragraph.paragraph_format.keep_with_next = True
    else:
        paragraph.style = document.styles["List Paragraph"]
        paragraph.paragraph_format.left_indent = Inches(0.25)
        paragraph.paragraph_format.space_before = Pt(5)
        paragraph.paragraph_format.space_after = Pt(2)
        add_inline(paragraph, text, base_size=11, color=RGBColor(0x4F, 0x81, 0xBC))
        for run in paragraph.runs:
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x4F, 0x81, 0xBC)


def add_body_paragraph(document, text):
    paragraph = document.add_paragraph(style="Normal")
    paragraph.paragraph_format.left_indent = Inches(0.25)
    paragraph.paragraph_format.space_before = Pt(2)
    paragraph.paragraph_format.space_after = Pt(5)
    paragraph.paragraph_format.line_spacing = 1.0
    add_inline(paragraph, text)
    return paragraph


def add_quote(document, text):
    paragraph = add_body_paragraph(document, text)
    paragraph.paragraph_format.left_indent = Inches(0.4)
    paragraph.paragraph_format.right_indent = Inches(0.2)
    for run in paragraph.runs:
        run.italic = True
        run.font.color.rgb = RGBColor(0x4F, 0x68, 0x83)


def add_list_item(document, text, ordered_number=None):
    paragraph = document.add_paragraph(style="List Paragraph")
    paragraph.paragraph_format.left_indent = Inches(0.5)
    paragraph.paragraph_format.first_line_indent = Inches(-0.2)
    paragraph.paragraph_format.space_after = Pt(3)
    marker = f"{ordered_number}. " if ordered_number is not None else "• "
    paragraph.add_run(marker)
    text = re.sub(r"^\[x\]\s*", "☑ ", text, flags=re.IGNORECASE)
    text = re.sub(r"^\[ \]\s*", "☐ ", text)
    add_inline(paragraph, text)


def add_code_block(document, code_lines):
    table = document.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.cell(0, 0)
    cell.width = Inches(6.9)
    set_cell_shading(cell, NAVY)
    set_cell_borders(cell, NAVY, "0")
    set_cell_margins(cell, top=110, start=140, bottom=110, end=140)
    paragraph = cell.paragraphs[0]
    paragraph.clear()
    paragraph.paragraph_format.space_after = Pt(0)
    paragraph.paragraph_format.line_spacing = 1.0
    run = paragraph.add_run("\n".join(code_lines).rstrip())
    run.font.name = "Consolas"
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(0xF2, 0xF6, 0xFB)
    document.add_paragraph().paragraph_format.space_after = Pt(1)


def add_markdown_table(document, rows):
    if not rows or not rows[0]:
        return
    column_count = len(rows[0])
    if any(len(row) != column_count for row in rows):
        raise ValueError("La plantilla Markdown contiene una tabla con diferente cantidad de columnas por fila.")

    table = document.add_table(rows=len(rows), cols=column_count)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    available_width = 7.0
    if column_count == 6:
        proportions = [0.62, 1.12, 1.15, 1.18, 1.68, 1.25]
    elif column_count == 5:
        proportions = [1.35, 1.25, 1.55, 1.55, 1.0]
    else:
        proportions = [available_width / column_count] * column_count
    total = sum(proportions)

    for row_index, values in enumerate(rows):
        row = table.rows[row_index]
        for column_index, value in enumerate(values):
            cell = row.cells[column_index]
            cell.width = Inches(available_width * proportions[column_index] / total)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            set_cell_borders(cell)
            set_cell_margins(cell)
            if row_index == 0:
                set_cell_shading(cell, NAVY)
            elif row_index % 2 == 0:
                set_cell_shading(cell, PALE)
            paragraph = cell.paragraphs[0]
            paragraph.clear()
            paragraph.paragraph_format.space_after = Pt(1)
            paragraph.paragraph_format.line_spacing = 1.0
            size = 7.2 if column_count >= 6 else 8
            add_inline(
                paragraph,
                value,
                base_size=size,
                color=RGBColor(0xFF, 0xFF, 0xFF) if row_index == 0 else BODY_COLOR,
            )
            if row_index == 0:
                for run in paragraph.runs:
                    run.bold = True
        if row_index == 0:
            set_repeat_table_header(row)
    document.add_paragraph().paragraph_format.space_after = Pt(1)


def add_image(document, line):
    match = IMAGE_PATTERN.fullmatch(line.strip())
    if match is None:
        raise ValueError(f"No se pudo interpretar la imagen Markdown: {line}")
    image_path = (CONTENT_PATH.parent / match.group(2)).resolve()
    if not image_path.is_relative_to(CAPTURAS_DIR.resolve()):
        raise ValueError(f"La imagen debe pertenecer a la carpeta de capturas: {image_path}")
    if not image_path.is_file():
        raise FileNotFoundError(f"No se encontró la captura requerida: {image_path}")

    paragraph = document.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.space_before = Pt(3)
    paragraph.paragraph_format.space_after = Pt(4)
    paragraph.add_run().add_picture(str(image_path), width=Inches(6.2))
    caption = document.add_paragraph(style="Caption")
    caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
    caption.paragraph_format.space_after = Pt(5)
    run = caption.add_run(match.group(1))
    run.font.name = "Arial"
    run.font.size = Pt(9)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0x4F, 0x68, 0x83)


def is_table_start(lines, index):
    return (
        index + 1 < len(lines)
        and lines[index].strip().startswith("|")
        and TABLE_SEPARATOR.fullmatch(lines[index + 1].strip()) is not None
        and "-" in lines[index + 1]
    )


def parse_table_row(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_block_start(lines, index):
    line = lines[index].strip()
    return (
        line.startswith(("#", "```", ">", "!["))
        or re.match(r"[-*]\s+", line) is not None
        or re.match(r"\d+\.\s+", line) is not None
        or re.fullmatch(r"(?:-{3,}|\*{3,})", line) is not None
        or is_table_start(lines, index)
    )


def render_content(document):
    lines = CONTENT_PATH.read_text(encoding="utf-8").splitlines()
    index = 0
    images_added = 0
    tables_added = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line or re.fullmatch(r"(?:-{3,}|\*{3,})", line):
            index += 1
            continue

        if line.startswith("```"):
            code_lines = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            if index == len(lines):
                raise ValueError("Se encontró un bloque de código Markdown sin cierre.")
            add_code_block(document, code_lines)
            index += 1
            continue

        if is_table_start(lines, index):
            rows = [parse_table_row(lines[index])]
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(parse_table_row(lines[index]))
                index += 1
            add_markdown_table(document, rows)
            tables_added += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            add_document_heading(document, heading.group(2), len(heading.group(1)))
            index += 1
            continue

        if line.startswith("!["):
            add_image(document, line)
            images_added += 1
            index += 1
            continue

        if line.startswith(">"):
            add_quote(document, line[1:].strip())
            index += 1
            continue

        unordered = re.match(r"^[-*]\s+(.*)$", line)
        ordered = re.match(r"^(\d+)\.\s+(.*)$", line)
        if unordered or ordered:
            add_list_item(
                document,
                unordered.group(1) if unordered else ordered.group(2),
                None if unordered else ordered.group(1),
            )
            index += 1
            continue

        paragraph_lines = [line]
        index += 1
        while index < len(lines) and lines[index].strip() and not is_block_start(lines, index):
            paragraph_lines.append(lines[index].strip())
            index += 1
        add_body_paragraph(document, " ".join(paragraph_lines))

    if images_added != EXPECTED_IMAGE_COUNT:
        raise ValueError(
            f"Se esperaban {EXPECTED_IMAGE_COUNT} imágenes de evidencias E1-E9 "
            f"y se encontraron {images_added}."
        )
    if tables_added != 3:
        raise ValueError(f"Se esperaban 3 tablas de evidencias y se encontraron {tables_added}.")
    return images_added, tables_added


def build_report():
    if not TEMPLATE_PATH.is_file():
        raise FileNotFoundError(f"No se encontró la plantilla Word ACT-F04: {TEMPLATE_PATH}")
    if not CONTENT_PATH.is_file():
        raise FileNotFoundError(f"No se encontró el contenido original de evidencias: {CONTENT_PATH}")

    document = Document(TEMPLATE_PATH)
    update_metadata(document)
    remove_template_body(document)
    images_added, tables_added = render_content(document)
    document.core_properties.title = "Documento de Evidencias - Unidad 5"
    document.core_properties.subject = "Integración, Pruebas y Calidad - Laboratorio U5"
    return document, images_added, tables_added


def save_report(document):
    output_path = DOCX_OUT
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=output_path.parent, suffix=".docx.tmp", delete=False) as temporary:
            temporary_path = Path(temporary.name)
        try:
            document.save(temporary_path)
            os.replace(temporary_path, output_path)
        except PermissionError:
            temporary_path.unlink(missing_ok=True)
            output_path = LOCKED_OUTPUT
            document.save(output_path)
            print(f"[AVISO] El reporte principal está abierto o bloqueado; se guardó una copia en {output_path}.")
    finally:
        if "temporary_path" in locals() and temporary_path.exists():
            temporary_path.unlink()
    return output_path


def create_report():
    document, images_added, tables_added = build_report()
    output_path = save_report(document)
    print(f"[OK] Reporte completo de evidencias U5 generado: {output_path}")
    print(f"Secciones incluidas: E1-E9; tablas: {tables_added}; capturas: {images_added}.")
    print("Se conservaron el encabezado, pie de página, logotipos, márgenes y estilos de ACT-F04.")
    print(f"Tamaño: {output_path.stat().st_size} bytes")


if __name__ == "__main__":
    create_report()
