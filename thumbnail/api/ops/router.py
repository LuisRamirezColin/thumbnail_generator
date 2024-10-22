import os
import aioboto3
from fastapi import Query, APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import asyncio
import logging

# Set up the router and logger
images_router = APIRouter()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Environment variables and API key setup
API_KEY = os.getenv('API_KEY')
api_key_header = APIKeyHeader(name="X-API-KEY")

# Determine storage mode
STORAGE_MODE = os.getenv('STORAGE_MODE', 'development')  # 'development' or 'production'
LOCAL_STORAGE_DIR = 'thumbnails'  # Local directory for development

# Ensure the local storage directory exists
if STORAGE_MODE == 'development':
    os.makedirs(LOCAL_STORAGE_DIR, exist_ok=True)

# Pydantic models for responses
class ErrorResponse(BaseModel):
    detail: str

class ThumbnailResponse(BaseModel):
    filename: str
    thumbnail_url: str = None
    error: str = None

# Valid image MIME types and extensions
VALID_IMAGE_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif'}
VALID_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}

# Function to validate file type
def is_valid_image(file: UploadFile) -> bool:
    return (file.content_type in VALID_IMAGE_MIME_TYPES) and \
           (os.path.splitext(file.filename)[1].lower() in VALID_IMAGE_EXTENSIONS)

def generate_thumbnail(image_file: UploadFile, size=(128, 128)):
    try:
        image_data = image_file.read()  # Read the file content
        img = Image.open(BytesIO(image_data))  # Create image from bytes
        img.thumbnail(size)
        
        thumbnail_io = BytesIO()
        img.save(thumbnail_io, format='JPEG')
        thumbnail_io.seek(0)  # Reset the pointer to the beginning
        return thumbnail_io
    except Exception as e:
        logger.error(f"Error generating thumbnail: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating thumbnail")

# API key validation
async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        logger.warning("Invalid API key provided")
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    logger.info("API key validated successfully")
    return api_key

# Function to save thumbnail to local storage
def save_to_local(thumbnail_io, filename):
    try:
        thumbnail_path = os.path.join(LOCAL_STORAGE_DIR, filename)
        with open(thumbnail_path, 'wb') as f:
            f.write(thumbnail_io.getvalue())
        logger.info(f"Saved thumbnail to local storage: {thumbnail_path}")
        return f'/{LOCAL_STORAGE_DIR}/{filename}'  # URL path to access the file
    except Exception as e:
        logger.error(f"Error saving to local storage: {str(e)}")
        raise HTTPException(status_code=500, detail="Error saving to local storage")

# Function to upload thumbnail to S3
async def upload_to_s3(thumbnail_io, bucket_name, filename):
    async with aioboto3.client('s3') as s3_client:
        try:
            thumbnail_key = f'thumbnails/{filename}'
            await s3_client.upload_fileobj(thumbnail_io, bucket_name, thumbnail_key)
            logger.info(f"Uploaded thumbnail to S3: {thumbnail_key}")
            return f'https://{bucket_name}.s3.amazonaws.com/{thumbnail_key}'
        except Exception as e:
            logger.error(f"Error uploading to S3: {str(e)}")
            raise HTTPException(status_code=500, detail="Error uploading to S3")

# Process each uploaded file
async def process_file(file: UploadFile, bucket_name: str = None, width: int = 128, height: int = 128):
    # Check if the uploaded file is a valid image
    if not is_valid_image(file):
        logger.error(f"Invalid file type for {file.filename}. Expected an image.")
        return {"filename": file.filename, "error": "Invalid file type. Please upload a valid image."}
    
    try:
        logger.info(f"Received file: {file.filename}, Content-Type: {file.content_type}")
        thumbnail_io = generate_thumbnail(file.file, size=(width, height))

        if STORAGE_MODE == 'development':
            thumbnail_url = save_to_local(thumbnail_io, file.filename)
        else:  # Production mode
            if not bucket_name:
                raise HTTPException(status_code=500, detail="S3 bucket not configured")
            thumbnail_url = await upload_to_s3(thumbnail_io, bucket_name, file.filename)
        return ThumbnailResponse(filename=file.filename, thumbnail_url=thumbnail_url)

    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing file")

# FastAPI endpoint for uploading images
@images_router.post("/images", response_model=ThumbnailResponse, responses={500: {"model": ErrorResponse}})
async def upload_image(
    file: UploadFile = File(...),
    bucket_name: str = Query(None, description="S3 bucket name for production mode"),
    api_key: str = Depends(get_api_key)
):
    return await process_file(file, bucket_name)