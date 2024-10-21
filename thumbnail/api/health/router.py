from fastapi import APIRouter, HTTPException

health_router = APIRouter()

@health_router.get("/check", tags=["health"])
async def health_check():
    try:
        # Example: Check database connection
        # await db_connection.check()  # Pseudo-code for checking DB connection
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Service unavailable")
