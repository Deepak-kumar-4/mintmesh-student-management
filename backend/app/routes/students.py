from datetime import datetime, UTC
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student
from app.schemas import (
    EnrollmentStatus,
    StudentCreate,
    StudentListResponse,
    StudentOut,
    StudentUpdate,
)

router = APIRouter(prefix="/students", tags=["students"])


@router.post("", response_model=StudentOut, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.email == student.email).first()
    if existing:
        raise HTTPException(
            status_code=409, detail="A student with this email already exists"
        )

    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.get("", response_model=StudentListResponse)
def list_students(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    enrollment_status: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
):
    if enrollment_status is not None:
        valid_statuses = {status.value for status in EnrollmentStatus}
        if enrollment_status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Invalid enrollment_status '{enrollment_status}'. "
                    f"Must be one of: {', '.join(sorted(valid_statuses))}"
                ),
            )

    query = db.query(Student)
    if enrollment_status is not None:
        query = query.filter(Student.enrollment_status == enrollment_status)

    total = query.count()
    skip = (page - 1) * page_size
    items = (
        query.order_by(Student.created_at.desc())
        .offset(skip)
        .limit(page_size)
        .all()
    )

    return StudentListResponse(total=total, page=page, page_size=page_size, items=items)


@router.get("/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.patch("/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int, student_update: StudentUpdate, db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    update_data = student_update.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing = (
            db.query(Student)
            .filter(Student.email == update_data["email"], Student.id != student_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=409, detail="A student with this email already exists"
            )

    for field, value in update_data.items():
        setattr(student, field, value)

    student.updated_at = datetime.now(UTC)

    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}
