from fastapi import FastAPI
from routes import students, auth, chat
from fastapi.testclient import TestClient

"""
TODO
- Create routes -> V
- Put db code (json read/write) in another folder -> V
- Add Authentication using jwt to sign-up -> V
- Do sign-in endpoint -> V
- Enforce authorization roles on endpoints -> V
- raise exceptions -> V
- handle edge cases and write tests
- create a README.md -> V
"""

app = FastAPI()
client = TestClient(app)


app.include_router(auth.router, tags=["Autherization endpoints"])
app.include_router(students.router, tags=["Student endpoints"])
app.include_router(chat.router, tags=["Chat endpoints"])


@app.get("/")
def home():
    return "Welcome to School API"


