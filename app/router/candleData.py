from fastapi import Request, APIRouter, Query

router = APIRouter(prefix='/candleData', tags=['CandleData'])

@router.get("/")
async def get_token_to_name():
    return {"data": "success"}