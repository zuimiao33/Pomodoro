from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    note: Optional[str] = None
    priority: int = Field(default=2, ge=1, le=3)
    due_at: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    note: Optional[str] = None
    priority: Optional[int] = Field(default=None, ge=1, le=3)
    status: Optional[TaskStatus] = None
    due_at: Optional[datetime] = None


class TaskRead(BaseModel):
    id: int
    title: str
    note: Optional[str]
    priority: int
    status: TaskStatus
    due_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

