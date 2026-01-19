from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_recommendation():
    return {"message": "Recommendation"}