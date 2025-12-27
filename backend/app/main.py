from fastapi import FastAPI

from app.versions.v1 import router as v1_router

app = FastAPI()


@app.get('/')
def health_check():
    return {"message": "Cycling routes API is running"}

app.include_router(router=v1_router)
