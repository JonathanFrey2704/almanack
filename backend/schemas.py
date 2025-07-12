from pydantic import BaseModel

class SavedYouTubeChannelBase(BaseModel):
    name: str
    youtube_channel_id: str

class SavedYouTubeChannelCreate(BaseModel):
    channel_id: str

class SavedYouTubeChannel(SavedYouTubeChannelBase):
    id: int

    class Config:
        from_attributes = True 