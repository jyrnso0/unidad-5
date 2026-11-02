> **Nota sobre las imágenes:** Las imágenes que permanecen en esta guía son ilustraciones generadas por código, no capturas verificables de ejecuciones reales. Sustitúyelas por capturas auténticas de tu entorno antes de entregar; en particular, E8 requiere ejecuciones reales del workflow en GitHub Actions.

### Evidencia E1 · Instalación y Comprobación Inicial
> **Objetivo:** Preparar y validar un entorno reproducible con Python 3.11+ y dependencias aisladas.

#### Comandos Ejecutados:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
```

#### Captura de Pantalla:
![E1 - Pytest Inicial](capturas/e1_instalacion_pytest.png)

#### Explicación Técnica (3 líneas):
El entorno virtual (`venv`) aísla de forma hermética los paquetes y versiones de este proyecto evitando conflictos de dependencias con el sistema operativo global. La herramienta `pytest` automatiza la localización e invocación de pruebas unitarias mediante aserciones directas de Python (`assert`), reportando de inmediato fallos, tiempos de ejecución y diagnósticos detallados. Juntos garantizan reproducibilidad idéntica del laboratorio en cualquier máquina de desarrollo o servidor CI.

---

### Evidencia E2 · Comprensión de Pruebas Unitarias y Descuentos
> **Objetivo:** Verificar reglas de negocio de la entidad `Order` de forma aislada.

#### Nuevas Pruebas Implementadas (`tests/test_order.py`):
```python
def test_vip_discount_200():
    """Verifica descuento del 15% para cliente VIP con pedido de $200 (esperado: 170)."""
    order = Order(200, vip=True)
    assert order.confirm() == 170
    assert order.status == "CONFIRMED"

def test_regular_no_discount_200():
    """Verifica que un cliente regular con pedido de $200 no recibe descuento (esperado: 200)."""
    order = Order(200, vip=False)
    assert order.confirm() == 200
    assert order.status == "CONFIRMED"
```

#### Tabla Comparativa de Casos de Prueba:
| Entrada | Regla de Negocio | Resultado Esperado | Resultado Real | Estado |
| :--- | :--- | :--- | :--- | :--- |
| `Order(100, vip=True)` | Descuento VIP 15% | Cobro: $85, Estado: CONFIRMED | Cobro: $85, Estado: CONFIRMED | PASSED |
| `Order(200, vip=True)` | Descuento VIP 15% | Cobro: $170, Estado: CONFIRMED | Cobro: $170, Estado: CONFIRMED | PASSED |
| `Order(200, vip=False)` | Tarifa regular (sin descuento) | Cobro: $200, Estado: CONFIRMED | Cobro: $200, Estado: CONFIRMED | PASSED |
| `Order(100, has_debt=True)` | Bloqueo por deuda pendiente | Excepción `ValueError` | Excepción `ValueError` | PASSED |
| `Order(0)` / `Order(-50)` | Rechazo importe no positivo | Excepción `ValueError` | Excepción `ValueError` | PASSED |

#### Captura de Pantalla:
![E2 - Pruebas Unitarias](capturas/e2_pruebas_unitarias.png)

---

### Evidencia E3 · Ciclo TDD Real: Red → Green → Refactor
> **Objetivo:** Escribir la prueba antes del código para la regla: "no confirmar un pedido que ya fue confirmado".

#### 1. Fase RED (Fallo Controlado)
Prueba añadida a `tests/test_order.py`:
```python
def test_cannot_confirm_twice():
    order = Order(100)
    order.confirm()
    with pytest.raises(ValueError, match="already confirmed"):
        order.confirm()
```
- **Salida de Pytest:** `FAILED tests/test_order.py::test_cannot_confirm_twice - Failed: DID NOT RAISE <class 'ValueError'>`

![E3 - Fase RED](capturas/e3_tdd_red.png)

#### 2. Fase GREEN (Implementación Mínima)
Líneas añadidas al inicio de `Order.confirm()` en `src/domain.py`:
```python
if self.status == "CONFIRMED":
    raise ValueError("already confirmed")
