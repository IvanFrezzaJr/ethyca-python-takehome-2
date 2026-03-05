from fastapi import FastAPI

from app.routers import status, game
from app.settings import Settings

app = FastAPI()
settings = Settings()

app.include_router(status.router)
app.include_router(game.router)


@app.get("/")
def root():
    return {
        "name": settings.APP_NAME,
        "version": app.version,
        "documentation": "/docs",
        "status": "ok",
    }
