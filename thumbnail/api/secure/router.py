import os
from fastapi import APIRouter, HTTPException, Depends

secure_router = APIRouter()

# Dependency to check API key
async def verify_api_key(api_key: str):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail='Invalid API Key')

@secure_router.get("/api-key", tags=["api-key"])
async def secure_data(api_key: str = Depends(verify_api_key)):
    return {"message": "secure data!!"}