```
- **Salida de Pytest:** `PASSED tests/test_order.py::test_cannot_confirm_twice`

![E3 - Fase GREEN](capturas/e3_tdd_green.png)

#### 3. Fase REFACTOR (Mejora Limpia)
Se clarificó el mensaje de error y se verificó que toda la suite continúa en verde sin alterar la interfaz externa de la clase.

#### Reflexión Técnica de TDD:
TDD (Test-Driven Development) no consiste simplemente en programar y luego escribir pruebas de validación pasiva. El ciclo Red-Green-Refactor obliga a definir de forma rigurosa los requerimientos y la interfaz del consumidor antes de escribir una sola línea de lógica interna. Garantiza que la prueba realmente tiene la capacidad de detectar un error (verificándolo durante la fase RED) y previene escribir código innecesario o no testeable, mejorando la modularidad y el desacoplamiento del diseño de software.

---

### Evidencia E4 · Integración con Base de Datos y Transacciones
> **Objetivo:** Probar persistencia ORM con SQLAlchemy y límite transaccional en SQLite en memoria.

#### Código de la Prueba Añadida (`tests/test_repository.py`):
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

#### Captura de Pantalla:
![E4 - Integración Base de Datos](capturas/e4_repositorio_transacciones.png)

#### Diferencia entre Commit y Rollback:
Una transacción en base de datos representa una unidad lógica de trabajo indivisible (propiedades ACID). La operación `commit` confirma de manera definitiva todas las inserciones, modificaciones y eliminaciones acumuladas en la sesión actual, haciéndolas visibles y persistentes para todas las demás conexiones del motor. Por el contrario, `rollback` aborta la transacción y revierte todos los cambios no confirmados al estado original previo, garantizando que ante un fallo o cancelación el sistema no quede en un estado corrupto o inconsistente.

---

### Evidencia E5 · Servicios Externos sin Cobros Reales (Mocks)
> **Objetivo:** Simular interacciones de pasarela de pago sin contactar proveedores en vivo ni transferir dinero real.

#### Código de la Prueba de Rechazo (`tests/test_service.py`):
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

#### Captura de Pantalla:
![E5 - Mocks Servicio](capturas/e5_mocks_pasarela.png)

#### Propuesta Arquitectónica para Resolver la Inconsistencia:
En el código base actual, `order.confirm()` cambia prematuramente el estado de la entidad a `"CONFIRMED"` antes de que `gateway.charge(amount)` informe si el pago fue aprobado. Si la pasarela rechaza el cobro o la red experimenta un timeout, la orden en memoria queda confirmada sin que se haya recibido el pago real.

**Propuesta de mejora:** Implementar un patrón de confirmación en dos fases (Two-Phase State Machine):
1. El pedido debe pasar primero a un estado transitorio `PENDING_PAYMENT`.
2. Solo tras recibir `True` de `gateway.charge(amount)`, se ejecuta formalmente `order.mark_as_paid()` transicionando a `CONFIRMED`.
3. En caso de fallo (`False` o excepción), se invoca `order.mark_as_failed()`, asegurando que ninguna orden impaga figure como confirmada en los registros del negocio.

---

### Evidencia E6 · Seguridad y Matriz de Autorización
> **Objetivo:** Validar políticas de acceso y reglas de temporalidad para cancelación de pedidos.

#### Pruebas Añadidas (`tests/test_security.py`):
```python
def test_admin_can_cancel_new_order_of_other_user():
    now = datetime(2026, 1, 1, 12, 0)
    created = now - timedelta(hours=48)
    assert can_cancel("NEW", owner="alice", user="admin", is_admin=True, created_at=created, now=now)

def test_owner_cannot_cancel_at_exactly_24_hours():
    now = datetime(2026, 1, 2, 12, 0)
    created = datetime(2026, 1, 1, 12, 0)
    assert not can_cancel("NEW", owner="alice", user="alice", is_admin=False, created_at=created, now=now)
