from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.routes.chat import router as chat_router
from config import validate_config


BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"

validate_config()

app = FastAPI(
    title="NOVA API",
    description="Personal AI Assistant",
    version="0.2.0",
)

app.include_router(chat_router)

app.mount(
    "/static",
    StaticFiles(directory=WEB_DIR),
    name="static",
)


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/health", tags=["System"])
def health():
    return {
        "status": "ok",
        "service": "NOVA",
    }