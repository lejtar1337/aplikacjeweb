from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, field_validator


def not_blank(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Wartość nie może składać się z samych białych znaków")
    return value


Title = Annotated[str, Field(min_length=1, max_length=200), AfterValidator(not_blank)]
Name = Annotated[str, Field(min_length=1, max_length=100), AfterValidator(not_blank)]
Description = Annotated[str, Field(max_length=500)]
Status = Literal["open", "in_progress", "done"]
Priority = Literal["low", "medium", "high"]


class UserOut(BaseModel):
    id: int
    name: str


class ProjectCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Name
    description: Description | None = None


class ProjectUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Name | None = None
    description: Description | None = None

    @field_validator("name")
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("Pole nie może mieć wartości null")
        return value


class ProjectOut(BaseModel):
    id: int
    name: str
    description: str | None
    task_count: int


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_id: int
    title: Title
    status: Status = "open"
    priority: Priority = "medium"
    assignee_id: int | None = None


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Title | None = None
    status: Status | None = None
    priority: Priority | None = None
    assignee_id: int | None = None

    @field_validator("title", "status", "priority")
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("Pole nie może mieć wartości null")
        return value


class TaskOut(BaseModel):
    id: int
    project_id: int
    title: str
    status: Status
    priority: Priority
    assignee_id: int | None


class TaskPage(BaseModel):
    items: list[TaskOut]
    total: int


class FieldError(BaseModel):
    location: str
    field: str
    message: str


class Problem(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    detail: str
    errors: list[FieldError] | None = None