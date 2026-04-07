#!/bin/bash
# Quick Transfer & Submit Script
# Run this on your OTHER LAPTOP after extracting the archive

set -e

echo "=========================================="
echo "Manufacturing QC - Transfer Setup"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Step 1: Check prerequisites
echo "Checking prerequisites..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.10+"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python3 found"

if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git"
    exit 1
fi
echo -e "${GREEN}✓${NC} Git found"

# Step 2: Setup virtual environment
echo ""
echo "Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"

# Step 3: Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
pip install -q huggingface-hub
echo -e "${GREEN}✓${NC} Dependencies installed"

# Step 4: Setup .env
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${YELLOW}!${NC} Please edit .env and add your credentials:"
    echo "   nano .env"
    echo ""
    read -p "Press Enter after you've updated .env file..."
else
    echo -e "${GREEN}✓${NC} .env file exists"
fi

# Step 5: Run tests
echo ""
echo "Running tests..."
if python3 test_env.py > /tmp/test_output.txt 2>&1; then
    echo -e "${GREEN}✓${NC} All tests passed!"
else
    echo "❌ Tests failed. Check the output:"
    cat /tmp/test_output.txt
    exit 1
fi

# Step 6: Get user info
echo ""
echo "=========================================="
echo "GitHub & HuggingFace Setup"
echo "=========================================="
echo ""

read -p "Enter your GitHub username: " GITHUB_USER
read -p "Enter your HuggingFace username: " HF_USER

if [ -z "$GITHUB_USER" ] || [ -z "$HF_USER" ]; then
    echo "❌ Usernames cannot be empty"
    exit 1
fi

GITHUB_URL="https://github.com/$GITHUB_USER/manufacturing-qc-env"
HF_URL="https://huggingface.co/spaces/$HF_USER/manufacturing-qc-env"

echo ""
echo "Your URLs will be:"
echo "GitHub: $GITHUB_URL"
echo "HF Space: $HF_URL"
echo ""

# Step 7: GitHub setup
echo "=========================================="
echo "Step 1: GitHub Repository Setup"
echo "=========================================="
echo ""
echo "Please complete these steps:"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: manufacturing-qc-env"
echo "3. Set to PUBLIC"
echo "4. Do NOT initialize with README"
echo "5. Click 'Create repository'"
echo ""
read -p "Press Enter when repository is created..."

echo ""
echo "Initializing Git..."
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit: Manufacturing QC Environment for OpenEnv Hackathon"
    echo -e "${GREEN}✓${NC} Git initialized and committed"
else
    echo -e "${GREEN}✓${NC} Git already initialized"
fi

echo ""
echo "Adding GitHub remote..."
git remote add origin "https://github.com/$GITHUB_USER/manufacturing-qc-env.git" 2>/dev/null || echo "Remote already exists"

echo ""
echo "Pushing to GitHub..."
echo "You may need to enter your GitHub credentials or token"
git branch -M main
git push -u origin main

echo -e "${GREEN}✓${NC} Pushed to GitHub!"

# Step 8: HF Spaces setup
echo ""
echo "=========================================="
echo "Step 2: HuggingFace Spaces Setup"
echo "=========================================="
echo ""
echo "Please complete these steps:"
echo ""
echo "1. Go to: https://huggingface.co/new-space"
echo "2. Space name: manufacturing-qc-env"
echo "3. SDK: Docker (IMPORTANT!)"
echo "4. Click 'Create Space'"
echo "5. Upload these files:"
echo "   - app.py, Dockerfile, inference.py"
echo "   - LICENSE, manufacturing_qc_env.py"
echo "   - openenv.yaml, README.md"
echo "   - requirements.txt, server.py"
echo "6. Go to Settings → Repository secrets"
echo "7. Add secrets:"
echo "   - HF_TOKEN: your token"
echo "   - API_BASE_URL: https://router.huggingface.co/v1"
echo "   - MODEL_NAME: Qwen/Qwen2.5-72B-Instruct"
echo ""
read -p "Press Enter when Space is created and secrets are added..."

echo ""
echo "=========================================="
echo "Step 3: Validation"
echo "=========================================="
echo ""
echo "Waiting for Space to build (this takes 10-15 minutes)..."
echo "Check status at: $HF_URL"
echo ""
read -p "Press Enter when Space status shows 'Running'..."

echo ""
echo "Testing endpoints..."

# Test health endpoint
echo -n "Testing /health... "
if curl -s "$HF_URL/health" | grep -q "healthy"; then
    echo -e "${GREEN}✓${NC}"
else
    echo "❌ Failed"
fi

# Test reset endpoint
echo -n "Testing /reset... "
if curl -s -X POST "$HF_URL/reset" \
    -H "Content-Type: application/json" \
    -d '{"task":"basic_inspection"}' | grep -q "observation"; then
    echo -e "${GREEN}✓${NC}"
else
    echo "❌ Failed"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ SETUP COMPLETE!${NC}"
echo "=========================================="
echo ""
echo "Your submission URLs:"
echo ""
echo "GitHub Repository:"
echo "  $GITHUB_URL"
echo ""
echo "HuggingFace Space:"
echo "  $HF_URL"
echo ""
echo "Copy these URLs and submit them to the hackathon form!"
echo ""
echo "Final checklist:"
echo "- [ ] GitHub repo is public"
echo "- [ ] HF Space shows 'Running'"
echo "- [ ] Both URLs work in incognito browser"
echo "- [ ] API endpoints respond correctly"
echo ""
echo "Good luck! 🚀"
echo ""
