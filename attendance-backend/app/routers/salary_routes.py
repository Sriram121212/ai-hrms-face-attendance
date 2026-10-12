import calendar
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import SalarySlip, Employee, Attendance
from app.schemas import SalarySlipOut, SalaryGenerateRequest
from app.auth import get_current_user, require_admin

router = APIRouter(tags=["Salary"])


@router.post("/admin/salary/generate", response_model=SalarySlipOut, dependencies=[Depends(require_admin)])
def generate_salary(payload: SalaryGenerateRequest, db: Session = Depends(get_db)):
    """Admin generates (or regenerates) a salary slip for an employee for a given month/year."""
    employee = db.query(Employee).filter(Employee.id == payload.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Count attendance for that month
    total_days_in_month = calendar.monthrange(payload.year, payload.month)[1]

    # records = db.query(Attendance).filter(
    #     Attendance.employee_id == payload.employee_id,
    #     Attendance.date.op("MONTH")() == payload.month if False else True
    # ).all()
    
    records = db.query(Attendance).filter(
        Attendance.employee_id == payload.employee_id
    ).all()
    
    
    
    # Filter in Python for simplicity (portable across DBs)
    month_records = [
        r for r in records
        if r.date.month == payload.month and r.date.year == payload.year
    ]

    days_present = sum(1 for r in month_records if r.status == "present")
    days_absent = total_days_in_month - days_present

    per_day_salary = float(employee.base_salary) / total_days_in_month
    deduction = round(per_day_salary * days_absent, 2)
    net_salary = round(float(employee.base_salary) - deduction, 2)

    # Update if slip already exists for this month, else create new
    existing = db.query(SalarySlip).filter(
        SalarySlip.employee_id == payload.employee_id,
        SalarySlip.month == payload.month,
        SalarySlip.year == payload.year
    ).first()

    if existing:
        existing.base_salary = employee.base_salary
        existing.days_present = days_present
        existing.days_absent = days_absent
        existing.deduction = deduction
        existing.net_salary = net_salary
        slip = existing
    else:
        slip = SalarySlip(
            employee_id=payload.employee_id,
            month=payload.month,
            year=payload.year,
            base_salary=employee.base_salary,
            days_present=days_present,
            days_absent=days_absent,
            deduction=deduction,
            net_salary=net_salary
        )
        db.add(slip)

    db.commit()
    db.refresh(slip)
    return slip


@router.get("/salary/my", response_model=List[SalarySlipOut])
def my_salary_slips(current_user: Employee = Depends(get_current_user), db: Session = Depends(get_db)):
    """Employee views their own salary slips."""
    return db.query(SalarySlip).filter(
        SalarySlip.employee_id == current_user.id
    ).order_by(SalarySlip.year.desc(), SalarySlip.month.desc()).all()


@router.get("/admin/salary/{employee_id}", response_model=List[SalarySlipOut], dependencies=[Depends(require_admin)])
def employee_salary_slips(employee_id: int, db: Session = Depends(get_db)):
    """Admin views a specific employee's salary slip history."""
    return db.query(SalarySlip).filter(
        SalarySlip.employee_id == employee_id
    ).order_by(SalarySlip.year.desc(), SalarySlip.month.desc()).all()