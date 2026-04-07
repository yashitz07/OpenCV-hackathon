#!/bin/bash
# Quick deployment script for HuggingFace Spaces

set -e

echo "=========================================="
echo "Manufacturing QC - HuggingFace Deployment"
echo "=========================================="
echo ""

# Get username
read -p "Enter your HuggingFace username: " HF_USERNAME

if [ -z "$HF_USERNAME" ]; then
    echo "Error: Username cannot be empty"
    exit 1
fi

REPO_NAME="manufacturing-qc-env"
SPACE_URL="https://huggingface.co/spaces/$HF_USERNAME/$REPO_NAME"

echo ""
echo "Space URL will be: $SPACE_URL"
echo ""

# Check if huggingface-hub is installed
if ! python3 -c "import huggingface_hub" 2>/dev/null; then
    echo "Installing huggingface-hub..."
    pip install huggingface-hub
fi

# Login
echo ""
echo "Please login to HuggingFace (you'll need your token from https://huggingface.co/settings/tokens):"
huggingface-cli login

echo ""
echo "=========================================="
echo "Deploying to HuggingFace Spaces..."
echo "=========================================="
echo ""

# Create temp directory
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

# Clone or create space
echo "Setting up Space repository..."
if huggingface-cli repo create "$REPO_NAME" --type space --space_sdk docker 2>/dev/null; then
    echo "✓ Space created successfully"
else
    echo "! Space may already exist, continuing..."
fi

# Clone the space
git clone "https://huggingface.co/spaces/$HF_USERNAME/$REPO_NAME.git" .

# Copy files
echo "Copying files..."
cp "$OLDPWD"/*.py . 2>/dev/null || true
cp "$OLDPWD"/*.yaml . 2>/dev/null || true
cp "$OLDPWD"/*.txt . 2>/dev/null || true
cp "$OLDPWD"/*.md . 2>/dev/null || true
cp "$OLDPWD"/Dockerfile . 2>/dev/null || true
cp "$OLDPWD"/LICENSE . 2>/dev/null || true

# Create README for HF Spaces
cat > README.md << 'EOF'
---
title: Manufacturing QC Environment
emoji: 🏭
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
license: mit
tags:
  - openenv
  - manufacturing
  - quality-control
  - reinforcement-learning
---

# Manufacturing Quality Control Environment

A real-world OpenEnv environment for AI agents to learn manufacturing quality control.

## Features
- 3 tasks with increasing difficulty
- Real-world product inspection simulation
- Defect detection and routing decisions
- Adaptive quality control mechanisms

## API Endpoints
- POST `/reset` - Reset environment
- POST `/step` - Take action
- GET `/state` - Get current state
- GET `/health` - Health check

## Tasks
1. **Basic Inspection** (Easy) - Identify obvious defects
2. **Optimized Throughput** (Medium) - Balance quality and speed
3. **Adaptive Control** (Hard) - Dynamic threshold adjustment

For full documentation, see the GitHub repository.
EOF

# Commit and push
echo "Committing files..."
git add .
git commit -m "Deploy Manufacturing QC Environment" || true

echo "Pushing to HuggingFace Spaces..."
git push

cd "$OLDPWD"
rm -rf "$TEMP_DIR"

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Your Space URL: $SPACE_URL"
echo ""
echo "Next steps:"
echo "1. Wait 5-10 minutes for the Space to build"
echo "2. Add secrets in Space settings:"
echo "   - HF_TOKEN"
echo "   - API_BASE_URL"
echo "   - MODEL_NAME"
echo "3. Test with: curl -X POST $SPACE_URL/reset"
echo "4. Submit your Space URL to the hackathon!"
echo ""
echo "Monitor build: $SPACE_URL/settings"
echo ""
