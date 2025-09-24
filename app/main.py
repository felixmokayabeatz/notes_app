import os
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Security, Body
from fastapi.security.api_key import APIKeyHeader
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from starlette.status import HTTP_403_FORBIDDEN
from dotenv import load_dotenv
# from .api_key_generator import create_api_key_string, save_api_key_to_db
from .api_key_generator import generate_api_key_string, save_api_key_to_db


from app.note_app_routers import users, notes
from app import models, database, api_key_generator

# ================== Load ENV ==================
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

ADMIN_SECRET = os.getenv("ADMIN_SECRET")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# ================== Init DB ==================
models.Base.metadata.create_all(bind=database.engine)

# ================== Create ONE FastAPI app ==================
app = FastAPI(title="Notes App API")

# Dependency to validate API key (from DB)
def get_api_key(api_key: str = Security(api_key_header)):
    if api_key and api_key_generator.verify_api_key(api_key):
        return api_key
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
    )

# ================== Include Routers (OPEN) ==================
app.include_router(users.router)
app.include_router(notes.router)

# ================== Routes ==================
@app.get("/")
def root():
    return {"message": "Welcome to Notes App!"}

# ✅ Protect Swagger UI ONLY
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui(api_key: str = Depends(get_api_key)):
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title + " - Docs")

@app.get("/redoc", include_in_schema=False)
async def custom_redoc(api_key: str = Depends(get_api_key)):
    return get_redoc_html(openapi_url=app.openapi_url, title=app.title + " - ReDoc")


@app.post("/generate-api-key")
def generate_api_key_endpoint():
    api_key = generate_api_key_string()
    save_api_key_to_db(api_key, owner="felix")
    return {"api_key": api_key}

@app.get("/openapi.json", include_in_schema=False)
async def openapi_json():
    return app.openapi()
