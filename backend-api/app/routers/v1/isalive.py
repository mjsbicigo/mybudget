from fastapi import APIRouter

router = APIRouter()

@router.get("/api/v1/isalive", status_code=200)
async def is_alive():
    return {"status": "true"}