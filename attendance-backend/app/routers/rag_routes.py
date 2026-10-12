# import os
# import shutil
# from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
# from sqlalchemy.orm import Session

# from app.database import get_db
# from app.models import HrPolicyDoc, ChatLog, Employee
# from app.schemas import HrPolicyDocOut, HrPolicyQuestion, HrPolicyAnswer
# from app.auth import require_admin, get_current_user
# from app.rag_utils import extract_text_from_pdf, chunk_text, store_chunks, delete_doc_chunks, retrieve_relevant_chunks
# from app.groq_client import answer_from_context
# from app.cache import get_cached_answer, set_cached_answer

# router = APIRouter(tags=["HR Policy RAG"])

# UPLOAD_DIR = "uploaded_policies"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


# @router.post("/admin/hr-policy/upload", response_model=HrPolicyDocOut, dependencies=[Depends(require_admin)])
# async def upload_hr_policy(
#     file: UploadFile = File(...),
#     current_admin: Employee = Depends(require_admin),
#     db: Session = Depends(get_db),
# ):
#     """
#     One-time upload. Chunks + embeddings are persisted in ChromaDB on disk,
#     so this does NOT need to be repeated unless the policy document changes.
#     """
#     if not file.filename.lower().endswith(".pdf"):
#         raise HTTPException(status_code=400, detail="Only PDF files are supported")

#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     doc = HrPolicyDoc(
#         filename=file.filename,
#         file_path=file_path,
#         uploaded_by=current_admin.id,
#         status="processing",
#     )
#     db.add(doc)
#     db.commit()
#     db.refresh(doc)

#     try:
#         text = extract_text_from_pdf(file_path)
#         chunks = chunk_text(text)
#         chunk_count = store_chunks(chunks, doc_id=doc.id, filename=file.filename)

#         doc.chunk_count = chunk_count
#         doc.status = "ready"
#         db.commit()
#         db.refresh(doc)
#     except Exception as e:
#         doc.status = "failed"
#         db.commit()
#         raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

#     return doc


# @router.get("/admin/hr-policy/docs", response_model=list[HrPolicyDocOut], dependencies=[Depends(require_admin)])
# def list_hr_policy_docs(db: Session = Depends(get_db)):
#     """Shows what's already uploaded and ready - check this before re-uploading anything."""
#     return db.query(HrPolicyDoc).order_by(HrPolicyDoc.uploaded_on.desc()).all()


# @router.delete("/admin/hr-policy/docs/{doc_id}", dependencies=[Depends(require_admin)])
# def delete_hr_policy_doc(doc_id: int, db: Session = Depends(get_db)):
#     """Use this before re-uploading a new version of the same policy."""
#     doc = db.query(HrPolicyDoc).filter(HrPolicyDoc.id == doc_id).first()
#     if not doc:
#         raise HTTPException(status_code=404, detail="Document not found")

#     delete_doc_chunks(doc_id)
#     if os.path.exists(doc.file_path):
#         os.remove(doc.file_path)
#     db.delete(doc)
#     db.commit()
#     return {"message": f"{doc.filename} removed"}


# @router.post("/hr-policy/ask", response_model=HrPolicyAnswer)
# def ask_hr_policy(
#     payload: HrPolicyQuestion,
#     current_user: Employee = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     """Available to both admin and employee - retrieves relevant chunks, asks Groq, logs cost."""
#     chunks = retrieve_relevant_chunks(payload.question)
#     result = answer_from_context(payload.question, chunks)

#     log = ChatLog(
#         employee_id=current_user.id,
#         chat_type="hr_policy_rag",
#         query=payload.question,
#         response=result["answer"],
#         tokens_used=result["tokens_used"],
#         cost_usd=result["cost_usd"],
#     )
#     # db.add(log)
#     # db.commit()

#     return HrPolicyAnswer(
#         answer=result["answer"],
#         tokens_used=result["tokens_used"],
#         cost_usd=result["cost_usd"],
#     )




# @router.post("/hr-policy/ask", response_model=HrPolicyAnswer)
# def ask_hr_policy(
#     payload: HrPolicyQuestion,
#     current_user: Employee = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     cached = get_cached_answer(payload.question)
#     if cached:
#         log = ChatLog(
#             employee_id=current_user.id,
#             chat_type="hr_policy_rag",
#             query=payload.question,
#             response=cached["answer"],
#             tokens_used=0,
#             cost_usd=0.0,
#         )
#         db.add(log)
#         # db.commit()
#         return HrPolicyAnswer(**cached)

