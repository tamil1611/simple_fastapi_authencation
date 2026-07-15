from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import auth, tasks
from app.core.config import settings
from app.db.init_db import init_db
from app.schemas.common import MessageResponse


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    description=(
        "Secure Task Manager REST API using FastAPI, SQLite, "
        "SQLAlchemy, Pydantic, bcrypt password hashing and JWT auth."
    ),
    version="2.0.0",
    lifespan=lifespan,
    swagger_ui_parameters={"persistAuthorization": True},
)

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get(
    "/",
    response_model=MessageResponse,
    tags=["Health"],
    summary="Check API health",
)
def health_check() -> dict[str, str]:
    return {"message": "Task Manager API is running successfully"}