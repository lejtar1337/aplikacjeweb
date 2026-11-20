from typing import Annotated

from fastapi import Depends

from app.services import ProjectService, TaskService
from app.storage import Storage, get_storage

StorageDep = Annotated[Storage, Depends(get_storage)]


def get_task_service(storage: StorageDep) -> TaskService:
    return TaskService(storage)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]


def get_project_service(storage: StorageDep) -> ProjectService:
    return ProjectService(storage)


ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]
