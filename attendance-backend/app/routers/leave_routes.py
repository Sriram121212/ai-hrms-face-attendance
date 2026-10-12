from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Leave, Employee
from app.schemas import LeaveApply, LeaveOut
from app.auth import get_current_user, require_admin

router = APIRouter(tags=["Leave"])


@router.post("/leave/apply", response_model=LeaveOut)
def apply_leave(
    payload: LeaveApply,
    current_user: Employee = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Employee applies for leave - employee_id comes from JWT, not request body."""
    if payload.to_date < payload.from_date:
        raise HTTPException(status_code=400, detail="to_date cannot be before from_date")

    leave = Leave(
        employee_id=current_user.id,
        from_date=payload.from_date,
        to_date=payload.to_date,
        reason=payload.reason,
        status="pending"
    )
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave


@router.get("/leave/my", response_model=List[LeaveOut])
def my_leaves(current_user: Employee = Depends(get_current_user), db: Session = Depends(get_db)):
    """Employee views their own leave history."""
    return db.query(Leave).filter(
        Leave.employee_id == current_user.id
    ).order_by(Leave.applied_on.desc()).all()


@router.get("/admin/leaves", response_model=List[LeaveOut], dependencies=[Depends(require_admin)])
def all_leaves(status_filter: str = None, db: Session = Depends(get_db)):
    """Admin views all leave requests, optionally filtered by status (pending/approved/rejected)."""
    query = db.query(Leave)
    if status_filter:
        query = query.filter(Leave.status == status_filter)
    return query.order_by(Leave.applied_on.desc()).all()


@router.put("/admin/leaves/{leave_id}/approve", response_model=LeaveOut)
def approve_leave(
    leave_id: int,
    current_admin: Employee = Depends(require_admin),
    db: Session = Depends(get_db)
):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if leave.status != "pending":
        raise HTTPException(status_code=400, detail=f"Leave already {leave.status}")

    leave.status = "approved"
    leave.reviewed_by = current_admin.id
    leave.reviewed_on = datetime.now()
    db.commit()
    db.refresh(leave)
    return leave


@router.put("/admin/leaves/{leave_id}/reject", response_model=LeaveOut)
def reject_leave(
    leave_id: int,
    current_admin: Employee = Depends(require_admin),
    db: Session = Depends(get_db)
):
    leave = db.query(Leave).filter(Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    if leave.status != "pending":
        raise HTTPException(status_code=400, detail=f"Leave already {leave.status}")

    leave.status = "rejected"
    leave.reviewed_by = current_admin.id
    leave.reviewed_on = datetime.now()
    db.commit()
    db.refresh(leave)
    return leave