from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class EnrollmentStatus(str, Enum):
    active = "active"
    graduated = "graduated"
    dropped = "dropped"


class StudentCreate(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    email: EmailStr
    date_of_birth: date
    enrollment_status: EnrollmentStatus

    @field_validator("date_of_birth")
    @classmethod
    def date_of_birth_must_be_in_past(cls, value: date) -> date:
        if value >= date.today():
            raise ValueError("date_of_birth must be in the past")
        return value


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
