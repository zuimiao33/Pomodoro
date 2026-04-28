from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.pomodoro_session import PomodoroSession, SessionStatus
from app.models.user import User
from app.schemas.pomodoro import PomodoroSessionRead, PomodoroStartRequest
from app.utils.time import utcnow

router = APIRouter()


def _computed_elapsed(session: PomodoroSession) -> int:
    elapsed = session.elapsed_sec
    if session.status == SessionStatus.RUNNING and session.last_started_at:
        elapsed += int((utcnow() - session.last_started_at).total_seconds())
    return max(0, elapsed)


def _to_read_model(session: PomodoroSession) -> PomodoroSessionRead:
    elapsed = _computed_elapsed(session)
    remaining = max(0, session.duration_sec - elapsed)
    return PomodoroSessionRead(
        id=session.id,
        task_id=session.task_id,
        mode=session.mode,
        status=session.status,
        duration_sec=session.duration_sec,
        elapsed_sec=elapsed,
        remaining_sec=remaining,
        start_at=session.start_at,
        last_started_at=session.last_started_at,
        end_at=session.end_at,
    )


@router.post("/start", response_model=PomodoroSessionRead, status_code=status.HTTP_201_CREATED)
def start_session(
    payload: PomodoroStartRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    active = db.scalar(
        select(PomodoroSession).where(
            PomodoroSession.user_id == current_user.id,
            PomodoroSession.status.in_([SessionStatus.RUNNING, SessionStatus.PAUSED]),
            PomodoroSession.end_at.is_(None),
        )
    )
    if active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="已有进行中的番茄钟")

    now = utcnow()
    session = PomodoroSession(
        user_id=current_user.id,
        task_id=payload.task_id,
        mode=payload.mode,
        duration_sec=payload.duration_sec,
        elapsed_sec=0,
        status=SessionStatus.RUNNING,
        start_at=now,
        last_started_at=now,
        end_at=None,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return _to_read_model(session)


@router.post("/pause", response_model=PomodoroSessionRead)
def pause_session(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.scalar(
        select(PomodoroSession).where(
            PomodoroSession.user_id == current_user.id,
            PomodoroSession.status == SessionStatus.RUNNING,
            PomodoroSession.end_at.is_(None),
        )
    )
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="没有进行中的番茄钟")

    session.elapsed_sec = _computed_elapsed(session)
    session.last_started_at = None
    session.status = SessionStatus.PAUSED
    db.commit()
    db.refresh(session)
    return _to_read_model(session)


@router.post("/resume", response_model=PomodoroSessionRead)
def resume_session(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.scalar(
        select(PomodoroSession).where(
            PomodoroSession.user_id == current_user.id,
            PomodoroSession.status == SessionStatus.PAUSED,
            PomodoroSession.end_at.is_(None),
        )
    )
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="没有已暂停的番茄钟")

    session.last_started_at = utcnow()
    session.status = SessionStatus.RUNNING
    db.commit()
    db.refresh(session)
    return _to_read_model(session)


@router.post("/finish", response_model=PomodoroSessionRead)
def finish_session(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.scalar(
        select(PomodoroSession).where(
            PomodoroSession.user_id == current_user.id,
            PomodoroSession.status.in_([SessionStatus.RUNNING, SessionStatus.PAUSED]),
            PomodoroSession.end_at.is_(None),
        )
    )
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="没有活动中的番茄钟")

    session.elapsed_sec = min(session.duration_sec, _computed_elapsed(session))
    session.status = SessionStatus.COMPLETED
    session.last_started_at = None
    session.end_at = utcnow()
    db.commit()
    db.refresh(session)
    return _to_read_model(session)


@router.get("/current", response_model=PomodoroSessionRead | None)
def get_current_session(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = db.scalar(
        select(PomodoroSession).where(
            PomodoroSession.user_id == current_user.id,
            PomodoroSession.status.in_([SessionStatus.RUNNING, SessionStatus.PAUSED]),
            PomodoroSession.end_at.is_(None),
        )
    )
    if not session:
        return None
    return _to_read_model(session)
