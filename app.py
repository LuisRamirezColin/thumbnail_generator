import os
import aioboto3
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import asyncio
import httpx

app = FastAPI()

API_KEY = os.getenv('API_KEY')
api_key_header = APIKeyHeader(name="X-API-KEY")


class ErrorResponse(BaseModel):
    detail: str

def generate_thumbnail(image_file, size=(128, 128)):
    try:
        img = Image.open(image_file)
        img.thumbnail(size)
        thumbnail_io = BytesIO()
        img.save(thumbnail_io, format='JPEG')
        thumbnail_io.seek(0)
        return thumbnail_io
    except Exception as e:
        raise Exception(f"error generating thumbnail: {str(e)}")


async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credencials")
    return api_key

async def upload_to_s3(thumbnail_io, bucket_name, filename):
    async with aioboto3.client('s3') as s3_client:
        try:
             thumbnail_key = f'thumbnails/{filename}'
             await s3_client.upload_fileobj(thumbnail_io, bucket_name, thumbnail_key)
             return f'https://{bucket_name}.s3.amazonaws.com/{thumbnail_key}'
        except Exception as e:
            raise Exception(f"error uploading to s3: {str(e)}")
        
async def process_file(file: UploadFile,
                       bucket_name: str,
                       width: int, height: int)
    try:
        thumbnail_io = generate_thumbnail(file.file, size=(width, height))
        thumbnail_url = await upload_to_s3(thumbnail_io, bucket_name, file.filename)
        return {"filename": file.filename, 
                "thumbnail_url": thumbnail_url}
    except Exception as e:
        return {"filename": file.filename, 
                "error": str(e)}

@app.post("/upload/", response_model=dict, responses={500: {"model": ErrorResponse}})
async def upload_image(
    files: list[UploadFile] = File(...),
    width: int = 128, height: int = 128,
    apy_key: str = Depends(get_api_key)):

    bucket_name = os.getenv('S3_BUCKET')
    tasks = []

    for file in files:
        tasks.append(process_file(file, bucket_name, width, height))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    return {"thumbnails": results}

@app.get("/healthcheck/")
async def health_check():
    return {"status": "healthy"}