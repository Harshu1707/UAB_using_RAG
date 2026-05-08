from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.security import (
    create_access_token,
    get_current_user,
    hash_password,
    require_admin,
    verify_password,
)
from app.core.config import get_settings
from app.db.session import get_db
from app.models.models import UploadedPDF, User
from app.rag.rag_service import rag_service
from app.schemas.schemas import (
    ChatRequest,
    ChatResponse,
    StudentRead,
    Token,
    UserCreate,
    UserRead,
    WebSearchRequest,
)
from app.services import analytics_service as analytics
from app.services.chat_service import handle_chat
from app.services.search_service import web_search

router = APIRouter()


@router.post("/auth/register", response_model=Token)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if payload.role not in {"student", "admin"}:
        raise HTTPException(400, "Invalid role")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, "Email already registered")

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        role=payload.role,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"access_token": create_access_token(user.email), "user": user}


@router.post("/auth/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Incorrect email or password")
    return {"access_token": create_access_token(user.email), "user": user}


@router.get("/auth/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)):
    return user


@router.post("/chat", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await handle_chat(db, user, payload.message)


@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")

    settings = get_settings()
    Path(settings.upload_dir).mkdir(exist_ok=True)
    filename = f"{uuid4()}-{file.filename}"
    path = Path(settings.upload_dir) / filename
    path.write_bytes(await file.read())

    meta = rag_service.index_pdf(str(path))
    record = UploadedPDF(
        filename=filename,
        original_filename=file.filename,
        pages=meta["pages"],
        uploaded_by=admin.id,
    )
    db.add(record)
    db.commit()
    return {"filename": file.filename, **meta}


@router.get("/student/{student_id}", response_model=StudentRead)
def student(
    student_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    row = analytics.get_student(db, student_id)
    if not row:
        raise HTTPException(404, "Student not found")
    return row


@router.get("/topper/{department}", response_model=StudentRead)
def topper(
    department: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    row = analytics.department_topper(db, department)
    if not row:
        raise HTTPException(404, "Department not found")
    return row


@router.get("/analytics/pass-rate")
def pass_rate(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return analytics.pass_rate(db)


@router.get("/analytics/at-risk")
def at_risk(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return analytics.at_risk(db)


@router.get("/analytics/cgpa-distribution")
def cgpa_distribution(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return analytics.cgpa_distribution(db)


@router.get("/analytics/department-cgpa")
def department_cgpa(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return analytics.average_cgpa(db)


@router.post("/search/web")
async def search(payload: WebSearchRequest, user: User = Depends(get_current_user)):
    return await web_search(payload.query)
