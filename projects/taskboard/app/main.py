from http.client import HTTPException
from urllib import response
from pydantic import BaseModel
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title = "TaskBoard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
)


@app.get("/")
def root():
    return {"message": "Hello Web"}
@app.get("/health")
def health():
    return {"status": "ok"}

TASKS: dict[int, dict] = {
    1: {"id": 1,"title": "Przygotować środowisko",
        "status": "done", "priority": "high"},
    2: {"id": 2,"title": "Przeczytać RFC 9110",
        "status": "open", "priority": "medium"},
}
NEXT_ID: int = 3

@app.get("/tasks")
def List_tasks():
    return {"items": list(TASKS.values()), "total": len(TASKS)}

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = TASKS.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="zadanie nie istnieje")
    return task

@app.get("/tasks")
def list_tasks(status: str | None = None, limit: int = 20):
    items = list(TASKS.values())
    if status is not None:
        items = [t for t in items if t["status"] == status]
        return {"items": items[:limit], "total": len(items)}

class TaskIn(BaseModel):
    title: str
    status: str = "open"
    priority: str = "medium"


@app.post("/tasks", status_code=201)
def create_task(payload: TaskIn, response: Response):
    if any(t.title == payload.title for t in tasks_db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Task already exists")
    task = ""
    response.headers["Location"] = f"/tasks/{NEXT_ID}"
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="zadanie nie istnieje")
    del TASKS[task_id]


