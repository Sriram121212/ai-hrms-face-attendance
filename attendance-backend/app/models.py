from sqlalchemy import (
    Column, Integer, String, DECIMAL, Date, DateTime, Boolean,
    Enum, ForeignKey, Text, TIMESTAMP, func
)
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class RoleEnum(str, enum.Enum):
    admin = "admin"
    employee = "employee"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.employee, nullable=False)
    department = Column(String(100))
    designation = Column(String(100))
    join_date = Column(Date, nullable=False)
    base_salary = Column(DECIMAL(10, 2), default=0.00)
    phone = Column(String(15))
    face_encoding_path = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    attendance_records = relationship("Attendance", back_populates="employee")
    leaves = relationship("Leave", foreign_keys="Leave.employee_id", back_populates="employee")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    check_in_time = Column(DateTime)
    check_out_time = Column(DateTime)
    status = Column(Enum("present", "absent", "half_day", "leave", name="status_enum"), default="absent")
    check_in_method = Column(Enum("face", "manual", name="method_enum"), default="face")
    created_at = Column(TIMESTAMP, server_default=func.now())

    employee = relationship("Employee", back_populates="attendance_records")


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date, nullable=False)
    reason = Column(Text)
    status = Column(Enum("pending", "approved", "rejected", name="leave_status_enum"), default="pending")
    applied_on = Column(TIMESTAMP, server_default=func.now())
    reviewed_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"))
    reviewed_on = Column(TIMESTAMP, nullable=True)

    employee = relationship("Employee", foreign_keys=[employee_id], back_populates="leaves")


class SalarySlip(Base):
    __tablename__ = "salary_slips"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    base_salary = Column(DECIMAL(10, 2), nullable=False)
    days_present = Column(Integer, default=0)
    days_absent = Column(Integer, default=0)
    deduction = Column(DECIMAL(10, 2), default=0.00)
    net_salary = Column(DECIMAL(10, 2), nullable=False)
    generated_on = Column(TIMESTAMP, server_default=func.now())
    
    
class HrPolicyDoc(Base):
    __tablename__ = "hr_policy_docs"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    chunk_count = Column(Integer, default=0)
    uploaded_by = Column(Integer, ForeignKey("employees.id", ondelete="SET NULL"))
    uploaded_on = Column(TIMESTAMP, server_default=func.now())
    status = Column(Enum("processing", "ready", "failed", name="doc_status_enum"), default="processing")


class ChatLog(Base):
    __tablename__ = "chat_logs"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    chat_type = Column(Enum("hr_policy_rag", "admin_agent", name="chat_type_enum"), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(Text)
    tokens_used = Column(Integer, default=0)
    cost_usd = Column(DECIMAL(10, 6), default=0.000000)
    created_at = Column(TIMESTAMP, server_default=func.now())