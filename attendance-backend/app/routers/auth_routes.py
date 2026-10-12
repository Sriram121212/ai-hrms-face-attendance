from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee
from app.schemas import LoginRequest, Token, EmployeeCreate, EmployeeOut
from app.auth import verify_password, create_access_token, hash_password, require_admin

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Employee).filter(Employee.email == payload.email).first()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    token = create_access_token({"employee_id": user.id, "role": user.role.value})

    return Token(
        access_token=token,
        role=user.role.value,
        employee_id=user.id,
        name=user.name,
    )


@router.post("/register", response_model=EmployeeOut, dependencies=[Depends(require_admin)])
def register_employee(payload: EmployeeCreate, db: Session = Depends(get_db)):
    """Only an admin can create new employee/admin accounts."""
    existing = db.query(Employee).filter(Employee.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_employee = Employee(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        department=payload.department,
        designation=payload.designation,
        join_date=payload.join_date,
        base_salary=payload.base_salary,
        phone=payload.phone,
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee
