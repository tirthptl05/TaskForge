from fastapi import APIRouter
from app.core.registry import dead_letter_queue

router = APIRouter(prefix="/dlq", tags=["Dead Letter Queue"])

@router.get("/")
def view_dlq():
    return {
        "count": dead_letter_queue.size(),
        "tasks": dead_letter_queue.peek_all()
    }

@router.delete("/")
def clear_dlq():
    dead_letter_queue.clear()
    return {"message": "Dead Letter Queue cleared"}
