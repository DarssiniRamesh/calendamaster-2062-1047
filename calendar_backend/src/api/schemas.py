from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# -------- Category Schemas --------
class CategoryBase(BaseModel):
    name: str = Field(..., description="The unique name of the category.")

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# -------- User Schemas --------
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="The email address of the user.")
    name: str = Field(..., description="The full name of the user.")

class UserCreate(UserBase):
    password: str = Field(..., description="User password.")

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class UserPublic(User):
    pass


# -------- Calendar Schemas --------
class CalendarBase(BaseModel):
    name: str = Field(..., description="Calendar display name.")
    description: Optional[str] = Field(None, description="Calendar description.")

class CalendarCreate(CalendarBase):
    owner_id: int

class Calendar(CalendarBase):
    id: int
    owner_id: int
    categories: Optional[List[Category]] = []

    class Config:
        orm_mode = True


# -------- Event Schemas --------
class EventBase(BaseModel):
    title: str = Field(..., description="Event title.")
    description: Optional[str] = Field(None, description="Event details.")
    start_time: datetime
    end_time: datetime
    all_day: bool = False

class EventCreate(EventBase):
    calendar_id: int
    owner_id: int
    categories: Optional[List[int]] = []

class Event(EventBase):
    id: int
    calendar_id: int
    owner_id: int
    categories: Optional[List[Category]] = []

    class Config:
        orm_mode = True


# -------- Appointment Schemas --------
class AppointmentBase(BaseModel):
    status: str = Field("pending", description="Appointment status (pending/accepted/declined).")
    notes: Optional[str] = Field(None, description="Optional notes for the appointment.")

class AppointmentCreate(AppointmentBase):
    user_id: int
    event_id: int

class Appointment(AppointmentBase):
    id: int
    user_id: int
    event_id: int

    class Config:
        orm_mode = True
