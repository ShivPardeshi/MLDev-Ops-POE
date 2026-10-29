# ====================================================================
# Step 9: Pull lightweight python docker image
# Using python:3.11-alpine (~50 MB total image size)
# ====================================================================
FROM python:3.11-alpine

# Metadata labels
LABEL maintainer="MLOps Student Team"
LABEL description="Lightweight Docker image running hello.py for MLOps POE"

# Set working directory inside container
WORKDIR /app

# Ensure immediate console output streaming without buffering
ENV PYTHONUNBUFFERED=1

# ====================================================================
# Step 10: Add Hello.py to docker
# ====================================================================
COPY hello.py .

# Default command executed when container starts
CMD ["python", "hello.py"]