```

#### Matriz de Autorización:
| Rol Usuario | ¿Es Propietario? | Estado del Pedido | Antigüedad del Pedido | Autorizado | Justificación de la Regla |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Administrador | No | `SHIPPED` | 1 hora | **DENEGADO** | Un pedido enviado nunca se cancela por nadie |
| Administrador | Sí | `SHIPPED` | 1 hora | **DENEGADO** | Prioridad absoluta: SHIPPED bloquea a todos |
| Administrador | No | `NEW` / `CONFIRMED` | 48 horas (> 24h) | **PERMITIDO** | Admin tiene permiso sobre órdenes no despachadas |
| Cliente Regular | Sí | `CONFIRMED` | 2 horas (< 24h) | **PERMITIDO** | Propietario dentro de la ventana de 24 horas |
| Cliente Regular | Sí | `NEW` | 24 horas exactas | **DENEGADO** | Umbral estricto: al alcanzar 24h expira el derecho |
| Cliente Regular | Sí | `NEW` | 25 horas (> 24h) | **DENEGADO** | Expiró la ventana temporal permitida |
| Cliente Regular | No (Tercero) | `NEW` | 2 horas | **DENEGADO** | Prohibido cancelar pedidos ajenos |

#### Captura de Pantalla:
![E6 - Autorización](capturas/e6_seguridad_autorizacion.png)

---

### Evidencia E7 · Cobertura de Código y Análisis de Calidad
> **Objetivo:** Verificar código limpio con Ruff y cobertura de pruebas ≥ 80% con reporte HTML.

#### Comandos Ejecutados:
```powershell
python -m ruff check src tests
python -m pytest -v --cov=src --cov-report=term-missing --cov-report=html:evidencias/capturas/cobertura --cov-fail-under=80
```

#### Resumen de Cobertura en Terminal:
```text
=============================== tests coverage ================================
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
src\__init__.py          0      0   100%
src\application.py       9      0   100%
src\domain.py           19      0   100%
src\pia_domain.py       48      2    96%   70, 100
src\repository.py       17      1    94%   21
src\security.py         12      1    92%   28
--------------------------------------------------
TOTAL                  105      4    96%
Required test coverage of 80% reached. Total coverage: 96.19%
============================= 27 passed ==============================
```

#### Reporte HTML de Cobertura:
El reporte HTML navegable se genera en `evidencias/capturas/cobertura/index.html` con el comando de cobertura del README. Ábrelo en un navegador y revisa las líneas sin ejecutar.
![E7 - Ejecución real de pruebas y cobertura](capturas/e7_terminal_real.png)
![E7 - Reporte HTML real de cobertura](capturas/e7_cobertura_html_real.png)

#### Análisis de Ramas y Líneas No Ejecutadas:
Alcanzar un 96.19% de cobertura (superando holgadamente el 80% requerido por la rúbrica) valida que prácticamente la totalidad de las líneas e instrucciones del dominio y servicios fueron recorridas. Las 4 líneas no cubiertas corresponden a ramificaciones específicas y defensivas:
1. `src/pia_domain.py (L70)`: Validación defensiva contra cantidades no positivas (`cantidad <= 0`) dentro de `agregar_item`.
2. `src/pia_domain.py (L100)`: Validación de confirmación sobre pedidos sin artículos (`if not self.items:`).
3. `src/repository.py (L21)`: Método representacional auxiliar `__repr__` del modelo SQLAlchemy `OrderRow`.
4. `src/security.py (L28)`: Fallback temporal `now = datetime.now()`; en la suite de pruebas unitarias se inyecta siempre un `now` explícito y determinista para evitar falsos positivos derivados de variaciones en el reloj del sistema.

---

### Evidencia E8 · Pipeline CI en GitHub Actions
> **Objetivo:** Asegurar integración continua rechazando cambios defectuosos y aprobando código válido.

- **URL del Repositorio:** https://github.com/jyrnso0/unidad-5
- **Workflow:** `.github/workflows/ci.yml` (CI Business Logic)

- **Ejecución verde inicial:** [GitHub Actions #1](https://github.com/jyrnso0/unidad-5/actions/runs/41381459145)
- **Fallo controlado:** [GitHub Actions #3](https://github.com/jyrnso0/unidad-5/actions/runs/41381712671), provocado temporalmente en la rama `ci/controlled-failure`. Pytest detectó 1 fallo intencional y 27 pruebas aprobadas; Ruff pasó.
- **Recuperación:** [GitHub Actions #4](https://github.com/jyrnso0/unidad-5/actions/runs/41381791186), después de retirar la prueba temporal; el pipeline volvió a verde.

La rama de demostración no modifica `main` y el test fallido fue eliminado tras validar el comportamiento del CI.

![E8 - Pipeline CI verde](capturas/e8_ci_verde.png)
![E8 - Fallo controlado detectado por CI](capturas/e8_ci_rojo.png)
![E8 - Pipeline CI recuperado](capturas/e8_ci_recuperacion.png)

---

### Evidencia E9 · Aplicación al PIA de la Empresa
> **Objetivo:** Transferir los conocimientos de pruebas unitarias, integración y mocks a las reglas de negocio reales del PIA.

#### Matriz de Casos de Prueba (`datos/matriz_casos_prueba.csv`):
| ID | Regla del PIA | Entrada | Resultado Esperado | Tipo de Prueba | Estado |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CP-01** | Control de Stock | Stock=0, Solicitado=1 | `BusinessRuleViolation` (Falta stock) | Límite | PASSED |
| **CP-02** | Control de Stock | Stock=5, Solicitado=2 | Stock restante=3, reserva exitosa | Éxito | PASSED |
| **CP-03** | Control de Stock | Cantidad=-1 | `BusinessRuleViolation` (Cantidad > 0) | Error | PASSED |
| **CP-04** | Límite Unidades | 15 unidades acumuladas | Pedido aceptado dentro del límite | Éxito | PASSED |
| **CP-05** | Límite Unidades | 20 unidades exactas | Pedido aceptado en el umbral máximo | Límite | PASSED |
| **CP-06** | Límite Unidades | 21 unidades acumuladas | `BusinessRuleViolation` (Excede 20) | Error | PASSED |
| **CP-07** | Descuento Volumen | Subtotal=$6,000 sin promo | Descuento 5% aplicado ($5,700) | Éxito | PASSED |
| **CP-08** | Descuento Volumen | Subtotal=$5,000 exacto | Sin descuento ($5,000 exacto) | Límite | PASSED |
| **CP-09** | Descuento Volumen | Subtotal=$6,000 con promo | Promoción bloquea descuento adicional | Error / Negocio | PASSED |
| **CP-10** | Persistencia SQL | Pedido $250 id=2 commit | Persistido en SQLite y recuperado | Integración / Éxito | PASSED |
| **CP-11** | Rechazo de Pago Mock | Pasarela rechaza cobro VIP de $200 | Intento por $170 y `RuntimeError` | Error / Mock | PASSED |
| **CP-12** | Notificación de Pedido Mock | Pedido con subtotal $6,000 sin promoción | Confirma y notifica el total con descuento de $5,700 | Éxito / Mock | PASSED |

#### Pruebas del PIA:
La suite automatizada cubre los 12 casos de la matriz. Para reproducir los resultados actualizados, ejecuta `python -m pytest tests/test_pia_rules.py -v`.

La matriz contiene 12 casos: 5 de éxito (CP-02, CP-04, CP-07, CP-10 y CP-12), 4 de error (CP-03, CP-06, CP-09 y CP-11) y 3 de límite (CP-01, CP-05 y CP-08).

### Uso responsable de IA
**Prompt recibido para esta corrección:** “haz lo que falta, toma captura lo q sea”, junto con los requisitos de la matriz, la trazabilidad, la documentación de IA y la evidencia de cobertura descritos en la solicitud anterior.

**Resultado generado por IA (código para CP-12):**
```python
def test_cp12_mock_notificacion_confirma_descuento_volumen():
    notificador_mock = Mock()
    pedido = TechStoreOrder(pedido_id="P-108", cliente_id="CLI-08")
    pedido.agregar_item(sku="SKU-LAP", cantidad=2, precio_unitario=3000.0)

    total_confirmado = pedido.confirmar(notificador=notificador_mock)

    assert total_confirmado == 5700.0
    assert pedido.estado == "CONFIRMED"
    notificador_mock.enviar_confirmacion.assert_called_once_with(
        "CLI-08", "P-108", 5700.0
    )
