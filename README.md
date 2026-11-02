# Laboratorio Guiado · Unidad 5: Integración, Pruebas y Calidad
## Proyecto Base: `05_Proyecto_Base_U5`

Manual y paquete de trabajo para el desarrollo, prueba automatizada y aseguramiento de calidad de software con Python 3.11+, Pytest, SQLAlchemy, Mocks, Ruff y GitHub Actions CI.

---

## 📁 Estructura del Proyecto

```text
05_Proyecto_Base_U5/
├── .github/
│   └── workflows/
│       └── ci.yml               # Pipeline de integración continua (GitHub Actions)
├── datos/
│   ├── matriz_casos_prueba.csv  # Matriz de 12 casos de prueba para el PIA
│   └── pedidos_muestra.csv      # Fixtures de datos de prueba
├── evidencias/
│   ├── capturas/                # Capturas y reporte HTML de cobertura
│   └── Reporte_U5.pdf           # Reporte de documentación
├── src/
│   ├── __init__.py
│   ├── domain.py                # Reglas de negocio de pedidos (Order)
│   ├── application.py           # Servicio de checkout y cobros
│   ├── repository.py            # Persistencia con SQLAlchemy ORM
│   ├── security.py              # Políticas de autorización de cancelación
│   └── pia_domain.py            # 3 reglas de negocio del PIA de la empresa
├── tests/
│   ├── __init__.py
│   ├── test_order.py            # Pruebas unitarias de dominio y ciclo TDD
│   ├── test_repository.py       # Pruebas de integración, commit y rollback
│   ├── test_service.py          # Pruebas con Mocks de pasarela externa
│   ├── test_security.py         # Pruebas de seguridad y ventana de tiempo
│   └── test_pia_rules.py        # Casos del PIA CP-01 a CP-09 y CP-12
├── INSTRUCCIONES_AGY.md         # Hoja de ruta para ejecución por Antigravity / Alumno
├── README.txt                   # Manual rápido en texto plano
├── README.md                    # Documentación principal del repositorio
├── requirements.txt             # Dependencias del proyecto
├── .gitignore                   # Exclusiones de Git
└── verificar_laboratorio.py     # Script de autodiagnóstico integral
```

---

## 🚀 Instalación y Verificación Rápida

### 1. Crear y activar el entorno virtual
En Windows (PowerShell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
En macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias
```bash
python -m pip install -r requirements.txt
```

### 3. Ejecutar las pruebas
```bash
python -m pytest -v
```

### 4. Ejecutar el verificador automatizado
```bash
python verificar_laboratorio.py
```

### 5. Medir cobertura y revisar con Ruff
```bash
python -m ruff check src tests
python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html:evidencias/capturas/cobertura --cov-fail-under=80
```
El reporte HTML verificable se generará en `evidencias/capturas/cobertura/index.html`, dentro de la carpeta de evidencias.


## 📋 Pasos del Laboratorio
1. **Paso 1:** Instalar y verificar entorno virtual y pytest.
2. **Paso 2:** Comprender pruebas unitarias y añadir pruebas de $200 para VIP ($170) y regular ($200).
3. **Paso 3:** Ciclo TDD (Red -> Green -> Refactor) para evitar doble confirmación.
4. **Paso 4:** Integración con base de datos SQLAlchemy, commit y rollback.
5. **Paso 5:** Simulación de pasarela de pago con `unittest.mock.Mock`.
6. **Paso 6:** Políticas de seguridad, roles y límite temporal estricto (< 24h).
7. **Paso 7:** Linter Ruff y umbral de cobertura ≥ 80%.
8. **Paso 8:** Configuración y ejecución de CI en GitHub Actions.
9. **Paso 9:** Matriz de 12 casos (5 de éxito, 4 de error y 3 de límite), además de pruebas de persistencia y mocks adaptadas al PIA. CP-10 y CP-11 se ejecutan en las pruebas de repositorio y servicio, respectivamente.
10. **Paso 10:** Las capturas de las pruebas y la cobertura están en `evidencias/capturas/`.
