from fastapi import FastAPI
from dotenv import load_dotenv

# need to load env variables otherwise agent router that needs API key doesn't load
load_dotenv()

from app.routers import hello, purpose, scanner, langgraphAPI

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to "http://localhost:5173"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hello.router, prefix="/api")
app.include_router(purpose.router, prefix="/api")
app.include_router(scanner.router, prefix="/api")
app.include_router(langgraphAPI.router, prefix="/api")