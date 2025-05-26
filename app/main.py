from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import hashlib
from google.cloud import firestore

app = FastAPI()
db = firestore.Client()  # Firestore client

def generate_short_url(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:6]

@app.post("/shorten")
async def shorten_url(data: dict):
    original_url = data.get("url")
    if not original_url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    short_code = generate_short_url(original_url)

    # Save in Firestore collection 'urls'
    doc_ref = db.collection('urls').document(short_code)
    doc_ref.set({"original_url": original_url})

    return {"short_url": f"/{short_code}"}

@app.get("/{code}")
async def redirect(code: str):
    doc_ref = db.collection('urls').document(code)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    long_url = doc.to_dict()["original_url"]
    return RedirectResponse(long_url)
