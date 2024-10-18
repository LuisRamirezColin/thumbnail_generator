import os
import aioboto3
from fastapi import Query
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from PIL import Image
from io import BytesIO
import asyncio
import logging

images_router = APIRouter()
logger = logging.getLogger(__name__)

API_KEY = os.getenv('API_KEY')
api_key_header = APIKeyHeader(name="X-API-KEY")

class ErrorResponse(BaseModel):
    detail: str

class ThumbnailResponse(BaseModel):
    filename: str
    thumbnail_url: str = None
    error: str = None

def generate_thumbnail(image_file, size=(128, 128)):
    try:
        img = Image.open(image_file)
        img.thumbnail(size)
        thumbnail_io = BytesIO()
        img.save(thumbnail_io, format='JPEG')
        thumbnail_io.seek(0)
        return thumbnail_io
    except Exception as e:
        logger.error(f"Error generating thumbnail: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating thumbnail")

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

async def upload_to_s3(thumbnail_io, bucket_name, filename):
    async with aioboto3.client('s3') as s3_client:
        try:
            thumbnail_key = f'thumbnails/{filename}'
            await s3_client.upload_fileobj(thumbnail_io, bucket_name, thumbnail_key)
            return f'https://{bucket_name}.s3.amazonaws.com/{thumbnail_key}'
        except Exception as e:
            logger.error(f"Error uploading to S3: {str(e)}")
            raise HTTPException(status_code=500, detail="Error uploading to S3")

async def process_file(file: UploadFile, bucket_name: str, width: int, height: int):
    try:
        thumbnail_io = generate_thumbnail(file.file, size=(width, height))
        thumbnail_url = await upload_to_s3(thumbnail_io, bucket_name, file.filename)
        return {"filename": file.filename, "thumbnail_url": thumbnail_url}
    except HTTPException as e:
        return {"filename": file.filename, "error": e.detail}
    except Exception as e:
        logger.error(f"Unexpected error processing file {file.filename}: {str(e)}")
        return {"filename": file.filename, "error": "Unexpected error"}

@images_router.post("/", response_model=list[ThumbnailResponse], responses={500: {"model": ErrorResponse}})
async def upload_image(
    files: list[UploadFile] = File(...),
    width: int = Query(default=128, description="Thumbnail width"),
    height: int = Query(default=128, description="Thumbnail height"),
    api_key: str = Depends(get_api_key)):

    if not API_KEY:
        raise HTTPException(status_code=500, detail="API key not configured")

    bucket_name = os.getenv('S3_BUCKET')
    if not bucket_name:
        raise HTTPException(status_code=500, detail="S3 bucket not configured")

    tasks = [process_file(file, bucket_name, width, height) for file in files]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Format results according to ThumbnailResponse
    formatted_results = []
    for result in results:
        if isinstance(result, dict):
            formatted_results.append(ThumbnailResponse(**result))
        else:
            formatted_results.append(ThumbnailResponse(filename=str(result), error="Unknown error"))

    return formatted_results
