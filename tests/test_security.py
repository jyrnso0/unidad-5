"""
Pruebas de Seguridad y Autorización (tests/test_security.py)
Comprueba el cumplimiento de las políticas de cancelación de pedidos.
"""
from datetime import datetime, timedelta

from src.security import can_cancel


def test_cannot_cancel_shipped_even_as_admin():
    """Un pedido SHIPPED nunca se cancela, incluso si lo solicita un administrador."""
    now = datetime(2026, 1, 1, 12, 0)
    created = now - timedelta(hours=1)
    assert not can_cancel("SHIPPED", owner="alice", user="admin", is_admin=True, created_at=created, now=now)


def test_owner_can_cancel_within_24_hours():
    """El propietario puede cancelar dentro de las primeras 24 horas."""
    now = datetime(2026, 1, 1, 12, 0)
    created = now - timedelta(hours=2)
    assert can_cancel("CONFIRMED", owner="alice", user="alice", is_admin=False, created_at=created, now=now)


def test_stranger_cannot_cancel():
    """Un usuario ajeno no administrador no puede cancelar."""
    now = datetime(2026, 1, 1, 12, 0)
    created = now - timedelta(hours=2)
    assert not can_cancel("CONFIRMED", owner="alice", user="bob", is_admin=False, created_at=created, now=now)


# =============================================================================
# ACTIVIDADES PARA EL ALUMNO / ANTIGRAVITY (Paso 6 del manual):
# =============================================================================
def test_admin_can_cancel_new_order_of_other_user():
    """Un administrador cancela un pedido NEW de otro usuario (debe permitirse)."""
    now = datetime(2026, 1, 1, 12, 0)
    created = now - timedelta(hours=48)  # Más de 24 horas
    assert can_cancel("NEW", owner="alice", user="admin", is_admin=True, created_at=created, now=now)


def test_owner_cannot_cancel_at_exactly_24_hours():
    """El propietario intenta cancelar exactamente a las 24 horas (debe rechazarse)."""
    now = datetime(2026, 1, 2, 12, 0)
    created = datetime(2026, 1, 1, 12, 0)  # Diferencia exacta de 24 horas
    assert not can_cancel("NEW", owner="alice", user="alice", is_admin=False, created_at=created, now=now)

