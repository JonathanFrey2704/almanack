from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uvicorn

from database import engine, get_db
from models import Base, SavedYouTubeChannel
from schemas import SavedYouTubeChannelCreate, SavedYouTubeChannel as SavedYouTubeChannelSchema

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
        name=channel.channel_id,
        youtube_channel_id=channel.channel_id
    )
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel

@app.get("/api/youtube-channels/", response_model=list[SavedYouTubeChannelSchema])
def get_youtube_channels(db: Session = Depends(get_db)):
    """Get all saved YouTube channels"""
    return db.query(SavedYouTubeChannel).all()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 