# FastAPI Thumbnail Generator

## Overview

The FastAPI Thumbnail Generator is a serverless application designed to generate thumbnails from base images using AWS Lambda and Docker. This project utilizes FastAPI to handle HTTP requests and is deployed on AWS using the Serverless Application Model (SAM).

## Features

- **Thumbnail Generation**: Upload images and receive generated thumbnails.
- **Health Check Endpoint**: Monitor the health of the service.
- **Secure Data Endpoint**: Access secure data with appropriate authentication.
- **CORS Support**: Allows cross-origin requests from any origin.

## Architecture

The application is structured as follows:

- **FastAPI**: The web framework used to build the API.
- **AWS Lambda**: The compute service that runs the application in a serverless environment.
- **Docker**: Used for containerizing the application for deployment on AWS Lambda.
- **Amazon S3**: (Optional) Storage for uploaded images and generated thumbnails.

## Prerequisites

- AWS Account
- Docker installed on your machine
- AWS CLI installed and configured
- Python 3.12 or higher
- Poetry for dependency management

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/LuisRamirezColin/thumbnail-generator.git
cd thumbnail-generator
```
Create a virtualenvironment

```bash
   virtualenv .venv
   source .venv/bin/activate
```
OR

```bash
   poetry shell
```
### 2. Install Dependencies

Using Poetry, install the required dependencies:
```bash
   poetry install
```
### 3. Build the Docker Image and publish over ECR
Build the Docker image for your FastAPI application:
```bash
   docker build -t thumbnail-fastapi-app .
```
OR
```bash
   DOCKER_BUILDKIT=0 docker build -t thumbnail-fastapi-app .
```

login ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 440744260607.dkr.ecr.us-east-1.amazonaws.com
```

Tag Image
```bash
   docker tag thumbnail-fastapi-app:latest 440744260607.dkr.ecr.us-east-1.amazonaws.com/thumbnail-fastapi-app:latest
```

Push Image registry
```bash
   docker push 440744260607.dkr.ecr.us-east-1.amazonaws.com/thumbnail-fastapi-app:latest.
```

### 4. Deploy to AWS
Use AWS SAM to deploy the application:
```bash
   sam validate
```
Package the application:
```bash
   sam build
```
Deploy the application:
```bash
   sam deploy --guided
```
### 5. Access the API
Once deployed, you can access the API endpoints:

Upload Image: POST /upload
Health Check: GET /health
Secure Data: GET /secure

### 6. Local Development
To run the application locally for testing, you can use:
```bash
   poetry run python run.py
```
### 7. Environment Variables
The application uses the following environment variables:

APP_MODE: Set to "production" for deployment.
DEBUG: Set to "true" or "false" for debugging mode.
S3_BUCKET: The name of the S3 bucket for storing images.
API_KEY: Your API key for secure endpoints.

### usage

### LOCAL  REQUEST
```bash
curl -X POST "http://localhost:8000/upload/images" \
-H "Content-Type: multipart/form-data" \
-H "X-API-KEY: my_stori_api_key" \
-F "file=@./tests/test_image_2.jpg"
```

### Response
```json
{"filename":"test_image:2.jpg","thumbnail_url":"/thumbnails/test_image:2.jpg","error":null}
```

### PROD REQUEST 
```bash
curl -X POST "https://g6b01c0hd2.execute-api.us-east-1.amazonaws.com/Prodhttp://localhost:8000/upload/images" \
-H "Content-Type: multipart/form-data" \
-H "X-API-KEY: my_stori_api_key" \
-F "file=@./tests/test_image.jpg"
```

### Response
```json
{"filename":"test_image.jpg","thumbnail_url":"/thumbnails/test_image.jpg","error":null}
```
