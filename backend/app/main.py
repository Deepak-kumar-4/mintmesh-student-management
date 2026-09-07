from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.database import Base, engine
from app.routes import students


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Student Management System", lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    detail = errors[0]["msg"] if len(errors) == 1 else [e["msg"] for e in errors]
    return JSONResponse(status_code=400, content={"detail": detail})


app.include_router(students.router)


@app.get("/health")
def health():
    return {"status": "ok"}
