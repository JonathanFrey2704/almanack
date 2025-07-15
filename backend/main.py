import os
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uvicorn
from sqlalchemy.exc import IntegrityError
from database import engine, get_db
from models import Base, SavedYouTubeChannel
from schemas import SavedYouTubeChannelCreate, SavedYouTubeChannel as SavedYouTubeChannelSchema
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Almanack API",
    description="Backend API for Almanack application",
    version="1.0.0"
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    message: str

# API Routes
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return HealthResponse(status="ok", message="Almanack API is running!")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy", message="Server is healthy")

@app.get("/api/hello")
async def hello():
    """Simple hello endpoint"""
    return {"message": "Hello from FastAPI!"}

# YouTube Channel endpoints
@app.post("/api/youtube-channels/", response_model=SavedYouTubeChannelSchema)
def add_youtube_channel(channel: SavedYouTubeChannelCreate, db: Session = Depends(get_db)):
    """Add a new YouTube channel"""
    db_channel = SavedYouTubeChannel(
        name=channel.name,
        youtube_channel_id=channel.youtube_channel_id
    )
    try:
        db.add(db_channel)
        db.commit()
        db.refresh(db_channel)
        return db_channel
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Channel already saved.")

@app.get("/api/youtube-channels/", response_model=list[SavedYouTubeChannelSchema])
def get_youtube_channels(db: Session = Depends(get_db)):
    """Get all saved YouTube channels"""
    return db.query(SavedYouTubeChannel).all()

@app.get("/api/youtube-search/")
def youtube_search(q: str = Query(..., min_length=2)):
    if not YOUTUBE_API_KEY:
        raise HTTPException(status_code=500, detail="YouTube API key not configured.")
    base_url = "https://www.googleapis.com/youtube/v3/channels"
    # Handle: starts with @
    if q.startswith("@"):
        params = {
            "part": "snippet",
            "forHandle": q[1:],
            "key": YOUTUBE_API_KEY,
            "maxResults": 1,
        }
        r = requests.get(base_url, params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="YouTube API error.")
        data = r.json()
        results = [
            {
                "name": item["snippet"]["title"],
                "youtube_channel_id": item["id"]
            }
            for item in data.get("items", [])
        ]
        return results
    # Channel ID: starts with UC
    elif q.startswith("UC") and len(q) >= 24:
        params = {
            "part": "snippet",
            "id": q,
            "key": YOUTUBE_API_KEY,
            "maxResults": 1,
        }
        r = requests.get(base_url, params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="YouTube API error.")
        data = r.json()
        results = [
            {
                "name": item["snippet"]["title"],
                "youtube_channel_id": item["id"]
            }
            for item in data.get("items", [])
        ]
        return results
    # Fallback: keyword search (as before)
    else:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "type": "channel",
            "q": q,
            "key": YOUTUBE_API_KEY,
            "maxResults": 8,
        }
        r = requests.get(url, params=params)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="YouTube API error.")
        data = r.json()
        results = [
            {
                "name": item["snippet"]["channelTitle"],
                "youtube_channel_id": item["snippet"]["channelId"]
            }
            for item in data.get("items", [])
        ]
        return results

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 