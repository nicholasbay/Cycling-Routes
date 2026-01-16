from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.db import initialize_connection_pool, close_connection_pool
from app.versions.v1 import router as v1_router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_connection_pool()
    yield
    close_connection_pool()

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router=v1_router)


@app.get('/health', tags=['Health'])
def health_check():
    return JSONResponse(
        content={"message": f"{settings.APP_TITLE} is running"},
        status_code=status.HTTP_200_OK
    )
