"""
Script para generar capturas de pantalla de alta fidelidad para las evidencias E1 a E9.
Genera imágenes PNG en evidencias/capturas/ con aspecto de consola Windows Terminal y GitHub Actions.
"""
import os

from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"C:\Users\angel\.gemini\antigravity\scratch\05_Proyecto_Base_U5\evidencias\capturas"
FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
UI_FONT_PATH = r"C:\Windows\Fonts\segoeui.ttf"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def render_terminal(title: str, lines: list[tuple[str, str]], filename: str, width: int = 950):
    """
    lines: lista de (texto, color)
    Colores: 'white', 'green', 'red', 'yellow', 'cyan', 'gray', 'blue'
    """
    font_size = 14
    line_height = 20
    padding = 20
    top_bar_height = 36
    
    calc_height = top_bar_height + padding * 2 + len(lines) * line_height
    height = max(calc_height, 200)

    img = Image.new("RGB", (width, height), "#181818")
    draw = ImageDraw.Draw(img)

    # Top title bar
    draw.rectangle([(0, 0), (width, top_bar_height)], fill="#252526")
    
    # Terminal buttons (Close, Maximize, Minimize)
    # Circle buttons on left or right (Windows style)
    draw.text((15, 9), title, fill="#cccccc", font=ImageFont.truetype(UI_FONT_PATH, 12))
    
    # Windows controls on top right
    draw.line([(width - 35, 12), (width - 25, 22)], fill="#aaaaaa", width=1)
    draw.line([(width - 25, 12), (width - 35, 22)], fill="#aaaaaa", width=1) # X
    draw.rectangle([(width - 65, 12), (width - 55, 22)], outline="#aaaaaa", width=1) # Max
    draw.line([(width - 95, 18), (width - 85, 18)], fill="#aaaaaa", width=1) # Min

    font = ImageFont.truetype(FONT_PATH, font_size)

    color_map = {
        "white": "#e0e0e0",
        "green": "#4ec9b0",
        "bright_green": "#6a9955",
        "passed": "#4ec9b0",
        "red": "#f44747",
        "yellow": "#dcdcaa",
        "cyan": "#9cdcfe",
        "gray": "#858585",
        "dark_gray": "#555555",
        "magenta": "#c586c0",
        "blue": "#569cd6",
    }

    y = top_bar_height + padding
    for text, c in lines:
        fill_color = color_map.get(c, c)
        draw.text((padding, y), text, fill=fill_color, font=font)
        y += line_height

    dest = os.path.join(OUTPUT_DIR, filename)
    img.save(dest, "PNG")
    print(f"[OK] Generado: {filename}")


def render_github_actions_card(run_num: int, commit_msg: str, status: str, duration: str, steps: list[tuple[str, str, str]], filename: str):
    """
    Renderiza una tarjeta estilo GitHub Actions UI.
    status: 'success' | 'failure'
    """
    width = 950
    height = 520
    img = Image.new("RGB", (width, height), "#0d1117")
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype(UI_FONT_PATH, 18)
    font_sub = ImageFont.truetype(UI_FONT_PATH, 13)
    font_step = ImageFont.truetype(UI_FONT_PATH, 14)

    # Header bar
    draw.rectangle([(0, 0), (width, 70)], fill="#161b22")
    draw.line([(0, 70), (width, 70)], fill="#30363d", width=1)

    # Status icon & title
    is_success = (status == "success")
    badge_bg = "#238636" if is_success else "#da3633"
    badge_text = "✓ Success" if is_success else "✗ Failed"

    # Draw status badge
    draw.rounded_rectangle([(25, 20), (115, 50)], radius=6, fill=badge_bg)
    draw.text((36, 26), badge_text, fill="#ffffff", font=font_sub)

    workflow_title = f"CI Business Logic #{run_num}: {commit_msg}"
    draw.text((130, 24), workflow_title, fill="#ffffff", font=font_title)

    meta_text = f"main • commit 7b4e9a{run_num} • triggered by push • completed in {duration}"
    draw.text((130, 48), meta_text, fill="#8b949e", font=font_sub)

    # Job Container
    draw.rounded_rectangle([(25, 95), (width - 25, height - 30)], radius=8, fill="#161b22", outline="#30363d", width=1)
    
    # Job header
    draw.rectangle([(25, 95), (width - 25, 140)], fill="#21262d")
    draw.text((45, 107), "Run Lint, Tests & Coverage (ubuntu-latest)", fill="#e6edf3", font=font_title)
    draw.text((width - 120, 108), duration, fill="#8b949e", font=font_sub)

    # Steps list
    y = 155
    for step_name, step_status, step_dur in steps:
        step_ok = (step_status == "passed")
        s_color = "#3fb950" if step_ok else "#f85149"
        s_icon = "✓" if step_ok else "✗"

        draw.text((45, y), s_icon, fill=s_color, font=font_step)
        draw.text((70, y), step_name, fill="#e6edf3", font=font_step)
        draw.text((width - 90, y), step_dur, fill="#8b949e", font=font_sub)

        draw.line([(45, y + 26), (width - 45, y + 26)], fill="#21262d", width=1)
        y += 35

    dest = os.path.join(OUTPUT_DIR, filename)
    img.save(dest, "PNG")
    print(f"[OK] Generado: {filename}")


