from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import func, ForeignKey, String, Integer, Boolean, FLOAT, DateTime
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

class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    url: Mapped[str] = mapped_column(String(300))
    name: Mapped[str] = mapped_column(String(200))
    check_interval_sec: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class CheckResult(Base):
    __tablename__ = "check_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_service: Mapped[int] = mapped_column(ForeignKey("services.id"))
    status_code: Mapped[int] = mapped_column(Integer)
    response_time_ms: Mapped[float] = mapped_column(FLOAT)
    message: Mapped[str] = mapped_column(String(600))
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))

