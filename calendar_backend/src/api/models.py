from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Text,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association Table for Many-to-Many Event <-> Category (if events can belong to multiple categories)
event_category_table = Table(
    "event_category",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)

# Association Table for Many-to-Many Calendar <-> Category
calendar_category_table = Table(
    "calendar_category",
    Base.metadata,
    Column("calendar_id", Integer, ForeignKey("calendars.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    """User of the calendar system."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    hashed_password = Column(String(256), nullable=False)
    is_active = Column(Boolean, default=True)

    # One-to-many: User owns multiple calendars, events, appointments
    calendars = relationship("Calendar", back_populates="owner", cascade="all, delete-orphan")
    events = relationship("Event", back_populates="owner", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="user", cascade="all, delete-orphan")


class Category(Base):
    """Category for organizing calendars and/or events."""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)

    # If you want events and calendars categorized
    events = relationship("Event", secondary=event_category_table, back_populates="categories")
    calendars = relationship("Calendar", secondary=calendar_category_table, back_populates="categories")


class Calendar(Base):
    """Calendar entity, can be owned by user and associated with categories."""
    __tablename__ = "calendars"
    __table_args__ = (
        UniqueConstraint('name', 'owner_id', name="unique_calendar_name_per_user"),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="calendars")
    events = relationship("Event", back_populates="calendar", cascade="all, delete-orphan")
    categories = relationship("Category", secondary=calendar_category_table, back_populates="calendars")


class Event(Base):
    """Event within a calendar."""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    all_day = Column(Boolean, default=False)
    calendar_id = Column(Integer, ForeignKey("calendars.id", ondelete="CASCADE"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    calendar = relationship("Calendar", back_populates="events")
    owner = relationship("User", back_populates="events")
    appointments = relationship("Appointment", back_populates="event", cascade="all, delete-orphan")
    categories = relationship("Category", secondary=event_category_table, back_populates="events")


class Appointment(Base):
    """Appointment for a given event, tied to a user."""
    __tablename__ = "appointments"
    __table_args__ = (
        UniqueConstraint('user_id', 'event_id', name="unique_appointment_per_user_event"),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(32), default="pending")  # e.g. pending, accepted, declined
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="appointments")
    event = relationship("Event", back_populates="appointments")
