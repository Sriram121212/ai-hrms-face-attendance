from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Employee, ChatLog
from app.schemas import AdminAgentQuestion, AdminAgentAnswer
from app.auth import require_admin
from app.admin_agent import run_admin_agent

router = APIRouter(tags=["Admin AI Agent"])


@router.post("/admin/agent/ask", response_model=AdminAgentAnswer, dependencies=[Depends(require_admin)])
def ask_admin_agent(
    payload: AdminAgentQuestion,
    current_admin: Employee = Depends(require_admin),
    db: Session = Depends(get_db),
):
    result = run_admin_agent(payload.question, db)

    log = ChatLog(
        employee_id=current_admin.id,
        chat_type="admin_agent",
        query=payload.question,
        response=result["answer"],
        tokens_used=result["tokens_used"],
        cost_usd=result["cost_usd"],
    )
    db.add(log)
    db.commit()

    return AdminAgentAnswer(answer=result["answer"], tokens_used=result["tokens_used"], cost_usd=result["cost_usd"])