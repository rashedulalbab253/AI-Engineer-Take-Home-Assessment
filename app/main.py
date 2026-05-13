from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.core.config import settings
from app.api import routes
from app.db.database import engine, Base
import os

# Create db tables safely avoiding uvicorn reload race conditions
import sqlalchemy
try:
    Base.metadata.create_all(bind=engine)
except sqlalchemy.exc.OperationalError:
    pass

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Grounded Legal Document Intelligence System API"
)

app.include_router(routes.router, prefix=settings.API_V1_STR)

os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")
