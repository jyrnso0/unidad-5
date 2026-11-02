"""
Módulo de Persistencia (src/repository.py)
Gestiona la capa de datos de pedidos utilizando SQLAlchemy.
"""
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OrderRow(Base):
    """Modelo ORM que define la tabla 'orders'."""

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    total = Column(Float, nullable=False)
    status = Column(String(50), nullable=False)

    def __repr__(self) -> str:
        return f"<OrderRow(id={self.id}, total={self.total}, status='{self.status}')>"


class SqlOrderRepository:
    """
    Repositorio SQL para persistencia de pedidos.
    La sesión representa el límite transaccional.
    """

    def __init__(self, session):
        self.session = session

    def save(self, order_row: OrderRow) -> None:
        """Agrega un registro de pedido a la sesión transaccional."""
        self.session.add(order_row)

    def get_by_id(self, order_id: int) -> OrderRow | None:
        """Consulta un pedido por su ID dentro de la sesión actual."""
        return self.session.get(OrderRow, order_id)

