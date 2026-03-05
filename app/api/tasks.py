from fastapi import APIRouter

from app.tasks.jobs import long_running_calculation

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/calculate/{value}")
def trigger_calculation(value: int):
    task = long_running_calculation.delay(value)
    return {"task_id": task.id, "status": "submitted"}
