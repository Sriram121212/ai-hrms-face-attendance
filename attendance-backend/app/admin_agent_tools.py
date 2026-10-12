from datetime import date as date_type
from sqlalchemy.orm import Session
from app.models import Employee, Attendance, Leave, SalarySlip


def get_attendance_summary(db: Session, date_str: str = None) -> dict:
    """Present/absent counts and names for a given date (defaults to today)."""
    target_date = date_type.fromisoformat(date_str) if date_str else date_type.today()

    total_employees = db.query(Employee).filter(Employee.is_active == True).count()
    records = db.query(Attendance).filter(Attendance.date == target_date).all()

    present = [r.employee.name for r in records if r.status == "present"]
    present_ids = {r.employee_id for r in records}
    all_employees = db.query(Employee).filter(Employee.is_active == True).all()
    absent = [e.name for e in all_employees if e.id not in present_ids]

    return {
        "date": str(target_date),
        "total_employees": total_employees,
        "present_count": len(present),
        "absent_count": len(absent),
        "present_employees": present,
        "absent_employees": absent,
    }


def get_employee_attendance(db: Session, employee_name: str, date_str: str = None) -> dict:
    """Attendance history for a specific employee, optionally filtered to one date."""
    employee = db.query(Employee).filter(Employee.name.ilike(f"%{employee_name}%")).first()
    if not employee:
        return {"error": f"No employee found matching '{employee_name}'"}

    query = db.query(Attendance).filter(Attendance.employee_id == employee.id)
    if date_str:
        query = query.filter(Attendance.date == date_type.fromisoformat(date_str))

    records = query.order_by(Attendance.date.desc()).limit(30).all()

    return {
        "employee_name": employee.name,
        "records": [
            {
                "date": str(r.date),
                "status": r.status,
                "check_in": r.check_in_time.strftime("%H:%M") if r.check_in_time else None,
                "check_out": r.check_out_time.strftime("%H:%M") if r.check_out_time else None,
            }
            for r in records
        ],
    }


def get_pending_leaves(db: Session) -> dict:
    """All leave requests currently awaiting approval."""
    leaves = db.query(Leave).filter(Leave.status == "pending").all()
    return {
        "pending_count": len(leaves),
        "requests": [
            {
                "employee_name": lv.employee.name,
                "from_date": str(lv.from_date),
                "to_date": str(lv.to_date),
                "reason": lv.reason,
            }
            for lv in leaves
        ],
    }


def get_salary_info(db: Session, employee_name: str, month: int, year: int) -> dict:
    """A specific employee's salary slip for a given month/year."""
    employee = db.query(Employee).filter(Employee.name.ilike(f"%{employee_name}%")).first()
    if not employee:
        return {"error": f"No employee found matching '{employee_name}'"}

    slip = db.query(SalarySlip).filter(
        SalarySlip.employee_id == employee.id,
        SalarySlip.month == month,
        SalarySlip.year == year,
    ).first()

    if not slip:
        return {"error": f"No salary slip found for {employee.name} for {month}/{year}"}

    return {
        "employee_name": employee.name,
        "month": month,
        "year": year,
        "base_salary": float(slip.base_salary),
        "days_present": slip.days_present,
        "days_absent": slip.days_absent,
        "deduction": float(slip.deduction),
        "net_salary": float(slip.net_salary),
    }