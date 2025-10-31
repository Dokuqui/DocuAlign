from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from db.database import create_db_and_tables
from api.documents import router as documents_router
from core.config import ALLOWED_ORIGINS


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Actions to perform on application startup and shutdown.
    """
    print("Application startup...")
    create_db_and_tables()
    print("Database and tables created.")
    yield
    print("Application shutdown...")


app = FastAPI(
    lifespan=lifespan,
    title="DocuAlign API",
    description="API for processing and aligning documents.",
    version="0.2.0-python-refactored",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router, prefix="/api/documents")


@app.get("/")
def read_root():
    """
    Root endpoint for basic health check.
    """
    return {"message": "Welcome to DocuAlign API. Visit /docs for documentation."}
