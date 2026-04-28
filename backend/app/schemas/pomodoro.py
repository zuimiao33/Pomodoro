from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.pomodoro_session import SessionMode, SessionStatus


class PomodoroStartRequest(BaseModel):
    task_id: Optional[int] = None
    mode: SessionMode = SessionMode.FOCUS
    duration_sec: int = Field(default=1500, ge=60, le=7200)


class PomodoroSessionRead(BaseModel):
    id: int
    task_id: Optional[int]
    mode: SessionMode
    status: SessionStatus
    duration_sec: int
    elapsed_sec: int
    remaining_sec: int
    start_at: datetime
    last_started_at: Optional[datetime]
    end_at: Optional[datetime]

    class Config:
        from_attributes = True

