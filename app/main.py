from fastapi import FastAPI
from app.note_app_routers import users, notes
from app import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Notes App API")

app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Notes App!"}
