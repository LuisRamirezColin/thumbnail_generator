# Stage 1: Install Poetry and export requirements
FROM public.ecr.aws/lambda/python:3.12 AS poetrytask
WORKDIR /app

# Copy pyproject.toml for Poetry
COPY pyproject.toml ./ 

# Install Poetry
RUN pip install poetry

# Export requirements.txt
RUN poetry export --without-hashes -f requirements.txt --output requirements.txt

# Stage 2: Build the application
FROM public.ecr.aws/lambda/python:3.12
WORKDIR /var/task
  # Change the working directory to where Lambda expects code

# Copy the exported requirements and application files
COPY --from=poetrytask /app/requirements.txt ./
COPY thumbnail ./thumbnail 
 # Assuming your FastAPI app is in a directory named 'thumbnail'

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for the application
ENV APP_MODE=production

# Use the Mangum handler as the entry point
CMD ["thumbnail.main.handler"]