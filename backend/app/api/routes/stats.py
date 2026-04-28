from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.pomodoro_session import PomodoroSession, SessionMode, SessionStatus
from app.models.user import User

router = APIRouter()


def _utc_day_start(day: datetime) -> datetime:
    return datetime(day.year, day.month, day.day, tzinfo=timezone.utc)


@router.get("/daily")
def daily_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    start = _utc_day_start(now)
    end = start + timedelta(days=1)

    sessions = list(
        db.scalars(
            select(PomodoroSession).where(
                PomodoroSession.user_id == current_user.id,
                PomodoroSession.mode == SessionMode.FOCUS,
                PomodoroSession.status == SessionStatus.COMPLETED,
                PomodoroSession.end_at >= start,
                PomodoroSession.end_at < end,
            )
        )
    )
    total_focus_sec = sum(s.duration_sec for s in sessions)
    return {"date": start.date().isoformat(), "focus_sec": total_focus_sec, "session_count": len(sessions)}


@router.get("/weekly")
def weekly_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    weekday = now.weekday()
    week_start = _utc_day_start(now - timedelta(days=weekday))
    week_end = week_start + timedelta(days=7)

    sessions = list(
        db.scalars(
            select(PomodoroSession).where(
                PomodoroSession.user_id == current_user.id,
                PomodoroSession.mode == SessionMode.FOCUS,
                PomodoroSession.status == SessionStatus.COMPLETED,
                PomodoroSession.end_at >= week_start,
                PomodoroSession.end_at < week_end,
            )
        )
    )
    total_focus_sec = sum(s.duration_sec for s in sessions)
    return {
        "week_start": week_start.date().isoformat(),
        "week_end": (week_end - timedelta(days=1)).date().isoformat(),
        "focus_sec": total_focus_sec,
        "session_count": len(sessions),
    }

