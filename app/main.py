from fastapi import FastAPI
from dotenv import load_dotenv
# need to load env variables otherwise agent router that needs API key doesn't load
load_dotenv()

from app.routers import hello, purpose, agent, scanner

import os

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
app.include_router(agent.router, prefix="/api")
app.include_router(scanner.router, prefix="/api")


# /Users/kshitijdani/Desktop/UW/Fall 2025/IMT 555 Cyber/sum-24-uw-cybersec-huskey-manager/webapp/public/users