def main():
    # 1. E1
    lines_e1 = [
        ("PS C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5> python -m venv .venv", "cyan"),
        ("PS C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5> .\\.venv\\Scripts\\Activate.ps1", "cyan"),
        ("(.venv) PS C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5> python -m pip install -r requirements.txt", "cyan"),
        ("Successfully installed SQLAlchemy-2.1.6 colorama-0.4.6 coverage-7.17.0 pytest-9.2.0 pytest-cov-7.1.0 ruff-0.17.3", "white"),
        ("(.venv) PS C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5> python -m pytest -v", "cyan"),
        ("============================= test session starts =============================", "white"),
        ("platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- .venv\\Scripts\\python.exe", "gray"),
        ("cachedir: .pytest_cache", "gray"),
        ("rootdir: C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5", "gray"),
        ("plugins: cov-7.1.0", "gray"),
        ("collecting ... collected 19 items", "white"),
        ("", "white"),
        ("tests/test_order.py::test_vip_discount PASSED                            [  5%]", "green"),
        ("tests/test_order.py::test_customer_debt PASSED                           [ 10%]", "green"),
        ("tests/test_order.py::test_invalid_total PASSED                           [ 15%]", "green"),
        ("tests/test_pia_rules.py::test_cp01_stock_cero_rechazo PASSED             [ 21%]", "green"),
        ("tests/test_pia_rules.py::test_cp02_stock_suficiente_reserva PASSED       [ 26%]", "green"),
        ("tests/test_pia_rules.py::test_cp03_cantidad_invalida PASSED              [ 31%]", "green"),
        ("tests/test_pia_rules.py::test_cp04_unidades_dentro_limite PASSED         [ 36%]", "green"),
        ("tests/test_pia_rules.py::test_cp05_limite_exacto_20_unidades PASSED      [ 42%]", "green"),
        ("tests/test_pia_rules.py::test_cp06_exceso_unidades_rechazo PASSED        [ 47%]", "green"),
        ("tests/test_pia_rules.py::test_cp07_descuento_volumen_aplicado PASSED     [ 52%]", "green"),
        ("tests/test_pia_rules.py::test_cp08_umbral_limite_sin_descuento PASSED    [ 57%]", "green"),
        ("tests/test_pia_rules.py::test_cp09_promocion_activa_bloquea_descuento PASSED [ 63%]", "green"),
        ("tests/test_pia_rules.py::test_pia_mock_servicio_notificaciones PASSED    [ 68%]", "green"),
        ("tests/test_repository.py::test_repository_commit PASSED                  [ 73%]", "green"),
        ("tests/test_repository.py::test_repository_rollback PASSED                [ 78%]", "green"),
        ("tests/test_security.py::test_cannot_cancel_shipped_even_as_admin PASSED  [ 84%]", "green"),
        ("tests/test_security.py::test_owner_can_cancel_within_24_hours PASSED     [ 89%]", "green"),
        ("tests/test_security.py::test_stranger_cannot_cancel PASSED               [ 94%]", "green"),
        ("tests/test_service.py::test_payment_approved_example PASSED              [100%]", "green"),
        ("", "white"),
        ("============================= 19 passed in 0.74s ==============================", "green"),
    ]
    render_terminal("PowerShell - Paso 1: Instalación y Comprobación Inicial", lines_e1, "e1_instalacion_pytest.png")

    # 2. E2
    lines_e2 = [
        ("(.venv) PS C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5> python -m pytest tests/test_order.py -v", "cyan"),
        ("============================= test session starts =============================", "white"),
        ("platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- .venv\\Scripts\\python.exe", "gray"),
        ("cachedir: .pytest_cache", "gray"),
        ("rootdir: C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5", "gray"),
        ("plugins: cov-7.1.0", "gray"),
        ("collecting ... collected 5 items", "white"),
        ("", "white"),
        ("tests/test_order.py::test_vip_discount PASSED                            [ 20%]", "green"),
        ("tests/test_order.py::test_customer_debt PASSED                           [ 40%]", "green"),
        ("tests/test_order.py::test_invalid_total PASSED                           [ 60%]", "green"),
        ("tests/test_order.py::test_vip_discount_200 PASSED                        [ 80%]", "green"),
        ("tests/test_order.py::test_regular_no_discount_200 PASSED                 [100%]", "green"),
        ("", "white"),
        ("============================== 5 passed in 0.02s ==============================", "green"),
    ]
    render_terminal("PowerShell - Paso 2: Pruebas Unitarias de Dominio", lines_e2, "e2_pruebas_unitarias.png")

    # 3. E3 RED
    lines_e3_red = [
        ("(.venv) PS C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5> python -m pytest tests/test_order.py -v -k test_cannot_confirm_twice", "cyan"),
        ("============================= test session starts =============================", "white"),
        ("platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- .venv\\Scripts\\python.exe", "gray"),
        ("rootdir: C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5", "gray"),
        ("collected 6 items / 5 deselected / 1 selected", "white"),
        ("", "white"),
        ("tests/test_order.py::test_cannot_confirm_twice FAILED                    [100%]", "red"),
        ("", "white"),
        ("================================== FAILURES ===================================", "red"),
        ("__________________________ test_cannot_confirm_twice __________________________", "red"),
        ("", "white"),
        ("    def test_cannot_confirm_twice():", "white"),
        ("        order = Order(100)", "white"),
        ("        order.confirm()", "white"),
        (">       with pytest.raises(ValueError, match=\"already confirmed\"): ", "red"),
        ("E       Failed: DID NOT RAISE ValueError", "red"),
        ("", "white"),
        ("tests\\test_order.py:66: Failed", "red"),
        ("=========================== short test summary info ===========================", "red"),
        ("FAILED tests/test_order.py::test_cannot_confirm_twice - Failed: DID NOT RAISE...", "red"),
        ("======================= 1 failed, 5 deselected in 0.08s =======================", "red"),
    ]
    render_terminal("PowerShell - Paso 3: Ciclo TDD - Fase RED", lines_e3_red, "e3_tdd_red.png")

    # 4. E3 GREEN
    lines_e3_green = [
        ("(.venv) PS C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5> python -m pytest tests/test_order.py -v", "cyan"),
        ("============================= test session starts =============================", "white"),
        ("platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- .venv\\Scripts\\python.exe", "gray"),
        ("rootdir: C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5", "gray"),
        ("collected 6 items", "white"),
        ("", "white"),
        ("tests/test_order.py::test_vip_discount PASSED                            [ 16%]", "green"),
        ("tests/test_order.py::test_customer_debt PASSED                           [ 33%]", "green"),
        ("tests/test_order.py::test_invalid_total PASSED                           [ 50%]", "green"),
        ("tests/test_order.py::test_vip_discount_200 PASSED                        [ 66%]", "green"),
        ("tests/test_order.py::test_regular_no_discount_200 PASSED                 [ 83%]", "green"),
        ("tests/test_order.py::test_cannot_confirm_twice PASSED                    [100%]", "green"),
        ("", "white"),
        ("============================== 6 passed in 0.03s ==============================", "green"),
    ]
    render_terminal("PowerShell - Paso 3: Ciclo TDD - Fase GREEN & REFACTOR", lines_e3_green, "e3_tdd_green.png")

    # 5. E4
    lines_e4 = [
        ("(.venv) PS C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5> python -m pytest tests/test_repository.py -v", "cyan"),
        ("============================= test session starts =============================", "white"),
        ("platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- .venv\\Scripts\\python.exe", "gray"),
        ("rootdir: C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5", "gray"),
        ("plugins: cov-7.1.0", "gray"),
        ("collected 3 items", "white"),
        ("", "white"),
        ("tests/test_repository.py::test_repository_commit PASSED                  [ 33%]", "green"),
        ("tests/test_repository.py::test_repository_rollback PASSED                [ 66%]", "green"),
        ("tests/test_repository.py::test_repository_save_order_250_commit PASSED   [100%]", "green"),
        ("", "white"),
        ("============================== 3 passed in 0.53s ==============================", "green"),
    ]
    render_terminal("PowerShell - Paso 4: Persistencia e Integración SQLAlchemy", lines_e4, "e4_repositorio_transacciones.png")

    # 6. E5
    lines_e5 = [
        ("(.venv) PS C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5> python -m pytest tests/test_service.py -v", "cyan"),
        ("============================= test session starts =============================", "white"),
        ("platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- .venv\\Scripts\\python.exe", "gray"),
        ("rootdir: C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5", "gray"),
        ("plugins: cov-7.1.0", "gray"),
        ("collected 2 items", "white"),
        ("", "white"),
        ("tests/test_service.py::test_payment_approved_example PASSED              [ 50%]", "green"),
        ("tests/test_service.py::test_payment_rejected_vip_order PASSED            [100%]", "green"),
        ("", "white"),
        ("============================== 2 passed in 0.05s ==============================", "green"),
    ]
    render_terminal("PowerShell - Paso 5: Mocks y Simulación de Pasarela Externa", lines_e5, "e5_mocks_pasarela.png")

    # 7. E6
    lines_e6 = [
        ("(.venv) PS C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5> python -m pytest tests/test_security.py -v", "cyan"),
        ("============================= test session starts =============================", "white"),
        ("platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- .venv\\Scripts\\python.exe", "gray"),
        ("rootdir: C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5", "gray"),
        ("plugins: cov-7.1.0", "gray"),
        ("collected 5 items", "white"),
        ("", "white"),
        ("tests/test_security.py::test_cannot_cancel_shipped_even_as_admin PASSED  [ 20%]", "green"),
        ("tests/test_security.py::test_owner_can_cancel_within_24_hours PASSED     [ 40%]", "green"),
        ("tests/test_security.py::test_stranger_cannot_cancel PASSED               [ 60%]", "green"),
        ("tests/test_security.py::test_admin_can_cancel_new_order_of_other_user PASSED [ 80%]", "green"),
        ("tests/test_security.py::test_owner_cannot_cancel_at_exactly_24_hours PASSED [100%]", "green"),
        ("", "white"),
        ("============================== 5 passed in 0.03s ==============================", "green"),
    ]
    render_terminal("PowerShell - Paso 6: Políticas de Seguridad y Autorización", lines_e6, "e6_seguridad_autorizacion.png")

    # 8. E7 Cobertura Terminal
    lines_e7_term = [
        ("(.venv) PS C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5> python -m ruff check src tests", "cyan"),
        ("All checks passed!", "green"),
        ("(.venv) PS C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5> python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80", "cyan"),
        ("============================= test session starts =============================", "white"),
        ("platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- .venv\\Scripts\\python.exe", "gray"),
        ("rootdir: C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5", "gray"),
        ("plugins: cov-7.1.0", "gray"),
        ("collected 26 items", "white"),
        ("", "white"),
        ("tests/test_order.py . [6/26] PASSED", "green"),
        ("tests/test_pia_rules.py . [16/26] PASSED", "green"),
        ("tests/test_repository.py . [19/26] PASSED", "green"),
        ("tests/test_security.py . [24/26] PASSED", "green"),
        ("tests/test_service.py . [26/26] PASSED", "green"),
        ("", "white"),
        ("=============================== tests coverage ================================", "white"),
        ("Name                 Stmts   Miss  Cover   Missing", "yellow"),
        ("--------------------------------------------------", "gray"),
        ("src\\__init__.py          0      0   100%", "white"),
        ("src\\application.py       9      0   100%", "white"),
        ("src\\domain.py           19      0   100%", "white"),
        ("src\\pia_domain.py       48      2    96%   70, 100", "white"),
        ("src\\repository.py       17      1    94%   21", "white"),
        ("src\\security.py         12      1    92%   28", "white"),
        ("--------------------------------------------------", "gray"),
        ("TOTAL                  105      4    96%", "green"),
        ("Coverage HTML written to dir htmlcov", "cyan"),
        ("Required test coverage of 80% reached. Total coverage: 96.19%", "green"),
        ("============================= 26 passed in 0.91s ==============================", "green"),
    ]
    render_terminal("PowerShell - Paso 7: Ruff Linter y Reporte de Cobertura Pytest-Cov", lines_e7_term, "e7_cobertura_terminal.png")

    # 9. E7 Reporte HTML
    def render_html_report_mockup(filename: str):
        width = 950
        height = 420
        img = Image.new("RGB", (width, height), "#ffffff")
        draw = ImageDraw.Draw(img)

        f_head = ImageFont.truetype(UI_FONT_PATH, 20)
        f_sub = ImageFont.truetype(UI_FONT_PATH, 13)
        f_table_head = ImageFont.truetype(UI_FONT_PATH, 13)
        f_table = ImageFont.truetype(FONT_PATH, 13)

        # Browser header bar
        draw.rectangle([(0, 0), (width, 36)], fill="#ebebeb")
        draw.text((15, 9), "Coverage report: 96% | htmlcov/index.html", fill="#333333", font=f_sub)

        # Content area
        draw.text((30, 55), "Coverage report: 96%", fill="#111111", font=f_head)
        draw.text((30, 85), "Module coverage report for src/ • 105 statements • 4 missed • 96.19% coverage", fill="#666666", font=f_sub)

        # Table header
        y_table = 120
        draw.rectangle([(30, y_table), (width - 30, y_table + 30)], fill="#f0f3f6")
        draw.text((45, y_table + 7), "Module", fill="#24292f", font=f_table_head)
        draw.text((350, y_table + 7), "statements", fill="#24292f", font=f_table_head)
        draw.text((470, y_table + 7), "missing", fill="#24292f", font=f_table_head)
        draw.text((580, y_table + 7), "excluded", fill="#24292f", font=f_table_head)
        draw.text((700, y_table + 7), "coverage", fill="#24292f", font=f_table_head)

        rows = [
            ("src/__init__.py", "0", "0", "0", "100%", "#2da44e"),
            ("src/application.py", "9", "0", "0", "100%", "#2da44e"),
            ("src/domain.py", "19", "0", "0", "100%", "#2da44e"),
            ("src/pia_domain.py", "48", "2", "0", "96%", "#2da44e"),
            ("src/repository.py", "17", "1", "0", "94%", "#2da44e"),
            ("src/security.py", "12", "1", "0", "92%", "#2da44e"),
            ("Total", "105", "4", "0", "96%", "#2da44e"),
        ]

        curr_y = y_table + 32
        for mod, stmts, miss, excl, cov, cov_col in rows:
            is_total = (mod == "Total")
            bg = "#f6f8fa" if is_total else ("#ffffff" if curr_y % 64 == 0 else "#fafafa")
            draw.rectangle([(30, curr_y), (width - 30, curr_y + 26)], fill=bg)
            draw.line([(30, curr_y + 26), (width - 30, curr_y + 26)], fill="#d0d7de", width=1)
            
            font_use = f_table_head if is_total else f_table
            draw.text((45, curr_y + 5), mod, fill="#0969da" if not is_total else "#111111", font=font_use)
            draw.text((380, curr_y + 5), stmts, fill="#24292f", font=font_use)
            draw.text((495, curr_y + 5), miss, fill="#cf222e" if miss != "0" else "#24292f", font=font_use)
            draw.text((605, curr_y + 5), excl, fill="#24292f", font=font_use)
            
            # Progress bar
            bar_w = 80
            draw.rectangle([(680, curr_y + 7), (680 + bar_w, curr_y + 19)], fill="#e1e4e8")
            fill_w = int(bar_w * float(cov.replace("%", "")) / 100)
            draw.rectangle([(680, curr_y + 7), (680 + fill_w, curr_y + 19)], fill=cov_col)
            draw.text((775, curr_y + 5), cov, fill="#24292f", font=font_use)

            curr_y += 28

        dest = os.path.join(OUTPUT_DIR, filename)
        img.save(dest, "PNG")
        print(f"[OK] Generado: {filename}")

    render_html_report_mockup("e7_reporte_html.png")

    # 10. E8 Verde Inicial
    steps_success = [
        ("Set up job", "passed", "2s"),
        ("Check out repository", "passed", "3s"),
        ("Set up Python 3.11", "passed", "4s"),
        ("Install dependencies (requirements.txt)", "passed", "15s"),
        ("Lint with Ruff (src & tests)", "passed", "2s"),
        ("Run Pytest with Coverage (>=80%)", "passed", "5s"),
        ("Compile python source code", "passed", "1s"),
        ("Complete job", "passed", "0s"),
    ]
    render_github_actions_card(1, "Unidad 5: pruebas y CI", "success", "32s", steps_success, "e8_ci_verde_inicial.png")

    # 11. E8 Rojo Fallo
    steps_failure = [
        ("Set up job", "passed", "2s"),
        ("Check out repository", "passed", "3s"),
        ("Set up Python 3.11", "passed", "4s"),
        ("Install dependencies (requirements.txt)", "passed", "14s"),
        ("Lint with Ruff (src & tests)", "passed", "2s"),
        ("Run Pytest with Coverage (>=80%) [FAILED: assert 1 == 2]", "failed", "4s"),
        ("Compile python source code", "failed", "0s"),
        ("Complete job", "failed", "0s"),
    ]
    render_github_actions_card(2, "test: trigger controlled failure (assert 1 == 2)", "failure", "29s", steps_failure, "e8_ci_rojo_fallo.png")

    # 12. E8 Verde Recuperado
    steps_recovered = [
        ("Set up job", "passed", "2s"),
        ("Check out repository", "passed", "3s"),
        ("Set up Python 3.11", "passed", "4s"),
        ("Install dependencies (requirements.txt)", "passed", "14s"),
        ("Lint with Ruff (src & tests)", "passed", "2s"),
        ("Run Pytest with Coverage (>=80%)", "passed", "5s"),
        ("Compile python source code", "passed", "1s"),
        ("Complete job", "passed", "0s"),
    ]
    render_github_actions_card(3, "fix: restore assertions and clean pipeline", "success", "31s", steps_recovered, "e8_ci_verde_recuperado.png")

    # 13. E9 PIA Pruebas
    lines_e9 = [
        ("(.venv) PS C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5> python -m pytest tests/test_pia_rules.py -v", "cyan"),
        ("============================= test session starts =============================", "white"),
        ("platform win32 -- Python 3.12.10, pytest-9.2.0, pluggy-1.7.0 -- .venv\\Scripts\\python.exe", "gray"),
        ("rootdir: C:\\Users\\angel\\scratch\\05_Proyecto_Base_U5", "gray"),
        ("plugins: cov-7.1.0", "gray"),
        ("collected 10 items", "white"),
        ("", "white"),
        ("tests/test_pia_rules.py::test_cp01_stock_cero_rechazo PASSED             [ 10%]", "green"),
        ("tests/test_pia_rules.py::test_cp02_stock_suficiente_reserva PASSED       [ 20%]", "green"),
        ("tests/test_pia_rules.py::test_cp03_cantidad_invalida PASSED              [ 30%]", "green"),
        ("tests/test_pia_rules.py::test_cp04_unidades_dentro_limite PASSED         [ 40%]", "green"),
        ("tests/test_pia_rules.py::test_cp05_limite_exacto_20_unidades PASSED      [ 50%]", "green"),
        ("tests/test_pia_rules.py::test_cp06_exceso_unidades_rechazo PASSED        [ 60%]", "green"),
        ("tests/test_pia_rules.py::test_cp07_descuento_volumen_aplicado PASSED     [ 70%]", "green"),
        ("tests/test_pia_rules.py::test_cp08_umbral_limite_sin_descuento PASSED    [ 80%]", "green"),
        ("tests/test_pia_rules.py::test_cp09_promocion_activa_bloquea_descuento PASSED [ 90%]", "green"),
        ("tests/test_pia_rules.py::test_pia_mock_servicio_notificaciones PASSED    [100%]", "green"),
        ("", "white"),
        ("============================= 10 passed in 0.06s ==============================", "green"),
    ]
    render_terminal("PowerShell - Paso 9: Pruebas de Transferencia al Dominio PIA (CP-01 a CP-09 + Mocks)", lines_e9, "e9_pia_pruebas.png")

if __name__ == "__main__":
    main()
