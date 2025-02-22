import os
import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from thumbnail.api.health.router import health_router
from thumbnail.api.secure.router import secure_router
from contextlib import asynccontextmanager
from mangum import Mangum
from thumbnail.api.ops.router import images_router

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("Starting service")
    yield
    logger.debug("Shutting down service")

app = FastAPI(
    title="Thumbnail Generator",
    description="Generate thumbnails from a base image",
    version='0.1.0',
    debug=os.getenv("DEBUG", "true").lower() == "true",
    lifespan=lifespan
)

app.include_router(images_router, prefix='/upload')
app.include_router(secure_router, prefix="/secure")
app.include_router(health_router, prefix="/health")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the Mangum handler
handler = Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8086)
