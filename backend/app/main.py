from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db import initialize_connection_pool, close_connection_pool
from app.versions.v1 import router as v1_router

@asynccontextmanager
async def lifespan():
    initialize_connection_pool()
    yield
    close_connection_pool()

app = FastAPI(lifespan=lifespan)

@app.get('/')
def health_check():
    return {"message": "Cycling routes API is running"}

app.include_router(router=v1_router)
