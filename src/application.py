"""
Módulo de Aplicación (src/application.py)
Contiene los servicios de aplicación y casos de uso.
"""
from src.domain import Order


class OrderService:
    """
    Servicio de aplicación para coordinar el checkout y cobro de pedidos.
    """

    def __init__(self, gateway):
        self.gateway = gateway

    def checkout(self, order: Order):
        """
        Confirma el pedido y efectúa el cobro en la pasarela externa.

        Observación técnica:
        El código base confirma el pedido antes de saber si el pago fue aceptado;
        esto genera un riesgo de consistencia si la pasarela rechaza la transacción.
        """
        amount = order.confirm()
        if not self.gateway.charge(amount):
            raise RuntimeError("payment rejected")
        return amount

