"""
Módulo del Dominio PIA - Empresa TechStore / Comercio Electrónico (src/pia_domain.py)
Implementa las 3 reglas de negocio del PIA de la empresa para la transferencia de aprendizaje (Paso 9).

Reglas seleccionadas del PIA:
1. Regla de Inventario / Stock: Control de existencias disponibles para venta.
2. Regla de Límite de Unidades: Máximo 20 unidades permitidas por pedido.
3. Regla de Descuento por Volumen: 5% de descuento en pedidos mayores a $5,000 MXN sin promociones activas.
"""
from dataclasses import dataclass


class BusinessRuleViolation(ValueError):
    """Excepción de dominio cuando se infringe una regla del PIA."""


@dataclass
class Product:
    sku: str
    nombre: str
    precio: float
    stock: int

    def reservar(self, cantidad: int) -> int:
        """
        Regla 1 (Inventario):
        - Valida que la cantidad sea un entero positivo (> 0).
        - Verifica que haya existencias disponibles (stock >= cantidad).
        - Descuenta las unidades del inventario.
        """
        if cantidad <= 0:
            raise BusinessRuleViolation("La cantidad solicitada debe ser mayor a cero")
        if self.stock < cantidad:
            raise BusinessRuleViolation(
                f"Inventario insuficiente para SKU {self.sku}. Stock actual: {self.stock}, solicitado: {cantidad}"
            )
        self.stock -= cantidad
        return self.stock


class TechStoreOrder:
    """
    Entidad de pedido adaptada a las reglas del PIA.
    """

    MAX_UNIDADES_POR_PEDIDO = 20

    def __init__(self, pedido_id: str, cliente_id: str, tiene_promocion: bool = False):
        self.pedido_id = pedido_id
        self.cliente_id = cliente_id
        self.tiene_promocion = tiene_promocion
        self.items: list[dict] = []
        self.estado = "DRAFT"

    @property
    def total_unidades(self) -> int:
        return sum(item["cantidad"] for item in self.items)

    @property
    def subtotal(self) -> float:
        return sum(item["cantidad"] * item["precio_unitario"] for item in self.items)

    def agregar_item(self, sku: str, cantidad: int, precio_unitario: float) -> None:
        """
        Regla 2 (Límite de Unidades):
        - No permite cantidades <= 0.
        - No permite que el acumulado de unidades en el pedido exceda 20 unidades.
        """
        if cantidad <= 0:
            raise BusinessRuleViolation("La cantidad a agregar debe ser mayor a cero")
        if self.total_unidades + cantidad > self.MAX_UNIDADES_POR_PEDIDO:
            raise BusinessRuleViolation(
                f"Límite excedido: El pedido no puede tener más de {self.MAX_UNIDADES_POR_PEDIDO} unidades en total"
            )

        self.items.append({
            "sku": sku,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario
        })

    def calcular_total_con_descuento(self) -> float:
        """
        Regla 3 (Descuento por Volumen):
        - Si el subtotal es estrictamente mayor a $5,000 MXN y NO cuenta con promoción previa,
          recibe un 5% de descuento sobre el total.
        - Si tiene promoción activa, la promoción bloquea el descuento de volumen.
        - Si el subtotal es <= $5,000 MXN, no se otorga descuento de volumen.
        """
        sub = self.subtotal
        if sub > 5000.0 and not self.tiene_promocion:
            return round(sub * 0.95, 2)
        return round(sub, 2)

    def confirmar(self, notificador=None) -> float:
        """
        Confirma el pedido y opcionalmente notifica al cliente mediante un servicio externo.
        """
        if not self.items:
            raise BusinessRuleViolation("No se puede confirmar un pedido sin artículos")

        total = self.calcular_total_con_descuento()
        self.estado = "CONFIRMED"

        if notificador is not None:
            notificador.enviar_confirmacion(self.cliente_id, self.pedido_id, total)

        return total

