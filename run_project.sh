#!/usr/bin/env bash
# ==============================================================================
# MLOps Internal POE - End-to-End Project Execution Runner
# Runs Hello Application, Pytest Suite, Evidently Monitoring & Docker Container
# ==============================================================================

set -e

# Change directory to project root
cd "$(dirname "$0")"

PYTHON_BIN=".venv/bin/python"
PYTEST_BIN=".venv/bin/pytest"

# Fallback to system python3 if venv is missing
if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

echo "================================================================="
echo "       🚀 EXECUTING COMPLETE MLOps INTERNAL POE PIPELINE        "
echo "================================================================="
echo "Working Directory : $(pwd)"
echo "Python Executable : $PYTHON_BIN"
echo "Date / Time       : $(date)"
echo "================================================================="
echo ""

# ------------------------------------------------------------------------------
# STEP 2: RUN HELLO APPLICATION
# ------------------------------------------------------------------------------
echo ">>> [STAGE 1/4] Running Single-File Application (hello.py) <<<"
$PYTHON_BIN hello.py
echo "[✓] hello.py executed successfully."
echo ""

# ------------------------------------------------------------------------------
# STEP 11: CONFIGURE PYTEST & PRINT 1 TEST CASE
# ------------------------------------------------------------------------------
echo ">>> [STAGE 2/4] Running Pytest Suite with Test Case Prints <<<"
if [ -f "$PYTEST_BIN" ]; then
    $PYTEST_BIN -s -v
else
    $PYTHON_BIN -m pytest -s -v
fi
echo "[✓] Pytest test cases passed."
echo ""

# ------------------------------------------------------------------------------
# STEP 12: RUN EVIDENTLY MONITORING & DRIFT DETECTION
# ------------------------------------------------------------------------------
echo ">>> [STAGE 3/4] Running Evidently AI Drift Detection & Quality Monitoring <<<"
$PYTHON_BIN evidently_monitor.py
echo "[✓] Evidently AI reports generated in ./evidently_reports/"
echo ""

# ------------------------------------------------------------------------------
# STEPS 9 & 10: DOCKER CONTAINER BUILD & RUN
# ------------------------------------------------------------------------------
echo ">>> [STAGE 4/4] Building & Running Lightweight Alpine Docker Container <<<"
if command -v docker &> /dev/null && docker ps &> /dev/null; then
    docker build -t hello-mlops:alpine .
    echo "[+] Running Container (hello-mlops:alpine):"
    docker run --rm hello-mlops:alpine
    echo "[✓] Container executed successfully."
else
    echo "[!] Docker daemon not reachable. Skipped Docker stage (start Docker Desktop to enable)."
fi

echo ""
echo "================================================================="
echo "   🎉 ALL MLOps POE PIPELINE STAGES COMPLETED SUCCESSFULLY!     "
echo "================================================================="
