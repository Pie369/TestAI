import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import greeting_agent, Deps

class QueryRequest(BaseModel):
    query: str

app = FastAPI()

@app.post("/search/")
async def search_endpoint(request: QueryRequest):
    deps = Deps(api_key=os.getenv("BRAVE_SEARCH_API_KEY"))
    if deps.api_key is None:
        raise HTTPException(status_code=500, detail="Search API key not configured.")

    try:
        result = await greeting_agent.run(request.query, deps=deps)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"response": result.data}
