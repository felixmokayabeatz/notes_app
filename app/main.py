from fastapi import FastAPI
from note_app_routers import users, notes
import models, database

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Notes App API")

app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Notes App!"}
