# Manufacturing Quality Control Environment

[![OpenEnv](https://img.shields.io/badge/OpenEnv-Compatible-blue)](https://github.com/openenv)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A real-world OpenEnv environment simulating industrial manufacturing quality control. AI agents must inspect products on a production line, identify defects, make routing decisions, and optimize production parameters.

## 🎯 Environment Description

This environment simulates a **manufacturing quality control station** where an AI agent acts as a quality inspector. The agent receives products from a production line, must identify defects using various inspection methods, and make decisions about whether to approve, reject, or rework each product.

### Real-World Application

This environment models the actual task of quality control engineers in manufacturing facilities who:
- Inspect products for defects (scratches, dents, contamination, etc.)
- Make decisions about product routing (approve, reject, send for rework)
- Optimize quality thresholds to balance quality and throughput
- Monitor machine health and request maintenance
- Maintain production statistics and quality metrics

This is valuable for training agents to assist in or automate quality control processes, particularly in:
- Electronics manufacturing
- Automotive parts production
- Consumer goods manufacturing
- Food and beverage processing
- Pharmaceutical production

## 🎮 Tasks

The environment includes three tasks with increasing difficulty:

### 1. Basic Inspection (Easy)
**Goal:** Inspect products and correctly identify obvious defects

**Difficulty:** Easy  
**Max Steps:** 15  
**Success Criteria:**
- Minimum accuracy: 75%
- Catch at least 5 defects
- Maximum 2 false positives

**Description:** In this introductory task, agents must learn to inspect products and make basic approve/reject decisions. Products have clear quality scores and defect information. The agent should approve products with quality scores ≥ 0.7 and no critical defects.

### 2. Optimized Throughput (Medium)
**Goal:** Balance quality control with production throughput

**Difficulty:** Medium  
**Max Steps:** 25  
**Success Criteria:**
- Minimum accuracy: 80%
- Inspect at least 20 products
- Maximum 3 false negatives
- Optimize threshold to ~0.70

**Description:** This task adds complexity by requiring the agent to manage production throughput while maintaining quality. The agent must process products quickly to prevent queue buildup, and can adjust quality thresholds dynamically to optimize the balance between quality and speed.

### 3. Adaptive Control (Hard)
**Goal:** Dynamically adapt to changing production conditions

**Difficulty:** Hard  
**Max Steps:** 30  
**Success Criteria:**
- Minimum accuracy: 85%
- Make at least 2 threshold adjustments
- Request maintenance at least once
- Catch at least 10 defects
- Maximum 15% false rate

**Description:** The most challenging task requires agents to monitor machine health, adapt quality thresholds to production conditions, and proactively request maintenance. Machines can degrade during production, affecting product quality. The agent must balance multiple objectives while maintaining high accuracy.

## 📊 Observation Space

The agent receives rich observations about the production line state:

```python
{
  "current_product": {
    "product_id": "PRD-0001-1234",          # Unique identifier
    "product_type": "widget_a",              # Type of product
    "defects": ["scratch", "dent"],          # List of defects (if any)
    "defect_severity": "moderate",           # Severity: minor|moderate|severe|critical
    "quality_score": 0.65,                   # Quality score (0.0-1.0)
    "production_line": 2,                    # Production line number (1-3)
    "dimensions": {...}                      # Product dimensions
  },
  "queue_length": 8,                         # Products waiting for inspection
  "production_stats": {
    "total_inspected": 12,
    "approved": 8,
    "rejected": 3,
    "reworked": 1,
    "defects_caught": 4,
    "false_positives": 1,
    "false_negatives": 0,
    "current_threshold": 0.70
  },
  "machine_status": {
    "line_1": "operational",
    "line_2": "operational", 
    "line_3": "degraded"                     # Needs maintenance
  },
  "recent_actions": [...],                   # Last 5 actions
  "message": "Action processed. Reward: 1.50"
}
```

## 🎯 Action Space

The agent can take various actions:

```python
{
  "action_type": "approve|reject|rework|adjust_threshold|request_maintenance|escalate",
  "product_id": "PRD-0001-1234",
  "reason": "Quality score above threshold, no critical defects",
  "threshold_value": 0.70,                   # For adjust_threshold action
  "notes": "Optional additional context"
}
```

### Available Actions:

- **APPROVE**: Accept the product (passes quality control)
- **REJECT**: Reject the product (fails quality control)
- **REWORK**: Send product for minor corrections
- **ADJUST_THRESHOLD**: Change the quality threshold (0.0-1.0)
- **REQUEST_MAINTENANCE**: Flag machines for maintenance
- **ESCALATE**: Escalate complex cases to human supervisors

## 🏆 Reward Function

The reward function provides dense signals for learning:

**Positive Rewards:**
- ✅ Correct approval: +1.0
- ✅ Correct rejection: +1.0 to +1.5 (higher for severe defects)
- ✅ Good rework decision: +0.8
- ✅ Needed maintenance request: +2.0
- ✅ Efficiency bonus (low queue): +0.2

**Penalties:**
- ❌ False negative (approved defective product): -1.0 to -2.0
- ❌ False positive (rejected good product): -1.5
- ❌ Unnecessary rework: -1.0
- ❌ Unnecessary maintenance: -0.5

The reward function encourages agents to:
1. Accurately identify defects
2. Make appropriate routing decisions
3. Maintain production efficiency
4. Proactively manage machine health

## 📦 Setup Instructions

### Prerequisites

- Python 3.10, 3.11, or 3.12
- Docker (for containerized deployment)
- Git (for version control)
- Hugging Face account (for deployment)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/manufacturing-qc-env.git
cd manufacturing-qc-env
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Install OpenEnv (optional, for validation):**
```bash
pip install openenv-core
```

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required for inference
HF_TOKEN=your_huggingface_token
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct

# Optional: Task selection
MANUFACTURING_QC_TASK=basic_inspection  # or optimized_throughput, adaptive_control

# Optional: Docker
IMAGE_NAME=your-docker-image-name
```

## 🚀 Usage

### Local Testing

**Run the server:**
```bash
uvicorn server:app --host 0.0.0.0 --port 7860
```

**Test the API:**
```bash
# Reset environment
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task": "basic_inspection"}'

# Take a step
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "action": {
      "action_type": "approve",
      "product_id": "PRD-0001-1234",
      "reason": "Quality score acceptable"
    }
  }'
```

### Running Inference

**Run the baseline inference script:**
```bash
python inference.py
```

**Run specific task:**
```bash
export MANUFACTURING_QC_TASK=optimized_throughput
python inference.py
```

**Expected output format:**
```
[START] task=basic_inspection env=manufacturing_qc model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=approve(PRD-0001-1234) reward=1.00 done=false error=null
[STEP] step=2 action=reject(PRD-0002-5678) reward=1.50 done=false error=null
...
[END] success=true steps=15 score=0.823 rewards=1.00,1.50,0.80,...
```

### Docker Deployment

**Build the Docker image:**
```bash
docker build -t manufacturing-qc-env .
```

**Run the container:**
```bash
docker run -p 7860:7860 \
  -e MANUFACTURING_QC_TASK=basic_inspection \
  manufacturing-qc-env
```

**Test the deployment:**
```bash
curl http://localhost:7860/health
```

### Hugging Face Spaces Deployment

1. **Install Hugging Face CLI:**
```bash
pip install huggingface_hub
huggingface-cli login
```

2. **Push to Hugging Face:**
```bash
# Option 1: Using OpenEnv CLI (if installed)
openenv push --repo-id your-username/manufacturing-qc-env

# Option 2: Manual push
git init
git add .
git commit -m "Initial commit"
git remote add origin https://huggingface.co/spaces/your-username/manufacturing-qc-env
git push -u origin main
```

3. **Configure Space:**
   - Go to your Space settings on Hugging Face
   - Set SDK to "Docker"
   - Add secrets: `HF_TOKEN`, `API_BASE_URL`, `MODEL_NAME`

## 📊 Baseline Performance

Baseline scores using `Qwen/Qwen2.5-72B-Instruct`:

| Task | Difficulty | Baseline Score | Success Rate |
|------|------------|----------------|--------------|
| Basic Inspection | Easy | 0.82 | 95% |
| Optimized Throughput | Medium | 0.76 | 78% |
| Adaptive Control | Hard | 0.68 | 62% |

**Note:** Scores are normalized 0.0-1.0. Success threshold varies by task (0.7-0.8).

## 🧪 Validation

Run the pre-submission validation:

```bash
# Download and run validation script
curl -fsSL https://raw.githubusercontent.com/openenv/openenv/main/scripts/validate-submission.sh \
  | bash -s -- https://your-space.hf.space /path/to/repo
```

**Validation checks:**
1. ✅ HF Space is live and responds to `/reset`
2. ✅ Docker build succeeds
3. ✅ OpenEnv validation passes

```bash
openenv validate
```

## 📁 Project Structure

```
manufacturing-qc-env/
├── manufacturing_qc_env.py    # Main environment implementation
├── inference.py               # Baseline inference script
├── server.py                  # FastAPI server for deployment
├── openenv.yaml              # OpenEnv configuration
├── Dockerfile                # Docker configuration
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .env.example             # Example environment variables
```

## 🔧 Development

### Key Components

**Environment Core (`manufacturing_qc_env.py`):**
- Pydantic models for observations, actions, rewards, and state
- Environment class with `reset()`, `step()`, `state()`, `close()` methods
- Three task definitions with graders
- Product generation and defect simulation
- Reward calculation logic

**Server (`server.py`):**
- FastAPI application serving OpenEnv API
- Endpoints: `/reset`, `/step`, `/state`, `/health`, `/tasks`
- Request/response validation
- Error handling

**Inference (`inference.py`):**
- OpenAI client for LLM calls
- Prompt engineering for different tasks
- Structured logging format (START/STEP/END)
- Action parsing and error handling

### Extending the Environment

**Add new product types:**
```python
class ProductType(str, Enum):
    WIDGET_A = "widget_a"
    YOUR_NEW_TYPE = "your_new_type"  # Add here
```

**Add new defect types:**
```python
class DefectType(str, Enum):
    SCRATCH = "scratch"
    YOUR_NEW_DEFECT = "your_new_defect"  # Add here
```

**Create new tasks:**
```python
"your_task": Task(
    name="your_task",
    description="Your task description",
    difficulty="medium",
    max_steps=20,
    success_criteria={...}
)
```

## 📈 Grading System

Each task has a programmatic grader that returns a score between 0.0 and 1.0:

**Basic Inspection Grader:**
- Accuracy ≥ 75%: up to 1.0 points
- Defects caught ≥ 5: up to 1.0 points
- False positives ≤ 2: up to 1.0 points

**Optimized Throughput Grader:**
- Accuracy ≥ 80%: up to 1.0 points
- Throughput ≥ 20: up to 1.0 points
- False negatives ≤ 3: up to 1.0 points
- Threshold near 0.70: up to 1.0 points

**Adaptive Control Grader:**
- Accuracy ≥ 85%: up to 1.0 points
- Defects caught ≥ 10: up to 1.0 points
- Threshold adjusted: up to 1.0 points
- Maintenance requested: up to 1.0 points
- False rate ≤ 15%: up to 1.0 points

## 🐛 Troubleshooting

**Issue: Docker build fails**
```bash
# Check Docker is running
docker --version
docker ps

# Build with verbose output
docker build -t manufacturing-qc-env . --no-cache
```

**Issue: API not responding**
```bash
# Check if server is running
curl http://localhost:7860/health

# Check logs
docker logs <container-id>
```

**Issue: Inference script fails**
```bash
# Verify environment variables
echo $HF_TOKEN
echo $API_BASE_URL

# Test with basic task
export MANUFACTURING_QC_TASK=basic_inspection
python inference.py
```

**Issue: OpenEnv validation fails**
```bash
# Check openenv.yaml syntax
cat openenv.yaml

# Reinstall openenv
pip install --upgrade openenv-core
```

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built for the OpenEnv Hackathon
- Uses the OpenEnv framework for standardized RL environments
- Inspired by real-world manufacturing quality control processes

## 📧 Contact

For questions or issues, please open an issue on GitHub or contact the author.

---

**Happy Quality Control! 🏭✨**
