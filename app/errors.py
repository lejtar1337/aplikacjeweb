

from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas import Problem


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class InvalidReferenceError(Exception):
    def __init__(self, field: str, message: str) -> None:
        super().__init__(message)
        self.field = field


def problem(status: int, detail: str, errors: list[dict] | None = None, headers: dict | None = None) -> JSONResponse:
    body = Problem(title=HTTPStatus(status).phrase, status=status, detail=detail, errors=errors)
    return JSONResponse(
        body.model_dump(exclude_none=True),
        status_code=status,
        headers=headers,
        media_type="application/problem+json",
    )

def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return problem(exc.status_code, str(exc.detail), headers=exc.headers)


def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    if any(error["type"] == "json_invalid" for error in exc.errors()):
        return problem(400, "Ciało żądania nie jest poprawnym dokumentem JSON")
    errors = [
        {
            "location": error["loc"][0],
            "field": ".".join(str(part) for part in error["loc"][1:]),
            "message": error["msg"],
        }
        for error in exc.errors()
    ]
    return problem(422, "Dane wejściowe nie spełniają kontraktu API", errors)


def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return problem(404, str(exc))


def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
    return problem(409, str(exc))


def invalid_reference_handler(request: Request, exc: InvalidReferenceError) -> JSONResponse:
    errors = [{"location": "body", "field": exc.field, "message": str(exc)}]
    return problem(422, "Dane wejściowe nie spełniają kontraktu API", errors)


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(NotFoundError, not_found_handler)
    app.add_exception_handler(ConflictError, conflict_handler)
    app.add_exception_handler(InvalidReferenceError, invalid_reference_handler)
