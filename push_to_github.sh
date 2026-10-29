#!/usr/bin/env bash
# Helper script to link and push to your GitHub remote repository (Step 4)

set -e

if [ -z "$1" ]; then
    echo "================================================================="
    echo "Usage: ./push_to_github.sh <YOUR_GITHUB_REPO_URL>"
    echo "Example: ./push_to_github.sh https://github.com/ShivPardeshi/mlops-internal-poe.git"
    echo "================================================================="
    exit 1
fi

REPO_URL="$1"

echo "[1/3] Adding remote origin: $REPO_URL..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

echo "[2/3] Setting branch to main..."
git branch -M main

echo "[3/3] Pushing commits to GitHub..."
git push -u origin main

echo "================================================================="
echo "[✓] SUCCESS: Project structure pushed to GitHub successfully!"
echo "================================================================="
