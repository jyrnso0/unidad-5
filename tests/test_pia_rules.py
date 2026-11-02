"""
Pruebas de Transferencia al Dominio del PIA (tests/test_pia_rules.py)
Implementa la suite de 9 casos de prueba (CP-01 a CP-09) para las 3 reglas de negocio del PIA,
más pruebas de integración/persistencia y simulación de servicios externos con mocks.
"""
from unittest.mock import Mock

import pytest

from src.pia_domain import BusinessRuleViolation, Product, TechStoreOrder

# =============================================================================
# REGLA 1 DEL PIA: Control de Existencias e Inventario
# =============================================================================

def test_cp01_stock_cero_rechazo():
    """CP-01 (Límite/Error): Rechazar venta cuando el stock disponible es cero."""
    producto = Product(sku="SKU-001", nombre="Mouse USB", precio=250.0, stock=0)
    with pytest.raises(BusinessRuleViolation, match="Inventario insuficiente"):
        producto.reservar(1)


def test_cp02_stock_suficiente_reserva():
    """CP-02 (Éxito): Reservar producto con existencias suficientes y actualizar stock."""
    producto = Product(sku="SKU-002", nombre="Teclado Gamer", precio=750.0, stock=5)
    stock_restante = producto.reservar(2)
    assert stock_restante == 3
    assert producto.stock == 3


def test_cp03_cantidad_invalida():
    """CP-03 (Error): Lanzar excepción cuando se solicita una cantidad no positiva (<= 0)."""
    producto = Product(sku="SKU-003", nombre="Monitor 27", precio=3500.0, stock=10)
    with pytest.raises(BusinessRuleViolation, match="mayor a cero"):
        producto.reservar(-1)


# =============================================================================
# REGLA 2 DEL PIA: Límite de Unidades por Pedido (Máximo 20)
# =============================================================================

def test_cp04_unidades_dentro_limite():
    """CP-04 (Éxito): Agregar artículos dentro del límite permitido de 20 unidades."""
    pedido = TechStoreOrder(pedido_id="P-101", cliente_id="CLI-01")
    pedido.agregar_item(sku="SKU-001", cantidad=15, precio_unitario=100.0)
    assert pedido.total_unidades == 15
    assert pedido.subtotal == 1500.0


def test_cp05_limite_exacto_20_unidades():
    """CP-05 (Límite): Permitir exactamente 20 unidades acumuladas en el pedido."""
    pedido = TechStoreOrder(pedido_id="P-102", cliente_id="CLI-02")
    pedido.agregar_item(sku="SKU-001", cantidad=12, precio_unitario=50.0)
    pedido.agregar_item(sku="SKU-002", cantidad=8, precio_unitario=50.0)
    assert pedido.total_unidades == 20
    assert pedido.subtotal == 1000.0


def test_cp06_exceso_unidades_rechazo():
    """CP-06 (Error): Rechazar operación si el pedido supera las 20 unidades."""
    pedido = TechStoreOrder(pedido_id="P-103", cliente_id="CLI-03")
    pedido.agregar_item(sku="SKU-001", cantidad=15, precio_unitario=100.0)
    with pytest.raises(BusinessRuleViolation, match="Límite excedido"):
        pedido.agregar_item(sku="SKU-002", cantidad=6, precio_unitario=100.0)


# =============================================================================
# REGLA 3 DEL PIA: Descuento por Volumen (> $5,000 MXN) y Promociones
# =============================================================================

def test_cp07_descuento_volumen_aplicado():
    """CP-07 (Éxito): Aplicar 5% de descuento en pedidos mayores a $5,000 sin promoción previa."""
    pedido = TechStoreOrder(pedido_id="P-104", cliente_id="CLI-04", tiene_promocion=False)
    # 2 artículos de $3,000 c/u = $6,000 de subtotal. Con 5% de descuento = $5,700
    pedido.agregar_item(sku="SKU-LAP", cantidad=2, precio_unitario=3000.0)
    assert pedido.subtotal == 6000.0
    assert pedido.calcular_total_con_descuento() == 5700.0


def test_cp08_umbral_limite_sin_descuento():
    """CP-08 (Límite): Pedido de exactamente $5,000 no recibe descuento por no superar el umbral estricto."""
    pedido = TechStoreOrder(pedido_id="P-105", cliente_id="CLI-05", tiene_promocion=False)
    pedido.agregar_item(sku="SKU-TAB", cantidad=5, precio_unitario=1000.0)
    assert pedido.subtotal == 5000.0
    assert pedido.calcular_total_con_descuento() == 5000.0


def test_cp09_promocion_activa_bloquea_descuento():
    """CP-09 (Error/Regla): Una promoción activa bloquea el descuento de volumen acumulativo."""
    pedido = TechStoreOrder(pedido_id="P-106", cliente_id="CLI-06", tiene_promocion=True)
    pedido.agregar_item(sku="SKU-LAP", cantidad=2, precio_unitario=3000.0)
    assert pedido.subtotal == 6000.0
    # No recibe el 5% de descuento adicional, conserva el subtotal
    assert pedido.calcular_total_con_descuento() == 6000.0


# =============================================================================
# PRUEBAS ADICIONALES: Persistencia y Mocks del PIA (Requisito Paso 9)
# =============================================================================

def test_pia_mock_servicio_notificaciones():
    """Verifica con Mock la invocación al servicio externo de notificaciones al confirmar."""
    notificador_mock = Mock()
    pedido = TechStoreOrder(pedido_id="P-107", cliente_id="CLI-07")
    pedido.agregar_item(sku="SKU-001", cantidad=2, precio_unitario=500.0)

    total_confirmado = pedido.confirmar(notificador=notificador_mock)

    assert total_confirmado == 1000.0
    assert pedido.estado == "CONFIRMED"
    notificador_mock.enviar_confirmacion.assert_called_once_with("CLI-07", "P-107", 1000.0)


def test_cp12_mock_notificacion_confirma_descuento_volumen():
    """CP-12 (Éxito): Confirma por Mock el total con descuento de volumen aplicado."""
    notificador_mock = Mock()
    pedido = TechStoreOrder(pedido_id="P-108", cliente_id="CLI-08")
    pedido.agregar_item(sku="SKU-LAP", cantidad=2, precio_unitario=3000.0)

    total_confirmado = pedido.confirmar(notificador=notificador_mock)

    assert total_confirmado == 5700.0
    assert pedido.estado == "CONFIRMED"
    notificador_mock.enviar_confirmacion.assert_called_once_with("CLI-08", "P-108", 5700.0)
