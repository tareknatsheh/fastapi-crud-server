from fastapi import FastAPI
from routes import students, auth, chat, classes
from fastapi.testclient import TestClient


app = FastAPI()
client = TestClient(app)


app.include_router(auth.router, tags=["Autherization endpoints"])
app.include_router(students.router, tags=["Student endpoints"])
app.include_router(chat.router, tags=["Chat endpoints"])
app.include_router(classes.router, tags=["Classes endpoints"])


@app.get("/")
def home():
    return "Welcome to School API"


