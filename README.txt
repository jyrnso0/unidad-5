CALIDAD Y PRUEBAS U5 - PAQUETE DEL ALUMNO (05_Proyecto_Base_U5)

OBJETIVO: Desarrollar, verificar y automatizar pruebas unitarias, de integracion con persistencia SQLAlchemy, simulacion de pasarelas con mocks, revision de politicas de seguridad, analisis de cobertura (>=80%), pipeline de GitHub Actions y adaptacion de reglas de negocio para el PIA de la empresa.

CONTENIDO DEL PAQUETE
 src/domain.py: Entidad Order con reglas de validacion, descuentos VIP (15%) y transicion de estados.
 src/application.py: OrderService para coordinacion de cobro mediante pasarela de pagos externa.
 src/repository.py: Persistencia ORM de pedidos con SQLAlchemy (OrderRow y SqlOrderRepository).
 src/security.py: Politica de seguridad y autorizacion temporal para cancelacion de pedidos.
 src/pia_domain.py: Implementacion de las 3 reglas de negocio del PIA de la empresa (Stock, Limite de unidades y Descuento por volumen).
 tests/test_order.py: Suite de pruebas unitarias de dominio y ciclo TDD (Red -> Green -> Refactor).
 tests/test_repository.py: Pruebas de integracion, commit y rollback transaccional en SQLite en memoria.
 tests/test_service.py: Pruebas con Mocks (unittest.mock) para simulacion de la pasarela de pagos externa.
 tests/test_security.py: Pruebas de control de acceso y autorizacion (regla SHIPPED y limite de 24 horas).
 tests/test_pia_rules.py: Casos del PIA CP-01 a CP-09 y CP-12; CP-10 y CP-11 se prueban en repository y service.
 datos/matriz_casos_prueba.csv: Matriz estandarizada de 12 casos (5 exitos, 4 errores y 3 limites).
 datos/pedidos_muestra.csv: Fixtures de prueba con pedidos de muestra para persistencia y validacion.
 evidencias/capturas/: Ilustraciones conceptuales E1-E6, capturas reales E7-E8 e informe HTML de cobertura.
 .github/workflows/ci.yml: Pipeline de Integracion Continua (CI Business Logic) para GitHub Actions.
 requirements.txt: Lista de dependencias aisladas (pytest, pytest-cov, SQLAlchemy, ruff).
 .gitignore: Exclusion de entornos virtuales, caches (__pycache__, .pytest_cache) y reportes de cobertura.
 verificar_laboratorio.py: Script utilitario de autodiagnostico y verificacion integral en un solo paso.
 INSTRUCCIONES_AGY.md: Guia detallada de ejecucion paso a paso para el asistente Antigravity o el alumno.

PASO A PASO DE USO
 1. Preparacion del entorno:
    py -3.11 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt
    python -m pytest -v
 2. Pruebas Unitarias (Paso 2):
    Ejecuta python -m pytest tests/test_order.py -v. Las pruebas VIP ($200 -> $170) y regular ($200 -> $200) ya estan incluidas.
 3. Ciclo TDD (Paso 3):
    La prueba de doble confirmacion y su validacion ya estan implementadas. Ejecuta python -m pytest tests/test_order.py -v.
 4. Persistencia y Transacciones (Paso 4):
    Ejecuta python -m pytest tests/test_repository.py -v. Incluye commit y rollback.
 5. Mocks de Servicios Externos (Paso 5):
    Ejecuta python -m pytest tests/test_service.py -v. El rechazo de pago VIP de $200 ya esta probado con Mock.
 6. Seguridad y Autorizacion (Paso 6):
    Ejecuta tests/test_security.py y verifica que un admin cancela pedido NEW ajeno y que a las 24h exactas se rechaza.
 7. Cobertura y Calidad (Paso 7):
    python -m ruff check src tests
    python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html:evidencias/capturas/cobertura --cov-fail-under=80
 8. GitHub Actions CI (Paso 8):
    Repositorio: https://github.com/jyrnso0/unidad-5. El workflow se ejecuta en cada push.
    Ejecucion verde: https://github.com/jyrnso0/unidad-5/actions/runs/41381459145
    Fallo controlado: https://github.com/jyrnso0/unidad-5/actions/runs/41381712671
    Recuperacion verde: https://github.com/jyrnso0/unidad-5/actions/runs/41381791186
 9. Reglas del PIA (Paso 9):
    Ejecuta python -m pytest -v para verificar todos los casos automatizados y los 12 de
    datos/matriz_casos_prueba.csv (5 exitos, 4 errores y 3 limites), persistencia y mocks.
 10. Evidencias:
     Contiene el registro E1-E9 y las capturas verificables E7-E8.

REGLAS DIDACTICAS
 - Un pedido SHIPPED nunca se cancela, ni siquiera por el rol administrador.
 - El propietario regular solo tiene ventana de cancelacion menor a 24 horas (< 24h exactas).
 - El descuento VIP base es del 15%.
 - Los mocks nunca deben transmitir dinero real ni realizar peticiones HTTP de produccion.
 - SQLite en memoria (:memory:) se recrea por prueba, garantizando aislamiento transaccional hermetico.

ADVERTENCIA
 No subas al repositorio la carpeta .venv/, htmlcov/, ni credenciales personales.
