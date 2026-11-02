"""
Módulo del Dominio de Pedidos (src/domain.py)
Define las reglas de negocio de la entidad Order.
"""


class Order:
    """
    Representa un pedido de compra en el sistema.

    Reglas de negocio base:
    - El importe total debe ser mayor a cero (rechaza totales <= 0).
    - Un cliente con deuda pendiente no puede confirmar el pedido.
    - Clientes VIP reciben un 15% de descuento sobre el total al confirmar.
    - Al confirmarse con éxito, el estado del pedido cambia a 'CONFIRMED'.
    """

    def __init__(
        self,
        total: float,
        vip: bool = False,
        has_debt: bool = False,
        status: str = "NEW",
    ):
        self.total = total
        self.vip = vip
        self.has_debt = has_debt
        self.status = status

    def confirm(self) -> float | int:
        """
        Confirma el pedido aplicando validaciones y descuentos.
        Retorna el importe final a cobrar.
        """
        # =====================================================================
        # PASO 3 (TDD - Fase GREEN):
        # =====================================================================
        if self.status == "CONFIRMED":
            raise ValueError("already confirmed")

        if self.total <= 0:
            raise ValueError("total must be greater than zero")

        if self.has_debt:
            raise ValueError("customer has pending debt")

        # Descuento VIP del 15%
        if self.vip:
            discounted = self.total * 0.85
            # Retornar entero si el valor es entero (ej. 100 * 0.85 = 85)
            final_amount = int(discounted) if isinstance(discounted, float) and discounted.is_integer() else discounted
        else:
            final_amount = self.total

        self.status = "CONFIRMED"
        return final_amount