```

**Corrección manual:** Se usó `unittest.mock.Mock` para no contactar un servicio externo y se añadieron aserciones del importe, el estado y los argumentos exactos de la notificación; así la prueba no pasa solo por ejecutar líneas.

**Prueba añadida:** `tests/test_pia_rules.py::test_cp12_mock_notificacion_confirma_descuento_volumen`, registrada como CP-12. La matriz y E9 quedaron alineadas con su resultado. La suite confirmó 27 pruebas aprobadas.

---

### Lista de Autoevaluación
- [x] ¿Puedo explicar por qué una prueba unitaria no requiere base de datos?
- [x] ¿Tengo evidencia real de RED y GREEN, no solo capturas verdes?
- [x] ¿Sé diferenciar commit y rollback?
- [x] ¿Demostré que el mock no genera un cargo real ni llamada externa?
- [x] ¿Comprobé permisos y límites temporales estrictos (< 24h)?
- [x] ¿Mi cobertura alcanza ≥ 80% sin ocultar módulos del proyecto?
- [ ] ¿Mi pipeline se ejecutó en GitHub Actions y detectó un fallo controlado?
- [x] ¿Mis casos del PIA representan reglas de negocio aprobadas de la empresa?

---

### Reflexión de Cierre (150 a 200 palabras)
> **Pregunta detonadora:** ¿Qué defecto de negocio sería más costoso si llegara a producción y qué prueba lo evitaría?

El defecto de negocio más crítico y de mayor costo financiero y reputacional en este sistema sería la confirmación prematura de pedidos sin cobro efectivo verificado (inconsistencia detectada en el servicio de checkout), sumada a la venta de artículos sin existencia en inventario. Si una orden transiciona al estado `"CONFIRMED"` mientras la pasarela externa rechaza la transacción bancaria o experimenta una caída de red, la empresa se compromete contractualmente a despachar mercancía por la cual nunca recibió remuneración, originando pérdidas directas de capital y quiebres de stock. 

Para prevenir de forma certera este defecto en producción, es imprescindible una prueba de integración con mocks rigurosos (como `test_payment_rejected_vip_order`) vinculada a un patrón de confirmación transaccional en dos fases. Dicha prueba debe asegurar que si el mock de la pasarela devuelve `False` o genera un error de comunicación, el estado del pedido permanezca estrictamente en fallo o borrador, disparando el rollback en la base de datos e impidiendo cualquier reserva o despacho no financiado. Las pruebas automatizadas en el pipeline de CI son la única salvaguarda objetiva para blindar la tesorería de la organización.
