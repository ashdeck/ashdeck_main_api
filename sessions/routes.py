from fastapi import APIRouter
from .models import ScheduledSession, RecurringSession, Session


# nest sessions in the database like:
'''
{
    recurring: [recurring_session_object],
    schedule: [schedule_session_object],
    session: [session_object]
}
'''
router = APIRouter()


@router.post("", status_code=201, description="Create session")
async def create_session(session: Session):
    pass


@router.post("/schedule", status_code=201, description="Create session")
async def schedule_session(session: ScheduledSession):
    pass


@router.post("/recurring", status_code=201, description="Create session")
async def schedule_recurring_session(session: RecurringSession):
    pass


@router.get("/", status_code=200)
async def get_sessions():
    pass
