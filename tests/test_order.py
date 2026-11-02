"""
Pruebas Unitarias del Dominio de Pedidos (tests/test_order.py)
Verifica las reglas de negocio de la entidad Order.
"""
import pytest

from src.domain import Order


def test_vip_discount():
    """Verifica descuento del 15% para cliente VIP con pedido de $100."""
    o = Order(100, vip=True)       # Arrange: preparar
    assert o.confirm() == 85       # Act + Assert: confirmar y verificar
    assert o.status == "CONFIRMED" # Assert: estado final


def test_customer_debt():
    """Verifica que un pedido no pueda confirmarse si el cliente tiene deuda."""
    o = Order(100, has_debt=True)
    with pytest.raises(ValueError, match="customer has pending debt"):
        o.confirm()


def test_invalid_total():
    """Verifica que se rechacen pedidos con importe menor o igual a cero."""
    o_zero = Order(0)
    with pytest.raises(ValueError, match="total must be greater than zero"):
        o_zero.confirm()

    o_negative = Order(-50)
    with pytest.raises(ValueError, match="total must be greater than zero"):
        o_negative.confirm()


# =============================================================================
# ACTIVIDADES PARA EL ALUMNO / ANTIGRAVITY:
# =============================================================================

# PASO 2 · Pruebas unitarias adicionales requeridas:
# -----------------------------------------------------------------------------
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


# PASO 3 · Ciclo TDD (Red -> Green -> Refactor):
# -----------------------------------------------------------------------------
def test_cannot_confirm_twice():
    """
    Regla nueva: No se puede confirmar un pedido que ya fue confirmado.
    1. RED: Descomentar esta prueba ANTES de modificar src/domain.py.
       Ejecutar 'pytest tests/test_order.py' y verificar que FALLA (FAIL).
    2. GREEN: Añadir validación en src/domain.py y comprobar que PASA.
    """
    order = Order(100)
    order.confirm()
    with pytest.raises(ValueError, match="already confirmed"):
        order.confirm()

