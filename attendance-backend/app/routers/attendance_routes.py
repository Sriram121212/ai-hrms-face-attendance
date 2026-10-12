# from datetime import date as date_type, datetime
# from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
# from typing import Optional

# from app.database import get_db
# from app.models import Attendance, Employee
# from app.auth import get_current_user, require_admin

# router = APIRouter(tags=["Attendance"])

# CHECK_IN_CUTOFF = time_type(10, 0)  # 10:00 AM


# # @router.post("/attendance/checkin")
# # def check_in(current_user: Employee = Depends(get_current_user), db: Session = Depends(get_db)):
# #     """Employee checks in using their own token - employee_id comes from JWT, not request body."""
# #     today = date_type.today()

# #     existing = db.query(Attendance).filter(
# #         Attendance.employee_id == current_user.id,
# #         Attendance.date == today
# #     ).first()

# #     if existing and existing.check_in_time:
# #         raise HTTPException(status_code=400, detail="Already checked in today")

# #     if existing:
# #         existing.check_in_time = datetime.now()
# #         existing.status = "present"
# #     else:
# #         existing = Attendance(
# #             employee_id=current_user.id,
# #             date=today,
# #             check_in_time=datetime.now(),
# #             status="present",
# #             check_in_method="face"
# #         )
# #         db.add(existing)

# #     db.commit()
# #     db.refresh(existing)
# #     return {"message": "Checked in successfully", "check_in_time": existing.check_in_time}


# from datetime import date as date_type, datetime, time as time_type
# from fastapi import APIRouter, Depends, HTTPException, Query
# from sqlalchemy.orm import Session
# from typing import Optional

# from app.database import get_db
# from app.models import Attendance, Employee
# from app.auth import get_current_user, require_admin

# from datetime import date as date_type, datetime

# router = APIRouter(tags=["Attendance"])

# CHECK_IN_CUTOFF = time_type(10, 0)  # 10:00 AM


# @router.post("/attendance/checkin")
# def check_in(current_user: Employee = Depends(get_current_user), db: Session = Depends(get_db)):
#     today = date_type.today()
#     now = datetime.now()

#     existing = db.query(Attendance).filter(
#         Attendance.employee_id == current_user.id,
#         Attendance.date == today
#     ).first()

#     if existing and existing.check_in_time:
#         raise HTTPException(status_code=400, detail="Already checked in today")

#     # Block check-in after the cutoff if not already checked in
#     if now.time() > CHECK_IN_CUTOFF:
#         raise HTTPException(
#             status_code=400,
#             detail="Check-in window has closed for today (cutoff: 10:00 AM). Contact your admin if this is an error."
#         )

#     if existing:
#         existing.check_in_time = now
#         existing.status = "present"
#     else:
#         existing = Attendance(
#             employee_id=current_user.id,
#             date=today,
#             check_in_time=now,
#             status="present",
#             check_in_method="manual"
#         )
#         db.add(existing)

#     db.commit()
#     db.refresh(existing)
#     return {"message": "Checked in successfully", "check_in_time": existing.check_in_time}




# @router.post("/attendance/checkout")
# def check_out(current_user: Employee = Depends(get_current_user), db: Session = Depends(get_db)):
#     today = date_type.today()

#     record = db.query(Attendance).filter(
#         Attendance.employee_id == current_user.id,
#         Attendance.date == today
#     ).first()

#     if not record or not record.check_in_time:
#         raise HTTPException(status_code=400, detail="You haven't checked in today")

#     if record.check_out_time:
#         raise HTTPException(status_code=400, detail="Already checked out today")

#     record.check_out_time = datetime.now()
#     db.commit()
#     db.refresh(record)
#     return {"message": "Checked out successfully", "check_out_time": record.check_out_time}


# @router.get("/attendance/my")
# def my_attendance(current_user: Employee = Depends(get_current_user), db: Session = Depends(get_db)):
#     """Employee views their own attendance history."""
#     records = db.query(Attendance).filter(
#         Attendance.employee_id == current_user.id
#     ).order_by(Attendance.date.desc()).all()
#     return records


