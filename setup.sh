#!/bin/bash
# Setup script for Manufacturing QC Environment

set -e

echo "=========================================="
echo "Manufacturing QC Environment Setup"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 10 ]; then
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION detected"
else
    echo -e "${RED}✗${NC} Python 3.10+ required, found $PYTHON_VERSION"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv .venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${YELLOW}!${NC} Please edit .env and add your API keys:"
    echo "   - HF_TOKEN (required for inference)"
    echo "   - API_BASE_URL (already set)"
    echo "   - MODEL_NAME (already set)"
else
    echo -e "${GREEN}✓${NC} .env file already exists"
fi

# Check Docker
echo ""
echo "Checking Docker installation..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | sed 's/,//')
    echo -e "${GREEN}✓${NC} Docker $DOCKER_VERSION detected"
else
    echo -e "${YELLOW}!${NC} Docker not found (optional, needed for deployment)"
fi

# Check Git
echo ""
echo "Checking Git installation..."
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    echo -e "${GREEN}✓${NC} Git $GIT_VERSION detected"
else
    echo -e "${YELLOW}!${NC} Git not found (optional, needed for version control)"
fi

# Run tests
echo ""
echo "=========================================="
read -p "Run tests to verify installation? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running tests..."
    python test_env.py
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Setup complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Configure your environment:"
echo "   ${YELLOW}nano .env${NC}  # Add your HF_TOKEN"
echo ""
echo "2. Run local tests:"
echo "   ${YELLOW}python test_env.py${NC}"
echo ""
echo "3. Start the server:"
echo "   ${YELLOW}uvicorn server:app --reload${NC}"
echo ""
echo "4. Run inference:"
echo "   ${YELLOW}python inference.py${NC}"
echo ""
echo "5. Build Docker image:"
echo "   ${YELLOW}docker build -t manufacturing-qc-env .${NC}"
echo ""
echo "6. Deploy to Hugging Face:"
echo "   ${YELLOW}huggingface-cli login${NC}"
echo "   ${YELLOW}git push${NC}"
echo ""
echo "For detailed instructions, see README.md"
echo ""
