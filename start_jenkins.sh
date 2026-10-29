#!/usr/bin/env bash
# Script to launch Jenkins using Docker with Docker socket mounted (Step 5 & 7)

set -e

CONTAINER_NAME="mlops-jenkins"
PORT="8080"

echo "================================================================="
echo "   MLOps POE - Starting Jenkins Automation Container            "
echo "================================================================="

# Check if container is already running
if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
    echo "[✓] Jenkins is already running at: http://localhost:${PORT}"
    echo "Initial Admin Password:"
    docker exec "${CONTAINER_NAME}" cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null || true
    exit 0
fi

# Check if stopped container exists
if [ "$(docker ps -aq -f status=exited -f name=${CONTAINER_NAME})" ]; then
    echo "[+] Restarting existing Jenkins container..."
    docker start "${CONTAINER_NAME}"
else
    echo "[+] Creating and starting new Jenkins container..."
    docker run -d \
      --name "${CONTAINER_NAME}" \
      -p "${PORT}:8080" \
      -p 50000:50000 \
      -v jenkins_home:/var/jenkins_home \
      -v /var/run/docker.sock:/var/run/docker.sock \
      jenkins/jenkins:lts
fi

echo "[+] Waiting for Jenkins to initialize (15 seconds)..."
sleep 15

echo "================================================================="
echo "[✓] Jenkins is up and running at: http://localhost:${PORT}"
echo "-----------------------------------------------------------------"
echo "Your Initial Admin Password is:"
docker exec "${CONTAINER_NAME}" cat /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null || echo "(Jenkins still initializing, please check in 10-15 seconds with: docker exec ${CONTAINER_NAME} cat /var/jenkins_home/secrets/initialAdminPassword)"
echo "================================================================="
