from fastapi import APIRouter

router = APIRouter()

@router.get("/purpose")
def purpose():
    return {"The purpose of this app is to help me stay in touch with coding, progress on my cybersecurity skills and learn to build AI agents from scratch"}

