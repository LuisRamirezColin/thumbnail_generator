import os
import pytest
from fastapi.testclient import TestClient
from thumbnail.api.app import app

os.environ['S3_BUCKET'] = 'test-bucket'
os.environ['API_KEY'] = 'test_api_key'


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    response = client.get("/healthcheck/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_upload_valid_image(client):
    with open("tests/test_image.jpg", "rb") as image_file:
        response = client.post(
            "/upload/",
            headers={"X-API-KEY": "test_api_key"},
            files={"files": ("test_image.jpg", image_file, "image/jpg")},
            data={"width": 200, "height": 200}
        )
    assert response.status_code == 200
    assert "thumbnails" in response.json()

def test_upload_invalid_file():
    response = client.post(
            "/upload/",
            headers={"X-API-KEY": "test_api_key"},
            files={"files": ("invalid_image.jpg", "not an image", "text/plain")},
        )
    assert response.status_code == 500
    assert "error" in response.json()[0]

def test_generate_thumbnail_bucket_not_found():
    with open("tests/test_image.jpg", "rb") as image_file:
        response = client.post(
            "/upload/",
            files={"files": ("test_image.jpg", image_file, "image/jpg")},
            data={"width": 200, "height": 200}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Could not validate credentials"}

