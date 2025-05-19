import os
import logging
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from agent_tools import search_brave

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    limit: int = 10
    market: str = "en-US"

@app.get("/search/")
async def search_get(
    q: str = Query(..., description="Từ khóa tìm kiếm"),
    limit: int = Query(10),
    market: str = Query("en-US"),
):
    api_key = os.getenv("BRAVE_SEARCH_API_KEY")
    subscription_token = os.getenv("BRAVE_SEARCH_SUBSCRIPTION_TOKEN")
    if not api_key or not subscription_token:
        logger.error("API key or subscription token not configured in environment variables.")
        raise HTTPException(status_code=500, detail="API key or subscription token not configured.")
    try:
        results = await search_brave(
            query=q,
            api_key=api_key,
            subscription_token=subscription_token,
            limit=limit,
            market=market
        )
    except Exception as e:
        logger.error(f"Failed to search Brave API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"results": results}

@app.post("/search/")
async def search_post(request: QueryRequest):
    api_key = os.getenv("BRAVE_SEARCH_API_KEY")
    subscription_token = os.getenv("BRAVE_SEARCH_SUBSCRIPTION_TOKEN")
    if not api_key or not subscription_token:
        logger.error("API key or subscription token not configured in environment variables.")
        raise HTTPException(status_code=500, detail="API key or subscription token not configured.")
    try:
        results = await search_brave(
            query=request.query,
            api_key=api_key,
            subscription_token=subscription_token,
            limit=request.limit,
            market=request.market
        )
    except Exception as e:
        logger.error(f"Failed to search Brave API: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return {"results": results}
