# 🚀 HACKATHON SUBMISSION WORKFLOW

## 📦 Files Ready for Transfer

Your project archive is ready: `/Users/yashpa/tempo-manufacturing-qc.tar.gz` (31KB)

---

## 🔄 TRANSFER & SETUP ON OTHER LAPTOP

### Step 1: Transfer the Archive

**Choose one method:**

**A. Using USB Drive:**
```bash
# On THIS laptop (copy to USB)
cp /Users/yashpa/tempo-manufacturing-qc.tar.gz /Volumes/YOUR_USB/

# On OTHER laptop (extract from USB)
cp /Volumes/YOUR_USB/tempo-manufacturing-qc.tar.gz ~/
cd ~
tar -xzf tempo-manufacturing-qc.tar.gz
cd tempo
```

**B. Using Cloud (Google Drive, Dropbox, etc):**
1. Upload `/Users/yashpa/tempo-manufacturing-qc.tar.gz` to cloud
2. Download on other laptop
3. Extract:
```bash
cd ~/Downloads
tar -xzf tempo-manufacturing-qc.tar.gz
cd tempo
```

**C. Using Email:**
1. Email the archive to yourself (it's only 31KB!)
2. Download on other laptop
3. Extract as above

---

## 🔧 SETUP ON OTHER LAPTOP (5 minutes)

### 1. Install Prerequisites

```bash
# Check Python version (need 3.10+)
python3 --version

# Check Git
git --version

# Check Docker (optional)
docker --version
```

### 2. Setup Project

```bash
cd tempo

# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate  # On Mac/Linux
# OR
.venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Install git and huggingface CLI
pip install huggingface-hub
```

### 3. Configure Credentials

```bash
# Copy environment template
cp .env.example .env

# Edit with your credentials
nano .env
# Or use: code .env (VS Code)
# Or use: open -e .env (TextEdit on Mac)
```

Add your tokens:
```env
HF_TOKEN=hf_your_actual_token_here
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
```

### 4. Test Everything Works

```bash
# Run tests
python3 test_env.py

# Should see: ✅ ALL TESTS PASSED!
```

---

## 📤 GITHUB REPOSITORY SETUP (10 minutes)

### Option A: Create via GitHub Website (Easiest)

1. **Go to:** https://github.com/new

2. **Fill in:**
   - Repository name: `manufacturing-qc-env`
   - Description: `Manufacturing Quality Control OpenEnv Environment for Hackathon`
   - Visibility: **Public** ⚠️ Important!
   - ❌ Do NOT initialize with README (we have one)

3. **Click "Create repository"**

4. **In your terminal (OTHER laptop):**
```bash
cd tempo

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Manufacturing QC Environment for OpenEnv Hackathon"

# Add remote (REPLACE YOUR_GITHUB_USERNAME)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/manufacturing-qc-env.git

# Push
git branch -M main
git push -u origin main
```

### Option B: Using GitHub CLI (Faster if installed)

```bash
# Install GitHub CLI first
brew install gh  # Mac
# OR download from: https://cli.github.com/

# Login
gh auth login

# Create and push in one go
cd tempo
git init
git add .
git commit -m "Initial commit: Manufacturing QC Environment"
gh repo create manufacturing-qc-env --public --source=. --remote=origin --push
```

---

## 🤗 HUGGING FACE SPACES DEPLOYMENT (15 minutes)

### Step 1: Login to Hugging Face

```bash
# Login via CLI
huggingface-cli login
# Paste your HF token when prompted
```

### Step 2: Create Space

**Option A: Using Web Interface (Recommended)**

1. Go to: https://huggingface.co/new-space

2. Fill in:
   - **Owner:** Your HF username
   - **Space name:** `manufacturing-qc-env`
   - **License:** MIT
   - **Select SDK:** **Docker** ⚠️ CRITICAL!
   - **Space hardware:** CPU basic (free)

3. Click **"Create Space"**

4. **Upload files via web:**
   - Go to "Files" tab
   - Click "Add file" → "Upload files"
   - Upload these files (you can drag & drop):
     - ✅ app.py
     - ✅ Dockerfile  
     - ✅ inference.py
     - ✅ LICENSE
     - ✅ manufacturing_qc_env.py
     - ✅ openenv.yaml
     - ✅ README.md
     - ✅ requirements.txt
     - ✅ server.py

5. **Add secrets:**
   - Go to "Settings" tab
   - Scroll to "Repository secrets"
   - Click "New secret" for each:
     - Name: `HF_TOKEN`, Value: `hf_your_token`
     - Name: `API_BASE_URL`, Value: `https://router.huggingface.co/v1`
     - Name: `MODEL_NAME`, Value: `Qwen/Qwen2.5-72B-Instruct`

**Option B: Using Git (Alternative)**

```bash
cd tempo

# Add HF remote
git remote add hf https://huggingface.co/spaces/YOUR_HF_USERNAME/manufacturing-qc-env

# Push
git push hf main

# Then add secrets via web interface (see Option A step 5)
```

### Step 3: Wait for Build

- Go to your Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env`
- Check "Building" tab
- Wait 10-15 minutes for first build
- Status should change to "Running" ✅

---

## ✅ VALIDATION BEFORE SUBMISSION (5 minutes)

### Test Your Deployed Space

```bash
# Replace YOUR_USERNAME with your HF username
SPACE_URL="https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env"

# Test health endpoint
curl $SPACE_URL/health

# Expected: {"status":"healthy","service":"manufacturing-qc-env"}

# Test reset endpoint
curl -X POST $SPACE_URL/reset \
  -H "Content-Type: application/json" \
  -d '{"task":"basic_inspection"}'

# Expected: JSON with observation data

# Test step endpoint
curl -X POST $SPACE_URL/step \
  -H "Content-Type: application/json" \
  -d '{
    "action": {
      "action_type": "approve",
      "product_id": "TEST-001",
      "reason": "Testing submission"
    }
  }'

