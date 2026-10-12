from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import ChatLog, Employee
from app.schemas import CostSummary, ChatTypeSummary, ChatLogOut
from app.auth import require_admin

router = APIRouter(tags=["Cost Tracker"])


@router.get("/admin/cost-tracker/summary", response_model=CostSummary, dependencies=[Depends(require_admin)])
def cost_summary(db: Session = Depends(get_db)):
    rows = (
        db.query(
            ChatLog.chat_type,
            func.count(ChatLog.id).label("query_count"),
            func.sum(ChatLog.tokens_used).label("total_tokens"),
            func.sum(ChatLog.cost_usd).label("total_cost"),
        )
        .group_by(ChatLog.chat_type)
        .all()
    )

    by_type = [
        ChatTypeSummary(
            chat_type=r.chat_type,
            query_count=r.query_count,
            total_tokens=int(r.total_tokens or 0),
            total_cost=float(r.total_cost or 0),
        )
        for r in rows
    ]

    return CostSummary(
        total_queries=sum(t.query_count for t in by_type),
        total_tokens=sum(t.total_tokens for t in by_type),
        total_cost=round(sum(t.total_cost for t in by_type), 6),
        by_type=by_type,
    )


@router.get("/admin/cost-tracker/logs", response_model=List[ChatLogOut], dependencies=[Depends(require_admin)])
def recent_chat_logs(limit: int = 30, db: Session = Depends(get_db)):
    logs = (
        db.query(ChatLog, Employee.name)
        .join(Employee, Employee.id == ChatLog.employee_id)
        .order_by(ChatLog.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        ChatLogOut(
            id=log.id, employee_id=log.employee_id, employee_name=name,
            chat_type=log.chat_type, query=log.query, tokens_used=log.tokens_used,
            cost_usd=float(log.cost_usd), created_at=log.created_at,
        )
        for log, name in logs
    ]