# ✅ DEPLOYMENT CHECKLIST

Use this checklist to track your progress to submission!

## 📋 Pre-Deployment Setup

- [ ] Virtual environment activated
  ```bash
  source .venv/bin/activate
  ```

- [ ] Dependencies installed
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Tests passing
  ```bash
  python3 test_env.py
  ```
  Expected: All tests pass ✅

- [ ] Have HuggingFace account
  - URL: https://huggingface.co/join

- [ ] Have HuggingFace Write token
  - Get from: https://huggingface.co/settings/tokens
  - Copy token (starts with `hf_...`)

- [ ] Updated .env file with credentials
  ```bash
  nano .env
  # Set HF_TOKEN=hf_your_actual_token
  ```

## 🐳 Local Docker Testing (Optional but Recommended)

- [ ] Docker installed
  ```bash
  docker --version
  ```

- [ ] Docker build succeeds
  ```bash
  docker build -t manufacturing-qc-env .
  ```
  Expected: "Successfully tagged manufacturing-qc-env:latest"

- [ ] Docker run works
  ```bash
  docker run -p 7860:7860 -e HF_TOKEN=$HF_TOKEN manufacturing-qc-env
  ```

- [ ] Can access in another terminal
  ```bash
  curl http://localhost:7860/health
  ```
  Expected: `{"status":"healthy","service":"manufacturing-qc-env"}`

- [ ] Stop container
  ```bash
  docker ps  # Get container ID
  docker stop <container-id>
  ```

## 🚀 HuggingFace Spaces Deployment

### Option A: Web Upload (Recommended for First Time)

- [ ] Navigate to https://huggingface.co/new-space

- [ ] Fill in Space details:
  - Space name: `manufacturing-qc-env`
  - License: `MIT`
  - SDK: `Docker` ⚠️ IMPORTANT!
  - Space hardware: `CPU basic` (free tier)

- [ ] Click "Create Space"

- [ ] Upload ALL required files:
  - [ ] `app.py`
  - [ ] `Dockerfile`
  - [ ] `inference.py`
  - [ ] `LICENSE`
  - [ ] `manufacturing_qc_env.py`
  - [ ] `openenv.yaml`
  - [ ] `README.md`
  - [ ] `requirements.txt`
  - [ ] `server.py`

- [ ] Go to Space Settings → Repository secrets

- [ ] Add repository secrets:
  - [ ] Name: `HF_TOKEN`, Value: `your_actual_token`
  - [ ] Name: `API_BASE_URL`, Value: `https://router.huggingface.co/v1`
  - [ ] Name: `MODEL_NAME`, Value: `Qwen/Qwen2.5-72B-Instruct`

- [ ] Wait for build (10-15 minutes)
  - Check "Building" tab for progress
  - Look for "Running" status

### Option B: Git CLI (For Advanced Users)

- [ ] Install HuggingFace CLI
  ```bash
  pip install huggingface-hub
  ```

- [ ] Login to HuggingFace
  ```bash
  huggingface-cli login
  # Paste your HF token when prompted
  ```

- [ ] Run deployment script
  ```bash
  ./deploy_hf.sh
  # Enter your HF username when prompted
  ```

- [ ] Add secrets via web interface (see Option A)

## ✅ Validation

- [ ] Space shows "Running" status
  - Check at: `https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env`

- [ ] Space URL is accessible in browser
  - Should see API interface

- [ ] Health check works
  ```bash
  curl https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env/health
  ```
  Expected: `{"status":"healthy","service":"manufacturing-qc-env"}`

- [ ] Reset endpoint works
  ```bash
  curl -X POST https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env/reset \
    -H "Content-Type: application/json" \
    -d '{"task":"basic_inspection"}'
  ```
  Expected: JSON with observation data

- [ ] Step endpoint works
  ```bash
  curl -X POST https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env/step \
    -H "Content-Type: application/json" \
    -d '{"action":{"action_type":"approve","product_id":"TEST","reason":"test"}}'
  ```
  Expected: JSON with observation, reward, done, info

- [ ] Check Space logs for errors
  - Go to Space → Files → Logs
  - Should see "Manufacturing QC Environment server starting..."
  - No ERROR messages

## 🧪 Final Testing

- [ ] Can run inference locally against deployed Space
  ```bash
  export API_BASE_URL=https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env
  python3 inference.py
  ```

- [ ] All 3 tasks accessible:
  - [ ] basic_inspection
  - [ ] optimized_throughput  
  - [ ] adaptive_control

- [ ] Logs follow required format:
  - [ ] [START] line present
  - [ ] [STEP] lines for each step
  - [ ] [END] line present
  - [ ] Correct field formatting

## 📝 Documentation Check

- [ ] README.md is complete
- [ ] openenv.yaml is valid
- [ ] LICENSE file included
- [ ] No secrets (tokens) in committed files
- [ ] .gitignore includes .env

## 🎯 Submission

- [ ] Copy your Space URL:
  ```
  https://huggingface.co/spaces/YOUR_USERNAME/manufacturing-qc-env
  ```

- [ ] Navigate to hackathon submission form

- [ ] Paste Space URL in submission field

- [ ] Fill in any other required fields:
  - Project name: Manufacturing Quality Control Environment
  - Description: Real-world manufacturing QC environment for AI agents
  - Tags: openenv, manufacturing, quality-control

- [ ] Double-check all information

- [ ] Click Submit! 🎉

## 📊 Post-Submission

- [ ] Confirm submission received
  - Check email for confirmation
  - Check submission dashboard

- [ ] Keep HuggingFace Space running
  - Don't delete until after judging
  - Monitor for crashes

- [ ] Save submission details:
  - Space URL: ______________________________
  - Submission time: _________________________
  - Confirmation number: _____________________

## 🎉 Celebration

- [ ] Pat yourself on the back! You built a complete OpenEnv environment! 🏆
- [ ] Share your Space URL with friends
- [ ] Star your own project on GitHub (if you created a repo)

## ⏱️ Time Tracking

Start time: __________  
End time: __________  
Total time: __________

Target: 30-40 minutes

---

## 🆘 If Something Goes Wrong

### Space won't build
1. Check Dockerfile syntax
2. Verify all required files uploaded
3. Check Space logs for specific error
4. Compare with working Dockerfile in project

### Secrets not working  
1. Re-add secrets in Space settings
2. Ensure no typos in secret names
3. Restart Space after adding secrets

### API returns errors
1. Check server.py syntax
2. Verify all imports work
3. Test locally first with uvicorn
4. Check Python version compatibility

### Can't login to HuggingFace
1. Verify token is "Write" permission
2. Try logging out and in again
3. Check token hasn't expired
4. Generate new token if needed

---

## 📞 Resources

- **HuggingFace Docs:** https://huggingface.co/docs/hub/spaces
- **Project README:** README.md
- **Quick Start:** QUICKSTART.md
- **Submission Guide:** SUBMISSION_GUIDE.md
- **Project Summary:** PROJECT_SUMMARY.md

---

**You've got this! Follow the checklist step by step. 🚀**

**Estimated time to completion: 30-40 minutes**

---

✅ = Done  
⏸️ = In Progress  
⬜ = Not Started  
