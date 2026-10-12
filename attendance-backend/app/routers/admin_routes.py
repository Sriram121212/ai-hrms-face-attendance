from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Employee
from app.schemas import EmployeeOut, EmployeeCreate
from app.auth import require_admin, hash_password

router = APIRouter(prefix="/admin", tags=["Admin - Employee Management"])


@router.get("/employees", response_model=List[EmployeeOut], dependencies=[Depends(require_admin)])
def list_employees(db: Session = Depends(get_db)):
    """List all active employees. Admin only."""
    return db.query(Employee).filter(Employee.is_active == True).all()


@router.get("/employees/{employee_id}", response_model=EmployeeOut, dependencies=[Depends(require_admin)])
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/employees/{employee_id}", response_model=EmployeeOut, dependencies=[Depends(require_admin)])
def update_employee(employee_id: int, payload: EmployeeCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.name = payload.name
    employee.email = payload.email
    employee.department = payload.department
    employee.designation = payload.designation
    employee.join_date = payload.join_date
    employee.base_salary = payload.base_salary
    employee.phone = payload.phone
    employee.role = payload.role

    # Only re-hash password if a new one was actually provided
    if payload.password:
        employee.password_hash = hash_password(payload.password)

    db.commit()
    db.refresh(employee)
    return employee


@router.delete("/employees/{employee_id}", dependencies=[Depends(require_admin)])
def deactivate_employee(employee_id: int, db: Session = Depends(get_db)):
    """Soft delete - keeps attendance/leave/salary history intact for records."""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.is_active = False
    db.commit()
    return {"message": f"Employee {employee.name} deactivated"}
