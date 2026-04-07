# Manufacturing QC Environment - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```bash
HF_TOKEN=hf_your_token_here
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
```

### 3. Test Locally

```bash
# Run tests
python test_env.py

# Start server
uvicorn server:app --reload

# In another terminal, test the API
curl -X POST http://localhost:7860/reset
```

### 4. Run Inference

```bash
# Run baseline inference
python inference.py

# Run specific task
export MANUFACTURING_QC_TASK=optimized_throughput
python inference.py
```

## 🐳 Docker Quick Start

```bash
# Build image
docker build -t manufacturing-qc-env .

# Run container
docker run -p 7860:7860 \
  -e HF_TOKEN=your_token \
  manufacturing-qc-env

# Test
curl http://localhost:7860/health
```

## 📤 Deploy to Hugging Face Spaces

### Option 1: Using Git

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Manufacturing QC Environment"

# Add Hugging Face remote
git remote add origin https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env

# Push
git push -u origin main
```

### Option 2: Upload Files Manually

1. Go to https://huggingface.co/new-space
2. Create a new Space with Docker SDK
3. Upload all files from this directory
4. Add secrets in Space settings:
   - `HF_TOKEN`
   - `API_BASE_URL`
   - `MODEL_NAME`

## ✅ Pre-Submission Checklist

Before submitting to the hackathon:

- [ ] All tests pass (`python test_env.py`)
- [ ] Docker builds successfully
- [ ] Server responds to `/reset` and `/step`
- [ ] Inference script runs without errors
- [ ] Structured logs follow [START]/[STEP]/[END] format
- [ ] All 3 tasks have working graders
- [ ] HF Space is deployed and accessible
- [ ] README is complete
- [ ] `.env.example` is included (not `.env`)

## 🔍 Validation

Run the official validation script:

```bash
# Your HF Space URL
SPACE_URL="https://YOUR_USERNAME-manufacturing-qc-env.hf.space"

# Download and run validator
curl -fsSL https://raw.githubusercontent.com/openenv/scripts/validate-submission.sh \
  | bash -s -- $SPACE_URL .
```

## 🎯 Task Details

### Basic Inspection (Easy)
- Duration: ~2 minutes
- Steps: 15
- Success: 70% score

```bash
export MANUFACTURING_QC_TASK=basic_inspection
python inference.py
```

### Optimized Throughput (Medium)
- Duration: ~4 minutes
- Steps: 25
- Success: 75% score

```bash
export MANUFACTURING_QC_TASK=optimized_throughput
python inference.py
```

### Adaptive Control (Hard)
- Duration: ~5 minutes
- Steps: 30
- Success: 80% score

```bash
export MANUFACTURING_QC_TASK=adaptive_control
python inference.py
```

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port is in use
lsof -i :7860

# Use different port
uvicorn server:app --port 8000
```

### Docker build fails
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t manufacturing-qc-env .
```

### Inference errors
```bash
# Check API key
echo $HF_TOKEN

# Test API endpoint
curl -X POST $API_BASE_URL/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"model":"$MODEL_NAME","messages":[{"role":"user","content":"test"}]}'
```

## 📞 Support

- Check the main README.md for detailed documentation
- Review error logs: `docker logs <container-id>`
- Test individual components with `test_env.py`

## 🎉 Submission

When ready to submit:

1. Ensure your HF Space is public and deployed
2. Get your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env`
3. Submit the URL in the hackathon form
4. Deadline: **TODAY** - don't miss it!

Good luck! 🍀
