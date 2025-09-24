from fastapi import FastAPI
from routers import notes, users

app = FastAPI(title="Notes App API")

# include routers
app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Notes App!"}
