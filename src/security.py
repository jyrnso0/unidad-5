"""
Módulo de Seguridad y Autorización (src/security.py)
Implementa la política de cancelación de pedidos.
"""
from datetime import datetime, timedelta


def can_cancel(
    status: str,
    owner: str,
    user: str,
    is_admin: bool,
    created_at: datetime,
    now: datetime | None = None,
) -> bool:
    """
    Determina si un usuario está autorizado para cancelar un pedido.

    Reglas de negocio:
    1. Un pedido 'SHIPPED' nunca se cancela, incluso si quien lo solicita es administrador.
    2. Para los demás estados:
       - Un administrador siempre puede cancelar.
       - Un propietario no administrador solo puede cancelar durante las primeras 24 horas
         (< 24 horas estrictas; a las 24 horas exactas debe rechazarse).
       - Cualquier otro usuario no autorizado recibe denegación (False).
    """
    if now is None:
        now = datetime.now()

    # Regla 1: Pedido enviado jamás se cancela
    if status == "SHIPPED":
        return False

    # Regla 2: Administrador tiene autorización para otros estados
    if is_admin:
        return True

    # Regla 3: Propietario solo dentro de las primeras 24 horas (< 24h)
    if user == owner:
        diff = now - created_at
        return diff < timedelta(hours=24)

    return False

