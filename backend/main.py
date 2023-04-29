from fastapi import FastAPI
from backend.api import users, hobbies

app = FastAPI()

app.include_router(users.router)
app.include_router(hobbies.router)


@app.get("/")
def hello():
    return {"msg": "Gal Davidi interview for Tenable"}
