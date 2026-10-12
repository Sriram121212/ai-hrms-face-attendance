from datetime import date as date_type, datetime
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Attendance, Employee
from app.schemas import FaceCheckinRequest
from app.config import DEVICE_API_KEY

router = APIRouter(tags=["Face Attendance"])


def verify_device_key(x_device_key: str = Header(...)):
    """Raspberry Pi / kiosk sends this header instead of an employee JWT."""
    if x_device_key != DEVICE_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid device key")


@router.post("/attendance/face-checkin", dependencies=[Depends(verify_device_key)])
def face_check_in(payload: FaceCheckinRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == payload.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    today = date_type.today()
    existing = db.query(Attendance).filter(
        Attendance.employee_id == employee.id,
        Attendance.date == today
    ).first()

    if existing and existing.check_in_time:
        raise HTTPException(status_code=400, detail=f"{employee.name} already checked in today")

    if existing:
        existing.check_in_time = datetime.now()
        existing.status = "present"
    else:
        existing = Attendance(
            employee_id=employee.id,
            date=today,
            check_in_time=datetime.now(),
            status="present",
            check_in_method="face"
        )
        db.add(existing)

    db.commit()
    db.refresh(existing)
    return {
        "message": "Checked in successfully",
        "employee_name": employee.name,
        "check_in_time": existing.check_in_time
    }


@router.post("/attendance/face-checkout", dependencies=[Depends(verify_device_key)])
def face_check_out(payload: FaceCheckinRequest, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == payload.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    today = date_type.today()
    record = db.query(Attendance).filter(
        Attendance.employee_id == employee.id,
        Attendance.date == today
    ).first()

    if not record or not record.check_in_time:
        raise HTTPException(status_code=400, detail=f"{employee.name} hasn't checked in today")
    if record.check_out_time:
        raise HTTPException(status_code=400, detail=f"{employee.name} already checked out today")

    record.check_out_time = datetime.now()
    db.commit()
    db.refresh(record)
    return {
        "message": "Checked out successfully",
        "employee_name": employee.name,
        "check_out_time": record.check_out_time
    }