# @router.get("/admin/attendance", dependencies=[Depends(require_admin)])
# def all_attendance(
#     date_filter: Optional[date_type] = Query(None, alias="date"),
#     db: Session = Depends(get_db)
# ):
#     """Admin views everyone's attendance, optionally filtered by date."""
#     query = db.query(Attendance)
#     if date_filter:
#         query = query.filter(Attendance.date == date_filter)
#     return query.order_by(Attendance.date.desc()).all()


# @router.get("/admin/attendance/{employee_id}", dependencies=[Depends(require_admin)])
# def employee_attendance(employee_id: int, db: Session = Depends(get_db)):
#     """Admin views a specific employee's attendance history."""
#     records = db.query(Attendance).filter(
#         Attendance.employee_id == employee_id
#     ).order_by(Attendance.date.desc()).all()

#     if not records:
#         raise HTTPException(status_code=404, detail="No attendance records found")
#     return records



from datetime import date as date_type, datetime, time as time_type
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models import Attendance, Employee
from app.auth import get_current_user, require_admin

router = APIRouter(tags=["Attendance"])

CHECK_IN_CUTOFF = time_type(10, 0)  # 10:00 AM


@router.post("/attendance/checkin")
def check_in(current_user: Employee = Depends(get_current_user), db: Session = Depends(get_db)):
    today = date_type.today()
    now = datetime.now()

    existing = db.query(Attendance).filter(
        Attendance.employee_id == current_user.id,
        Attendance.date == today
    ).first()

    if existing and existing.check_in_time:
        raise HTTPException(status_code=400, detail="Already checked in today")

    # Block check-in after the cutoff if not already checked in
    if now.time() > CHECK_IN_CUTOFF:
        raise HTTPException(
            status_code=400,
            detail="Check-in window has closed for today (cutoff: 10:00 AM). Contact your admin if this is an error."
        )

    if existing:
        existing.check_in_time = now
        existing.status = "present"
    else:
        existing = Attendance(
            employee_id=current_user.id,
            date=today,
            check_in_time=now,
            status="present",
            check_in_method="manual"
        )
        db.add(existing)

    db.commit()
    db.refresh(existing)
    return {"message": "Checked in successfully", "check_in_time": existing.check_in_time}


@router.post("/attendance/checkout")
def check_out(current_user: Employee = Depends(get_current_user), db: Session = Depends(get_db)):
    today = date_type.today()

    record = db.query(Attendance).filter(
        Attendance.employee_id == current_user.id,
        Attendance.date == today
    ).first()

    if not record or not record.check_in_time:
        raise HTTPException(status_code=400, detail="You haven't checked in today")

    if record.check_out_time:
        raise HTTPException(status_code=400, detail="Already checked out today")

    record.check_out_time = datetime.now()
    db.commit()
    db.refresh(record)
    return {"message": "Checked out successfully", "check_out_time": record.check_out_time}


@router.get("/attendance/my")
def my_attendance(current_user: Employee = Depends(get_current_user), db: Session = Depends(get_db)):
    """Employee views their own attendance history."""
    records = db.query(Attendance).filter(
        Attendance.employee_id == current_user.id
    ).order_by(Attendance.date.desc()).all()
    return records


@router.get("/admin/attendance", dependencies=[Depends(require_admin)])
def all_attendance(
    date_filter: Optional[date_type] = Query(None, alias="date"),
    db: Session = Depends(get_db)
):
    """Admin views everyone's attendance, optionally filtered by date."""
    query = db.query(Attendance)
    if date_filter:
        query = query.filter(Attendance.date == date_filter)
    return query.order_by(Attendance.date.desc()).all()


@router.get("/admin/attendance/{employee_id}", dependencies=[Depends(require_admin)])
def employee_attendance(employee_id: int, db: Session = Depends(get_db)):
    """Admin views a specific employee's attendance history."""
    records = db.query(Attendance).filter(
        Attendance.employee_id == employee_id
    ).order_by(Attendance.date.desc()).all()

    if not records:
        raise HTTPException(status_code=404, detail="No attendance records found")
    return records