from sqlalchemy import Column, Integer, String
from database import Base

class SavedYouTubeChannel(Base):
    __tablename__ = "saved_youtube_channels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    youtube_channel_id = Column(String, unique=True, index=True) 