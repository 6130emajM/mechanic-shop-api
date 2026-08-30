from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column # type: ignore
from typing import List
from datetime import date

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

mechanic_service_ticket = db.Table(
    'service_mechanics',
    Base.metadata,
    db.Column("ticket_id", db.ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", db.ForeignKey("mechanics.id"))
)

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(100), nullable=False)
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(back_populates='customer')

class Mechanic(Base):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    email: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(db.String(150), unique=True, nullable=False)
    salary: Mapped[float] = mapped_column(db.Float(), nullable=False)
    service_tickets: Mapped[List['ServiceTicket']] = db.relationship(secondary=mechanic_service_ticket, back_populates='mechanics')

class ServiceTicket(Base):
    __tablename__ = "service_tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(17), nullable=False)
    description: Mapped[str] = mapped_column(db.String(300), nullable=False)
    service_date: Mapped[date]
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"), nullable=False)
    customer: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    mechanics: Mapped[List['Mechanic']] = db.relationship(secondary=mechanic_service_ticket, back_populates='service_tickets')
