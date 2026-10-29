# Docker Setup & Containerization Guide (Steps 8, 9, 10)

This guide documents the Docker installation, pulling a lightweight Python image, containerizing `hello.py`, and verifying execution.

---

## 1. Step 8: Install Docker

### On macOS:
1. Docker Desktop can be downloaded from the official website:
   - [Download Docker Desktop for Mac (Apple Silicon / Intel)](https://www.docker.com/products/docker-desktop/)
   - Or via Homebrew:
     ```bash
     brew install --cask docker
     ```
2. Start Docker Desktop from Applications or run:
   ```bash
   open -a Docker
   ```
3. Verify installation:
   ```bash
   docker --version
   docker ps
   ```

### On Ubuntu / Linux:
```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
```

---

## 2. Step 9: Pull Lightweight Python Docker Image

To minimize image size, resource usage, and attack surface, we use Alpine Linux base images:

```bash
docker pull python:3.11-alpine
```

### Image Size Comparison:
| Image Tag | Base OS | Approximate Size | Selection |
| :--- | :--- | :--- | :--- |
| `python:3.11` | Debian Bookworm | ~1.0 GB | Heavy |
| `python:3.11-slim` | Debian Minimal | ~150 MB | Moderate |
| **`python:3.11-alpine`** | **Alpine Linux 3.x** | **~50 MB** | **Selected (Lightweight)** |

Verify the downloaded image:
```bash
docker images | grep python
```

---

## 3. Step 10: Add Hello.py to Docker

The containerization is defined in [Dockerfile](file:///Users/shivpardeshi/Downloads/MLOps%20Internal%20POE/Dockerfile):

```dockerfile
# Step 9: Pull lightweight python docker image
FROM python:3.11-alpine

# Set working directory inside container
WORKDIR /app

# Ensure output streams without buffering
ENV PYTHONUNBUFFERED=1

# Step 10: Add hello.py to container
COPY hello.py .

# Execute hello.py on container startup
CMD ["python", "hello.py"]
```

### Build the Docker Image:
```bash
docker build -t hello-mlops:alpine .
```

### Run the Container:
```bash
docker run --rm hello-mlops:alpine
```

### Expected Output:
```text
============================================================
   MLOps POE - Hello Application   
============================================================
[Application Output] Hello, DevOps Engineer! Welcome to the MLOps POE Pipeline.
[Model/Metric Output] Input: 4.0 -> Prediction: 8.0
============================================================
```
