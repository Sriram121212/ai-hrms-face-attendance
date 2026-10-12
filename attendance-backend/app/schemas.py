from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from datetime import datetime, date as date_type


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "employee"
    department: Optional[str] = None
    designation: Optional[str] = None
    join_date: date
    base_salary: float = 0.0
    phone: Optional[str] = None


class EmployeeOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    department: Optional[str]
    designation: Optional[str]
    join_date: date
    base_salary: float

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    employee_id: int
    name: str


class LeaveApply(BaseModel):
    from_date: date_type
    to_date: date_type
    reason: str


class LeaveOut(BaseModel):
    id: int
    employee_id: int
    from_date: date_type
    to_date: date_type
    reason: str
    status: str
    applied_on: datetime
    reviewed_by: Optional[int] = None
    reviewed_on: Optional[datetime] = None

    class Config:
        from_attributes = True
        
        
        
class SalarySlipOut(BaseModel):
    id: int
    employee_id: int
    month: int
    year: int
    base_salary: float
    days_present: int
    days_absent: int
    deduction: float
    net_salary: float
    generated_on: datetime

    class Config:
        from_attributes = True


class SalaryGenerateRequest(BaseModel):
    employee_id: int
    month: int
    year: int
    
    
class FaceCheckinRequest(BaseModel):
    employee_id: int
    
    
class HrPolicyDocOut(BaseModel):
    id: int
    filename: str
    chunk_count: int
    uploaded_on: datetime
    status: str
    class Config:
        from_attributes = True

class HrPolicyQuestion(BaseModel):
    question: str

class HrPolicyAnswer(BaseModel):
    answer: str
    tokens_used: int
    cost_usd: float
    
    
class ChatTypeSummary(BaseModel):
    chat_type: str
    query_count: int
    total_tokens: int
    total_cost: float

class CostSummary(BaseModel):
    total_queries: int
    total_tokens: int
    total_cost: float
    by_type: list[ChatTypeSummary]

class ChatLogOut(BaseModel):
    id: int
    employee_id: int
    employee_name: str
    chat_type: str
    query: str
    tokens_used: int
    cost_usd: float
    created_at: datetime
    class Config:
        from_attributes = True
        
        
class AdminAgentQuestion(BaseModel):
    question: str


class AdminAgentAnswer(BaseModel):
    answer: str
    tokens_used: int
    cost_usd: float