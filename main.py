from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
import hashlib

from database import Base, engine, SessionLocal

from models import URLMap


app = FastAPI(title="Persistent URL Shortener", version="1.0")

# Create database tables
Base.metadata.create_all(bind=engine)

# ------------------------------
# Dependency
# ------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------
# Data Models
# ------------------------------

class URLRequest(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    short_url: str

# ------------------------------
# Utility Functions
# ------------------------------

def generate_short_code(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:6]

def build_short_url(request: Request, code: str) -> str:
    return f"{request.base_url}{code}"

# ------------------------------
# Routes
# ------------------------------

@app.post("/shorten", response_model=URLResponse)
def shorten_url(
    request_data: URLRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    original_url = str(request_data.url)  # <-- convert HttpUrl to str
    short_code = generate_short_code(original_url)

    # Check if already exists
    url_obj = db.query(URLMap).filter(URLMap.code == short_code).first()
    if not url_obj:
        url_obj = URLMap(code=short_code, original_url=original_url)
        db.add(url_obj)
        db.commit()

    return URLResponse(short_url=build_short_url(request, short_code))


@app.get("/{code}")
def redirect_to_original_url(code: str, db: Session = Depends(get_db)):
    url_obj = db.query(URLMap).filter(URLMap.code == code).first()
    if not url_obj:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return RedirectResponse(url=url_obj.original_url)
