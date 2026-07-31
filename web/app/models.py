from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import func, ForeignKey, String, Integer, Boolean, FLOAT, DATETIME
from datetime import datetime

class Base(db.Model):
    __abstract__ = True
    ceated_at: Mapped[datetime] = mapped_column(server_default=func.now())

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    f_name: Mapped[str] = mapped_column(String(100))
    l_name: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(120),unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

