# Use a smaller base image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (optimizes caching)
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Now copy only the app files
COPY ./app ./app

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