#     chunks = retrieve_relevant_chunks(payload.question)
#     result = answer_from_context(payload.question, chunks)
#     set_cached_answer(payload.question, result)

#     log = ChatLog(
#         employee_id=current_user.id,
#         chat_type="hr_policy_rag",
#         query=payload.question,
#         response=result["answer"],
#         tokens_used=result["tokens_used"],
#         cost_usd=result["cost_usd"],
#     )
#     db.add(log)
#     db.commit()

#     return HrPolicyAnswer(
#         answer=result["answer"],
#         tokens_used=result["tokens_used"],
#         cost_usd=result["cost_usd"],
#     )



import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import HrPolicyDoc, ChatLog, Employee
from app.schemas import HrPolicyDocOut, HrPolicyQuestion, HrPolicyAnswer
from app.auth import require_admin, get_current_user
from app.rag_utils import extract_text_from_pdf, chunk_text, store_chunks, delete_doc_chunks, retrieve_relevant_chunks
from app.groq_client import answer_from_context
from app.cache import get_cached_answer, set_cached_answer

router = APIRouter(tags=["HR Policy RAG"])

UPLOAD_DIR = "uploaded_policies"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/admin/hr-policy/upload", response_model=HrPolicyDocOut, dependencies=[Depends(require_admin)])
async def upload_hr_policy(
    file: UploadFile = File(...),
    current_admin: Employee = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """
    One-time upload. Chunks + embeddings are persisted in ChromaDB on disk,
    so this does NOT need to be repeated unless the policy document changes.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    doc = HrPolicyDoc(
        filename=file.filename,
        file_path=file_path,
        uploaded_by=current_admin.id,
        status="processing",
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    try:
        text = extract_text_from_pdf(file_path)
        chunks = chunk_text(text)
        chunk_count = store_chunks(chunks, doc_id=doc.id, filename=file.filename)

        doc.chunk_count = chunk_count
        doc.status = "ready"
        db.commit()
        db.refresh(doc)
    except Exception as e:
        doc.status = "failed"
        db.commit()
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    return doc


@router.get("/admin/hr-policy/docs", response_model=list[HrPolicyDocOut], dependencies=[Depends(require_admin)])
def list_hr_policy_docs(db: Session = Depends(get_db)):
    """Shows what's already uploaded and ready - check this before re-uploading anything."""
    return db.query(HrPolicyDoc).order_by(HrPolicyDoc.uploaded_on.desc()).all()


@router.delete("/admin/hr-policy/docs/{doc_id}", dependencies=[Depends(require_admin)])
def delete_hr_policy_doc(doc_id: int, db: Session = Depends(get_db)):
    """Use this before re-uploading a new version of the same policy."""
    doc = db.query(HrPolicyDoc).filter(HrPolicyDoc.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    delete_doc_chunks(doc_id)
    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)
    db.delete(doc)
    db.commit()
    return {"message": f"{doc.filename} removed"}


@router.post("/hr-policy/ask", response_model=HrPolicyAnswer)
def ask_hr_policy(
    payload: HrPolicyQuestion,
    current_user: Employee = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Available to both admin and employee - checks cache first, else retrieves chunks + asks Groq."""
    cached = get_cached_answer(payload.question)
    if cached:
        log = ChatLog(
            employee_id=current_user.id,
            chat_type="hr_policy_rag",
            query=payload.question,
            response=cached["answer"],
            tokens_used=0,
            cost_usd=0.0,
        )
        db.add(log)
        db.commit()
        return HrPolicyAnswer(**cached)

    chunks = retrieve_relevant_chunks(payload.question)
    result = answer_from_context(payload.question, chunks)
    set_cached_answer(payload.question, result)

    log = ChatLog(
        employee_id=current_user.id,
        chat_type="hr_policy_rag",
        query=payload.question,
        response=result["answer"],
        tokens_used=result["tokens_used"],
        cost_usd=result["cost_usd"],
    )
    db.add(log)
    db.commit()

    return HrPolicyAnswer(
        answer=result["answer"],
        tokens_used=result["tokens_used"],
        cost_usd=result["cost_usd"],
    )