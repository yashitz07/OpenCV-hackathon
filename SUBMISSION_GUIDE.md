# 🚀 HACKATHON SUBMISSION GUIDE

## ⚡ URGENT - Steps to Submit Today

### Prerequisites Checklist
- [x] Project files created ✅
- [x] Tests passing ✅
- [ ] HuggingFace account (you need to create one)
- [ ] GitHub account (optional but recommended)
- [ ] API credentials (HF_TOKEN, API_BASE_URL)

---

## 🔥 FAST TRACK: 30-Minute Deployment

### Step 1: Get Your API Credentials (5 min)

1. **Get HuggingFace Token:**
   - Go to: https://huggingface.co/settings/tokens
   - Click "New token"
   - Name it: "manufacturing-qc-env"
   - Type: "Write"
   - Copy the token (starts with `hf_...`)

2. **Add credentials to .env:**
   ```bash
   nano .env
   ```
   
   Update the following line:
   ```
   HF_TOKEN=hf_your_actual_token_here
   ```
   
   Save and exit (Ctrl+X, then Y, then Enter)

---

### Step 2: Test Locally (5 min)

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies (if not already done)
pip install -r requirements.txt

# Test the environment
python3 test_env.py

# Test the server
uvicorn server:app --reload &

# Wait 5 seconds then test
sleep 5
curl -X POST http://localhost:7860/reset

# Stop the server
pkill -f uvicorn
```

---

### Step 3A: Deploy to HuggingFace Spaces (20 min) - RECOMMENDED

**Option 1: Web Upload (Easier)**

1. Go to: https://huggingface.co/new-space
2. Fill in:
   - **Space name:** `manufacturing-qc-env`
   - **License:** MIT
   - **SDK:** Docker
   - **Space hardware:** CPU basic (free)
3. Click "Create Space"
4. Upload ALL files from your tempo folder:
   - `manufacturing_qc_env.py`
   - `server.py`
   - `inference.py`
   - `app.py`
   - `Dockerfile`
   - `openenv.yaml`
   - `requirements.txt`
   - `README.md`
   - `LICENSE`
5. Go to Settings → Repository secrets
6. Add secrets:
   - Name: `HF_TOKEN`, Value: your token
   - Name: `API_BASE_URL`, Value: `https://router.huggingface.co/v1`
   - Name: `MODEL_NAME`, Value: `Qwen/Qwen2.5-72B-Instruct`
7. Wait 5-10 minutes for deployment
8. Test your space at: `https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env`

**Option 2: Git Push (Faster if you know Git)**

```bash
# Login to HuggingFace
pip install huggingface-hub
huggingface-cli login
# Paste your HF token when prompted

# Create a space on HuggingFace.co first (see Option 1, steps 1-3)
# Then clone it
cd ..
git clone https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env
cd manufacturing-qc-env

# Copy all files from tempo
cp ../tempo/*.py .
cp ../tempo/*.yaml .
cp ../tempo/*.txt .
cp ../tempo/*.md .
cp ../tempo/Dockerfile .
cp ../tempo/LICENSE .

# Commit and push
git add .
git commit -m "Initial commit: Manufacturing QC Environment"
git push

# Add secrets via web interface (see Option 1, steps 5-6)
```

---

### Step 3B: Create GitHub Repository (Optional, 10 min)

```bash
# Initialize git
git init

# Create .gitignore (already exists)
# Add all files
git add .

# Commit
git commit -m "Initial commit: Manufacturing QC Environment for OpenEnv Hackathon"

# Create a new repository on GitHub.com:
# 1. Go to https://github.com/new
# 2. Name: manufacturing-qc-env
# 3. Public repository
# 4. Do NOT initialize with README (we have one)
# 5. Click "Create repository"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/manufacturing-qc-env.git

# Push
git branch -M main
git push -u origin main
```

---

### Step 4: Validate Your Submission (5 min)

Once your HuggingFace Space is deployed:

```bash
# Get your Space URL
SPACE_URL="https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env"

# Test it's responding
curl -X POST "$SPACE_URL/reset" \
  -H "Content-Type: application/json" \
  -d '{"task": "basic_inspection"}'

# You should see JSON output with observation data
```

**Manual validation checks:**

✅ Space is live and shows "Running"  
✅ Can access the Space at the URL  
✅ `/reset` endpoint returns 200  
✅ `/health` endpoint returns healthy  
✅ No build errors in Space logs  

---

### Step 5: Submit to Hackathon

1. Copy your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env`
2. Go to the hackathon submission form
3. Paste your URL
4. Submit before the deadline!

---

## 🔍 Troubleshooting

### Problem: Space build failed

**Solution:**
1. Check Dockerfile syntax
2. Ensure all imports in Python files are correct
3. Check Space logs for specific error
4. Verify all files were uploaded

### Problem: Space times out

**Solution:**
1. Check if container is running in Space logs  
2. Verify port 7860 is exposed in Dockerfile  
3. Wait a few more minutes (first build can take 10-15 min)

### Problem: Reset returns error

**Solution:**
1. Check Space secrets are set correctly
2. Verify Dockerfile CMD is: `uvicorn server:app --host 0.0.0.0 --port 7860`
3. Check server.py has no syntax errors

### Problem: Can't login to HuggingFace

**Solution:**
```bash
# Logout and login again
huggingface-cli logout
huggingface-cli login

# Or set token directly
export HF_TOKEN=your_token_here
```

---

## 📋 Final Pre-Submission Checklist

Before you submit, verify:

- [ ] HuggingFace Space is deployed and "Running"
- [ ] Space URL is accessible in browser
- [ ] `/reset` endpoint works (returns 200)
- [ ] `/health` endpoint works
- [ ] All 3 tasks are defined (basic_inspection, optimized_throughput, adaptive_control)
- [ ] Dockerfile builds without errors
- [ ] No secrets (tokens/keys) committed to repository
- [ ] README.md is complete
- [ ] LICENSE file included
- [ ] openenv.yaml is valid

---

## 🎯 Your Space URL Format

Your submission URL will be:
```
https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env
```

Replace `YOUR_USERNAME` with your actual HuggingFace username.

---

## ⏰ Time Management

| Task | Time | Status |
|------|------|--------|
| Get API credentials | 5 min | ⬜ |
| Test locally | 5 min | ⬜ |
| Deploy to HF Spaces | 20 min | ⬜ |
| Validate deployment | 5 min | ⬜ |
| Submit to hackathon | 5 min | ⬜ |
| **TOTAL** | **40 min** | |

---

## 🆘 Emergency Contacts

If you run into issues:
- HuggingFace Docs: https://huggingface.co/docs/hub/spaces
- OpenEnv Discord: [Check hackathon page]
- GitHub Issues: [Your repo]/issues

---

## 🎉 After Submission

Once submitted:
1. ✅ Celebrate! You built a complete OpenEnv environment! 🎊
2. 📱 Save your Space URL
3. 📊 Monitor your Space logs 
4. 🔄 Keep your Space running until judging is complete
5. 🌟 Star your own repo on GitHub

---

**Good luck! You've got this! 🚀🏆**
