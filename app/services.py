from app.errors import ConflictError, InvalidReferenceError, NotFoundError
from app.schemas import ProjectCreate, ProjectUpdate, Status, TaskCreate, TaskUpdate
from app.storage import Storage


class ProjectService:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def list_projects(self) -> list[dict]:
        return [self._with_task_count(project) for project in self.storage.projects.values()]

    def get_project(self, project_id: int) -> dict:
        return self._with_task_count(self._get_or_raise(project_id))

    def create_project(self, data: ProjectCreate) -> dict:
        if any(project["name"] == data.name for project in self.storage.projects.values()):
            raise ConflictError("Projekt o tej nazwie już istnieje")
        project_id = next(self.storage.next_project_id)
        project = {"id": project_id, **data.model_dump()}
        self.storage.projects[project_id] = project
        return self._with_task_count(project)

    def update_project(self, project_id: int, data: ProjectUpdate) -> dict:
        project = self._get_or_raise(project_id)
        changes = data.model_dump(exclude_unset=True)
        if "name" in changes and any(
            other["name"] == changes["name"] and other["id"] != project_id
            for other in self.storage.projects.values()
        ):
            raise ConflictError("Projekt o tej nazwie już istnieje")
        project.update(changes)
        return self._with_task_count(project)

    def delete_project(self, project_id: int) -> None:
        project = self._get_or_raise(project_id)
        if self._with_task_count(project)["task_count"] > 0:
            raise ConflictError("Projekt zawiera zadania i nie może zostać usunięty")
        del self.storage.projects[project_id]

    def _get_or_raise(self, project_id: int) -> dict:
        project = self.storage.projects.get(project_id)
        if project is None:
            raise NotFoundError(f"Projekt {project_id} nie istnieje")
        return project

    def _with_task_count(self, project: dict) -> dict:
        task_count = sum(1 for task in self.storage.tasks.values() if task["project_id"] == project["id"])
        return {**project, "task_count": task_count}


class TaskService:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def list_tasks(
        self,
        status: Status | None = None,
        project_id: int | None = None,
        assignee_id: int | None = None,
        limit: int = 20,
    ) -> tuple[list[dict], int]:
        items = list(self.storage.tasks.values())
        if status is not None:
            items = [task for task in items if task["status"] == status]
        if project_id is not None:
            items = [task for task in items if task["project_id"] == project_id]
        if assignee_id is not None:
            items = [task for task in items if task["assignee_id"] == assignee_id]
        return items[:limit], len(items)

    def get_task(self, task_id: int) -> dict:
        task = self.storage.tasks.get(task_id)
        if task is None:
            raise NotFoundError(f"Zadanie {task_id} nie istnieje")
        return task

    def create_task(self, data: TaskCreate) -> dict:
        if data.project_id not in self.storage.projects:
            raise InvalidReferenceError("project_id", f"Projekt {data.project_id} nie istnieje")
        self._ensure_assignee_exists(data.assignee_id)
        self._ensure_unique_title(data.project_id, data.title)
        task_id = next(self.storage.next_task_id)
        task = {"id": task_id, **data.model_dump()}
        self.storage.tasks[task_id] = task
        return task

    def update_task(self, task_id: int, data: TaskUpdate) -> dict:
        task = self.get_task(task_id)
        changes = data.model_dump(exclude_unset=True)
        if "assignee_id" in changes:
            self._ensure_assignee_exists(changes["assignee_id"])
        if "title" in changes:
            self._ensure_unique_title(task["project_id"], changes["title"], task_id)
        task.update(changes)
        return task

    def delete_task(self, task_id: int) -> None:
        self.get_task(task_id)
        del self.storage.tasks[task_id]

    def _ensure_assignee_exists(self, assignee_id: int | None) -> None:
        if assignee_id is not None and assignee_id not in self.storage.users:
            raise InvalidReferenceError("assignee_id", f"Użytkownik {assignee_id} nie istnieje")

    def _ensure_unique_title(self, project_id: int, title: str, task_id: int | None = None) -> None:
        for task in self.storage.tasks.values():
            if task["project_id"] == project_id and task["title"] == title and task["id"] != task_id:
                raise ConflictError("Zadanie o tym tytule już istnieje w projekcie")
