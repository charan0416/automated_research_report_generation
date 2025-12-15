from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from research_and_analyst.database.db_config import SessionLocal, User, hash_password, verify_password
from research_and_analyst.api.services.report_service import ReportService

router = APIRouter()
SESSIONS = {}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ AUTH ROUTES ------------------ #

@router.get("/", response_class=HTMLResponse)
async def show_login(request: Request):
    return request.app.templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    db = next(get_db())
    user = db.query(User).filter(User.username == username).first()

    if user and verify_password(password, user.password):
        session_id = f"{username}_session"
        SESSIONS[session_id] = username
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie(key="session_id", value=session_id)
        return response

    return request.app.templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid username or password"},
    )

@router.get("/signup", response_class=HTMLResponse)
async def show_signup(request: Request):
    return request.app.templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, username: str = Form(...), password: str = Form(...)):
    db = next(get_db())
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return request.app.templates.TemplateResponse(
            "signup.html", {"request": request, "error": "Username already exists"}
        )

    hashed_pw = hash_password(password)
    new_user = User(username=username, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return RedirectResponse(url="/", status_code=302)

# ------------------ REPORT ROUTES ------------------ #

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id not in SESSIONS:
        return RedirectResponse(url="/")
    return request.app.templates.TemplateResponse("dashboard.html", {"request": request, "user": SESSIONS[session_id]})

@router.post("/generate_report", response_class=HTMLResponse)
async def generate_report(request: Request, topic: str = Form(...)):
    service = ReportService()
    result = service.start_report_generation(topic, 3)
    thread_id = result["thread_id"] 

    return request.app.templates.TemplateResponse(
        "report_progress.html",
        {
            "request": request,
            "topic": topic,
            "feedback": "",
            "thread_id": thread_id,
        },
    )

@router.post("/submit_feedback", response_class=HTMLResponse)
async def submit_feedback(request: Request, topic: str = Form(...), feedback: str = Form(...), thread_id: str = Form(...)):
    service = ReportService()
    service.submit_feedback(thread_id, feedback)

    # Get latest report status
    result = service.get_report_status(thread_id)
    doc_path = result.get("docx_path")
    pdf_path = result.get("pdf_path")

    return request.app.templates.TemplateResponse(
        "report_progress.html",
        {
            "request": request,
            "topic": topic,
            "feedback": feedback,
            "doc_path": doc_path,
            "pdf_path": pdf_path,
            "thread_id": thread_id,
        },
    )

@router.get("/download/{file_name}", response_class=HTMLResponse)
async def download_report(file_name: str):
    service = ReportService()
    file_response = service.download_file(file_name)
    if file_response:
        return file_response
    return {"error": f"File {file_name} not found"}
