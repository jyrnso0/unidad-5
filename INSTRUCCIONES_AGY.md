# Instrucciones de Ejecución para Antigravity (Unidad 5)
## Laboratorio Guiado: Integración, Pruebas y Calidad

> **Aviso para Antigravity / Asistente de IA:**
> Este documento contiene la hoja de ruta técnica completa y detallada para resolver, ejecutar y generar todas las evidencias de la Unidad 5 de forma impecable y sin ambigüedades. Sigue cada paso en el orden indicado.

---

## 🎯 Objetivo Global
Comprobar mediante pruebas automatizadas (unitarias, integración con base de datos SQLAlchemy, mocks y políticas de seguridad) que las reglas del dominio se cumplen cabalmente, alcanzar una cobertura de código **≥ 80%**, configurar y validar el pipeline de **GitHub Actions CI**, adaptar 3 reglas de negocio al PIA de la empresa con una **matriz de 9 casos de prueba** y generar el informe de evidencias **E1 a E9**.

---

## 🛠️ Requisitos y Entorno
1. **Python:** 3.11 o superior.
2. **Dependencias:** `requirements.txt` (`pytest`, `pytest-cov`, `SQLAlchemy`, `ruff`).
3. **Instalación en consola:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

---

## 📋 Hoja de Ruta Paso a Paso

### PASO 1 · Comprobación Inicial del Proyecto (Evidencia E1)
1. Ejecuta la suite inicial de pruebas:
   ```powershell
   python -m pytest -v
   ```
2. **Resultado esperado:** Todas las pruebas base existentes deben terminar en estado `PASSED`.
3. **Para Evidencia E1:** Toma nota de la salida de la terminal y redacta la justificación técnica de 3 líneas sobre la utilidad de `pytest` y `venv` (ya disponible como modelo en `evidencias/EVIDENCIAS_GUIA_PLANTILLA.md`).

---

### PASO 2 · Pruebas Unitarias de Dominio (Evidencia E2)
1. Abre `tests/test_order.py`.
2. Añade (o descomenta) las siguientes dos pruebas unitarias:
   ```python
   def test_vip_discount_200():
       """Verifica que un cliente VIP con total 200 recibe 15% de descuento ($170)."""
       order = Order(200, vip=True)
       assert order.confirm() == 170
       assert order.status == "CONFIRMED"

   def test_regular_no_discount_200():
       """Verifica que un cliente regular con total 200 no recibe descuento ($200)."""
       order = Order(200, vip=False)
       assert order.confirm() == 200
       assert order.status == "CONFIRMED"
   ```
3. Ejecuta:
   ```powershell
   python -m pytest tests/test_order.py -v
   ```
4. **Para Evidencia E2:** Registra la tabla comparativa con: Entrada, Regla, Resultado Esperado, Resultado Real y Estado `PASSED`.

---

### PASO 3 · Ciclo TDD Real: Red → Green → Refactor (Evidencia E3)
> **Regla nueva a implementar:** No permitir confirmar un pedido que ya fue confirmado previamente.

1. **FASE RED:**
   En `tests/test_order.py`, añade (o descomenta):
   ```python
   def test_cannot_confirm_twice():
       order = Order(100)
       order.confirm()
       with pytest.raises(ValueError, match="already confirmed"):
           order.confirm()
   ```
   Ejecuta: `python -m pytest tests/test_order.py -v -k test_cannot_confirm_twice`.
   **Resultado esperado:** `FAILED` (DID NOT RAISE ValueError). Captura este resultado para la evidencia RED.

2. **FASE GREEN:**
   En `src/domain.py`, al inicio del método `confirm()` de la clase `Order`, añade:
   ```python
   if self.status == "CONFIRMED":
       raise ValueError("already confirmed")
   ```
   Ejecuta nuevamente: `python -m pytest tests/test_order.py -v`.
   **Resultado esperado:** `PASSED`. Captura este resultado para la evidencia GREEN.

3. **FASE REFACTOR:**
   Verifica que la implementación sea concisa y no rompa ninguna otra prueba existente ejecutando la suite completa.

---

### PASO 4 · Integración con Base de Datos y Transacciones (Evidencia E4)
1. Abre `tests/test_repository.py`.
2. Añade (o descomenta) la prueba para guardar un pedido con `id=2` y `total=250`:
   ```python
   def test_repository_save_order_250_commit(session):
       repo = SqlOrderRepository(session)
       order = OrderRow(id=2, total=250.0, status="CONFIRMED")
       repo.save(order)
       session.commit()

       saved = repo.get_by_id(2)
       assert saved is not None
       assert saved.id == 2
       assert saved.total == 250.0
       assert saved.status == "CONFIRMED"
   ```
3. Ejecuta:
   ```powershell
   python -m pytest tests/test_repository.py -v
   ```
