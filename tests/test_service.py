"""
Pruebas de Servicios de Aplicación con Mocks (tests/test_service.py)
Comprueba el servicio de checkout simulando la pasarela externa de cobros.
"""
from unittest.mock import Mock

import pytest

from src.application import OrderService
from src.domain import Order


def test_payment_approved_example():
    """Comprueba cobro exitoso cuando la pasarela responde True."""
    gateway = Mock()
    gateway.charge.return_value = True

    amount = OrderService(gateway).checkout(Order(100))

    assert amount == 100
    gateway.charge.assert_called_once_with(100)


# =============================================================================
# ACTIVIDAD PARA EL ALUMNO / ANTIGRAVITY (Paso 5 del manual):
# =============================================================================
def test_payment_rejected_vip_order():
    """
    Actividad Paso 5: Prueba de rechazo para un pedido VIP de $200.
    - Verifica que el intento de cobro fue por $170 (15% de descuento).
    - Verifica que se lanzó RuntimeError("payment rejected").
    """
    gateway = Mock()
    gateway.charge.return_value = False

    order = Order(200, vip=True)
    service = OrderService(gateway)

    with pytest.raises(RuntimeError, match="payment rejected"):
        service.checkout(order)

    gateway.charge.assert_called_once_with(170)