# Expected: JSON with observation, reward, done, info
```

### Checklist

- [ ] GitHub repo is public and accessible
- [ ] GitHub repo URL: `https://github.com/YOUR_USERNAME/manufacturing-qc-env`
- [ ] HF Space shows "Running" status
- [ ] HF Space URL: `https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env`
- [ ] `/health` endpoint returns 200
- [ ] `/reset` endpoint returns valid observation
- [ ] `/step` endpoint works correctly
- [ ] All files are present in both repos
- [ ] No `.env` file in repos (secrets only in HF settings)

---

## 📝 SUBMIT TO HACKATHON

### Your Submission URLs

Fill in the form with:

1. **GitHub Repository URL:**
   ```
   https://github.com/YOUR_GITHUB_USERNAME/manufacturing-qc-env
   ```

2. **Hugging Face Space URL:**
   ```
   https://huggingface.co/spaces/YOUR_HF_USERNAME/manufacturing-qc-env
   ```

### Before Hitting Submit

Double-check:
- ✅ Both URLs are accessible in incognito/private browser window
- ✅ GitHub repo shows all files
- ✅ HF Space is "Running" (not "Building" or "Error")
- ✅ You can call the API endpoints successfully

### Submit!

1. Go to hackathon submission form
2. Paste your GitHub URL
3. Paste your HF Space URL
4. Click Submit! 🎉

---

## 🔍 TROUBLESHOOTING

### Problem: Git push asks for username/password

**Solution:**
```bash
# Use personal access token for GitHub
# Create token at: https://github.com/settings/tokens
# Then use:
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/manufacturing-qc-env.git
```

### Problem: HF Space build fails

**Solution:**
1. Check "Building" logs in HF Space
2. Verify all files uploaded correctly
3. Check Dockerfile syntax
4. Ensure secrets are set correctly
5. Rebuild: Settings → "Factory Reboot"

### Problem: Can't access /reset endpoint

**Solution:**
1. Ensure Space is "Running" (not just started)
2. Wait 2-3 minutes after "Running" status
3. Check Space logs for errors
4. Verify secrets are set (HF_TOKEN, etc.)

### Problem: Files too large

**Solution:**
Our project is only 31KB - this shouldn't be an issue!

---

## ⏱️ TIMELINE

| Task | Time | Running Total |
|------|------|---------------|
| Transfer archive | 2 min | 2 min |
| Setup on other laptop | 5 min | 7 min |
| GitHub repo setup | 10 min | 17 min |
| HF Spaces deployment | 15 min | 32 min |
| Validation | 5 min | 37 min |
| **Build wait time** | 10 min | 47 min |
| Final submission | 3 min | **50 min total** |

**Actual hands-on time:** ~40 minutes  
**Waiting time:** ~10 minutes (Space build)

---

## 📞 QUICK REFERENCE

### Important URLs

- **GitHub new repo:** https://github.com/new
- **GitHub tokens:** https://github.com/settings/tokens
- **HF new space:** https://huggingface.co/new-space
- **HF tokens:** https://huggingface.co/settings/tokens

### Key Commands

```bash
# Extract archive
tar -xzf tempo-manufacturing-qc.tar.gz

# Setup environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Test
python3 test_env.py

# Git setup
git init && git add . && git commit -m "Initial commit"
git remote add origin https://github.com/USER/repo.git
git push -u origin main

# HF login
huggingface-cli login
```

---

## 🎉 SUCCESS CRITERIA

You're ready to submit when:

✅ Archive transferred successfully  
✅ Project runs on other laptop  
✅ Tests pass: `python3 test_env.py`  
✅ GitHub repo is public with all files  
✅ HF Space is "Running"  
✅ API endpoints respond correctly  
✅ Both URLs accessible publicly  

---

**You've got everything ready! Just transfer, setup, and submit! 🚀**

**Estimated total time:** 50 minutes (including build wait time)

Good luck! 🏆
