from typing import Annotated

from fastapi import APIRouter, Query, Response

from app.dependencies import TaskServiceDep
from app.schemas import Status, TaskCreate, TaskOut, TaskPage, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=TaskPage)
def list_tasks(
    response: Response,
    service: TaskServiceDep,
    status: Status | None = None,
    project_id: int | None = None,
    assignee_id: int | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    items, total = service.list_tasks(status, project_id, assignee_id, limit)
    response.headers["X-Total-Count"] = str(total)
    return {"items": items, "total": total}


@router.post("", status_code=201, response_model=TaskOut)
def create_task(payload: TaskCreate, response: Response, service: TaskServiceDep):
    task = service.create_task(payload)
    response.headers["Location"] = f"/tasks/{task['id']}"
    return task


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, service: TaskServiceDep):
    return service.get_task(task_id)


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, service: TaskServiceDep):
    return service.update_task(task_id, payload)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, service: TaskServiceDep):
    service.delete_task(task_id)
