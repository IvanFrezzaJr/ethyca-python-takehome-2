import time

from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import engine


router = APIRouter(prefix="/status", tags=["status"])

START_TIME = time.time()


def check_database() -> bool:
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


@router.get("/")
def status_root():
    return {"status": "pong"}


@router.get("/health")
def health_check():
    db_ok = check_database()

    # add other status
    overall_status = "ok" if db_ok else "fail"

    return {
        "status": overall_status,
        "dependencies": {"database": "ok" if db_ok else "fail"},
        "uptime_seconds": time.time() - START_TIME,
    }
