from datetime import date as date_type
from apscheduler.schedulers.background import BackgroundScheduler

from app.database import SessionLocal
from app.models import Employee, Attendance


def mark_absentees():
    """
    Runs once daily at 10:00 AM.
    Any active employee with no attendance record for today gets marked absent.
    Employees who already checked in (even late) are left untouched.
    """
    db = SessionLocal()
    try:
        today = date_type.today()

        active_employees = db.query(Employee).filter(Employee.is_active == True).all()
        already_marked_ids = {
            a.employee_id
            for a in db.query(Attendance).filter(Attendance.date == today).all()
        }

        marked_count = 0
        for emp in active_employees:
            if emp.id not in already_marked_ids:
                db.add(Attendance(
                    employee_id=emp.id,
                    date=today,
                    status="absent",
                    check_in_method="manual",
                ))
                marked_count += 1

        db.commit()
        print(f"[scheduler] Marked {marked_count} employee(s) absent for {today}")
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(mark_absentees, "cron", hour=10, minute=0)
    scheduler.start()
    return scheduler