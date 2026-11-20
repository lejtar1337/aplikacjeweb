from fastapi import APIRouter, Response

from app.dependencies import ProjectServiceDep
from app.schemas import ProjectCreate, ProjectOut, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectOut])
def list_projects(service: ProjectServiceDep):
    return service.list_projects()


@router.post("", status_code=201, response_model=ProjectOut)
def create_project(payload: ProjectCreate, response: Response, service: ProjectServiceDep):
    project = service.create_project(payload)
    response.headers["Location"] = f"/projects/{project['id']}"
    return project


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, service: ProjectServiceDep):
    return service.get_project(project_id)


@router.patch("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, payload: ProjectUpdate, service: ProjectServiceDep):
    return service.update_project(project_id, payload)


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, service: ProjectServiceDep):
    service.delete_project(project_id)
