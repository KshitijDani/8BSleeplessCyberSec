from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from FastAPI"}

@app.get("/test")
def test():
    return {"my first test API in a long time"}

@app.get("/purpose")
def purpose():
    return {"The purpose of this app is to help me stay in touch with coding, progress on my cybersecurity skills and learn to build AI agents from scratch"}