"""
Pruebas de Integración y Persistencia (tests/test_repository.py)
Verifica la persistencia con SQLAlchemy y el comportamiento transaccional (commit/rollback).
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.repository import Base, OrderRow, SqlOrderRepository


@pytest.fixture
def session():
    """Fixture que crea un motor SQLite en memoria y sesión transaccional."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


def test_repository_commit(session):
    """Verifica que el repositorio almacena un pedido y session.commit lo hace persistente."""
    repo = SqlOrderRepository(session)
    order = OrderRow(id=1, total=120.0, status="CONFIRMED")
    repo.save(order)
    session.commit()

    saved = repo.get_by_id(1)
    assert saved is not None
    assert saved.id == 1
    assert saved.total == 120.0
    assert saved.status == "CONFIRMED"


def test_repository_rollback(session):
    """Verifica que session.rollback descarta la transacción no confirmada."""
    repo = SqlOrderRepository(session)
    order = OrderRow(id=1, total=120.0, status="CONFIRMED")
    repo.save(order)
    session.rollback()

    saved = repo.get_by_id(1)
    assert saved is None


# =============================================================================
# ACTIVIDAD PARA EL ALUMNO / ANTIGRAVITY (Paso 4 del manual):
# =============================================================================
def test_repository_save_order_250_commit(session):
    """
    Actividad Paso 4: Guarda un pedido de total 250 con id=2,
    hace commit y verifica id, total y estado.
    """
    repo = SqlOrderRepository(session)
    order = OrderRow(id=2, total=250.0, status="CONFIRMED")
    repo.save(order)
    session.commit()

    saved = repo.get_by_id(2)
    assert saved is not None
    assert saved.id == 2
    assert saved.total == 250.0
    assert saved.status == "CONFIRMED"

