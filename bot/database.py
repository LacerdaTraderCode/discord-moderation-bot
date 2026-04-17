"""
Persistência de warns em SQLite.
"""
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

DATABASE_URL = "sqlite:///./bot.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Warning(Base):
    __tablename__ = "warnings"

    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, nullable=False, index=True)
    user_id = Column(BigInteger, nullable=False, index=True)
    moderator_id = Column(BigInteger, nullable=False)
    reason = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


def init_db():
    Base.metadata.create_all(bind=engine)


def add_warning(guild_id: int, user_id: int, moderator_id: int, reason: str) -> Warning:
    """Registra nova advertência."""
    with SessionLocal() as db:
        w = Warning(
            guild_id=guild_id,
            user_id=user_id,
            moderator_id=moderator_id,
            reason=reason,
        )
        db.add(w)
        db.commit()
        db.refresh(w)
        return w


def get_warnings(guild_id: int, user_id: int) -> list:
    """Lista advertências de um usuário em um servidor."""
    with SessionLocal() as db:
        return (
            db.query(Warning)
            .filter(Warning.guild_id == guild_id, Warning.user_id == user_id)
            .order_by(Warning.created_at.desc())
            .all()
        )
