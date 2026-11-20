from app.routers import projects, tasks, users
from app.config import settings
from app.errors import register_error_handlers
from app.schemas import Problem

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title=settings.app_title,
    responses={
        400: {"model": Problem},
        404: {"model": Problem},
        409: {"model": Problem},
        422: {"model": Problem},
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    expose_headers=["X-Total-Count"],
)
register_error_handlers(app)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/")
def root():
    return {"message": "Hello Web"}


@app.get("/health")
def health():
    return {"status": "ok"}
