from fastapi import FastAPI
from dotenv import load_dotenv
import os
from app.routers import hello, purpose

app = FastAPI()

@app.get("/")
def root():
    secret = os.getenv("MY_SECRET_TEST", "not set")
    return {"message": "Hello from FastAPI" + secret}

@app.get("/test")
def test():
    return {"my first test API in a long time"}

app.include_router(hello.router, prefix="/api")
app.include_router(purpose.router, prefix="/api")