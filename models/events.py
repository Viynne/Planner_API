from typing import List, Optional
from sqlmodel import JSON, SQLModel, Field, Column
from beanie import Document
from pydantic import BaseModel


class Event(Document):
    creator: Optional[str]
    title: str
    image: str
    description: str
    tags: List[str] = Field(sa_column=Column(JSON))
    location: str

    class Config:
        arbitrary_type_allowed = True
        schema_extra = {
            "example": {
                "title": "FastAPI",
                "image": "https://theimages.com/image.png",
                "description": "This is an API framework",
                "tags": ["python", 'fastapi'],
                "location": "Google Meet"
            }
        }

        class Settings:
            name = "events"


class EventUpdate(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "FastAPI",
                "image": "https://theimages.com/image.png",
                "description": "This is an API framework",
                "tags": ["python", 'fastapi'],
                "location": "Google Meet"
            }
        }