4. **Para Evidencia E4:** Explica la diferencia técnica entre `commit` (hace persistentes e irrevocables los cambios en la BD) y `rollback` (revierte la sesión al estado previo descartando modificaciones no confirmadas).

---

### PASO 5 · Simulación de Servicios Externos con Mocks (Evidencia E5)
1. Abre `tests/test_service.py`.
2. Añade (o descomenta) la prueba de rechazo para pedido VIP de $200:
   ```python
   def test_payment_rejected_vip_order():
       gateway = Mock()
       gateway.charge.return_value = False

       order = Order(200, vip=True)
       service = OrderService(gateway)

       with pytest.raises(RuntimeError, match="payment rejected"):
           service.checkout(order)

       gateway.charge.assert_called_once_with(170)
   ```
3. Ejecuta:
   ```powershell
   python -m pytest tests/test_service.py -v
   ```
4. **Para Evidencia E5:** Documenta la propuesta arquitectónica para evitar inconsistencia (Two-Phase Commit / State Machine transitorio `PENDING_PAYMENT` antes de confirmar).

---

### PASO 6 · Seguridad y Políticas de Autorización (Evidencia E6)
1. Abre `tests/test_security.py`.
2. Añade (o descomenta) los casos de prueba de administrador y límite temporal:
   ```python
   def test_admin_can_cancel_new_order_of_other_user():
       now = datetime(2026, 1, 1, 12, 0)
       created = now - timedelta(hours=48)
       assert can_cancel("NEW", owner="alice", user="admin", is_admin=True, created_at=created, now=now)

   def test_owner_cannot_cancel_at_exactly_24_hours():
       now = datetime(2026, 1, 2, 12, 0)
       created = datetime(2026, 1, 1, 12, 0) # Exactamente 24 horas
       assert not can_cancel("NEW", owner="alice", user="alice", is_admin=False, created_at=created, now=now)
   ```
3. Ejecuta:
   ```powershell
   python -m pytest tests/test_security.py -v
   ```
4. **Para Evidencia E6:** Genera la matriz de autorización cruzando: rol, propietario, estado, antigüedad y permiso concedido/denegado.

---

### PASO 7 · Cobertura y Linter Ruff (Evidencia E7)
1. Ejecuta el linter Ruff:
   ```powershell
   python -m ruff check src tests
   ```
   **Resultado esperado:** `All checks passed!`.
2. Ejecuta pytest con cobertura y umbral ≥ 80%:
   ```powershell
   python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=80
   ```
3. Revisa el reporte en `htmlcov/index.html`.
4. **Para Evidencia E7:** Documenta el resumen numérico de cobertura (alcanzando 100% o ≥ 80%) y el análisis de ramas probadas.

---

### PASO 8 · Automatización con GitHub Actions CI (Evidencia E8)
1. Verifica que el archivo `.github/workflows/ci.yml` contenga el workflow `CI Business Logic`.
2. Inicializa git y publica el repositorio en GitHub:
   ```powershell
   git init
   git add .
   git commit -m "Unidad 5: pruebas y CI"
   git branch -M main
   git remote add origin <URL_DEL_REPOSITORIO>
   git push -u origin main
   ```
3. En la pestaña **Actions** de GitHub:
   - Verifica la ejecución verde inicial.
   - Para la prueba de fallo controlado: modifica temporalmente una aserción para que falle (ej. `assert 1 == 2`), haz commit y push, y captura el fallo rojo en Actions.
   - Revierte el cambio, haz commit y push, y captura el regreso a verde.

---

### PASO 9 · Adaptación al PIA de la Empresa (Evidencia E9)
1. Las 3 reglas de negocio del PIA están implementadas en `src/pia_domain.py`:
   - **Regla 1 (Stock):** Control de existencias e inventario (`CP-01`, `CP-02`, `CP-03`).
   - **Regla 2 (Límite):** Máximo 20 unidades por pedido (`CP-04`, `CP-05`, `CP-06`).
   - **Regla 3 (Volumen):** 5% de descuento en compras > $5,000 sin promoción (`CP-07`, `CP-08`, `CP-09`).
2. La matriz de casos de prueba está en `datos/matriz_casos_prueba.csv`.
3. Ejecuta la suite de pruebas del PIA:
   ```powershell
   python -m pytest tests/test_pia_rules.py -v
   ```
4. **Para Evidencia E9:** Presenta la matriz CSV con los 9 casos y los resultados `PASSED`.

---

### PASO 10 · Cierre y Reporte Final
1. Abre `evidencias/EVIDENCIAS_GUIA_PLANTILLA.md`.
2. Completa los datos del estudiante, verifica las tablas, inserta las capturas obtenidas en `evidencias/capturas/` y revisa la reflexión final de 150 a 200 palabras.
3. Ejecuta `python verificar_laboratorio.py` para una comprobación final antes de empaquetar o entregar.

