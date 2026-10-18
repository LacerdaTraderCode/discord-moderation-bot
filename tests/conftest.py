"""Shared fixtures: an in-memory SQLite database instead of the bot.db file."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from bot import database


@pytest.fixture
def engine(monkeypatch):
    """Replace the module-level engine and session factory with in-memory ones."""
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    monkeypatch.setattr(database, "engine", test_engine)
    monkeypatch.setattr(database, "SessionLocal", sessionmaker(bind=test_engine))
    yield test_engine
    test_engine.dispose()


@pytest.fixture
def db(engine):
    """The database module, with its tables created on the in-memory engine."""
    database.init_db()
    return database
