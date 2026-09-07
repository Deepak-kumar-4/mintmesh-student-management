from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class EnrollmentStatus(str, Enum):
    active = "active"
    graduated = "graduated"
    dropped = "dropped"


def _validate_dob_not_future(value: date) -> date:
    if value >= date.today():
        raise ValueError("date_of_birth must be in the past")
    return value


class StudentCreate(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: EmailStr
    date_of_birth: date
    enrollment_status: EnrollmentStatus

    @field_validator("date_of_birth")
    @classmethod
    def date_of_birth_must_be_in_past(cls, value: date) -> date:
        return _validate_dob_not_future(value)


class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1)
    last_name: Optional[str] = Field(default=None, min_length=1)
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None
    enrollment_status: Optional[EnrollmentStatus] = None

    @field_validator("date_of_birth")
    @classmethod
    def date_of_birth_must_be_in_past(cls, value: Optional[date]) -> Optional[date]:
        if value is None:
            return value
        return _validate_dob_not_future(value)


class StudentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    email: EmailStr
    date_of_birth: date
    enrollment_status: EnrollmentStatus
    created_at: datetime
    updated_at: datetime


class StudentListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list[StudentOut]
