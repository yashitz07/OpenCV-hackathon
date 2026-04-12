"""
Manufacturing QC Inference Script
===================================

Runs an AI agent against the Manufacturing Quality Control environment.
Follows the mandatory stdout format for OpenEnv evaluation.
"""

import asyncio
import os
import sys
import textwrap
from typing import List, Optional

from openai import OpenAI

from manufacturing_qc_env import (
    ManufacturingQCAction,
    ManufacturingQCEnv,
    ActionType,
    GRADERS,
)

# ============================================================================
# Environment Variables (MANDATORY)
# ============================================================================

IMAGE_NAME = os.getenv("IMAGE_NAME")  # For Docker deployment
API_KEY = os.getenv("API_KEY") or os.getenv("HF_TOKEN")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
TASK_NAME = os.getenv("MANUFACTURING_QC_TASK", "basic_inspection")
BENCHMARK = "manufacturing_qc"

# Task configuration
TASK_CONFIGS = {
    "basic_inspection": {
        "max_steps": 15,
        "temperature": 0.7,
        "max_tokens": 200,
        "success_threshold": 0.7,
    },
    "optimized_throughput": {
        "max_steps": 25,
        "temperature": 0.6,
        "max_tokens": 250,
        "success_threshold": 0.75,
    },
    "adaptive_control": {
        "max_steps": 30,
        "temperature": 0.5,
        "max_tokens": 300,
        "success_threshold": 0.80,
    },
}

config = TASK_CONFIGS.get(TASK_NAME, TASK_CONFIGS["basic_inspection"])
MAX_STEPS = config["max_steps"]
TEMPERATURE = config["temperature"]
MAX_TOKENS = config["max_tokens"]
SUCCESS_SCORE_THRESHOLD = config["success_threshold"]

# ============================================================================
# System Prompts
# ============================================================================

SYSTEM_PROMPTS = {
    "basic_inspection": textwrap.dedent(
        """
        You are an AI quality control inspector in a manufacturing facility.
        
        Your task is to inspect products on the production line and make decisions:
        - INSPECT: Examine a product carefully
        - APPROVE: Accept a product that meets quality standards
        - REJECT: Reject a product with defects
        - REWORK: Send a product for minor corrections
        
        Each product has:
        - product_id: unique identifier
        - product_type: type of product
        - defects: list of defects (if any)
        - quality_score: 0.0-1.0 (higher is better)
        - defect_severity: minor, moderate, severe, or critical
        
        DECISION RULES:
        - Approve products with quality_score >= 0.7 and no critical defects
        - Reject products with severe or critical defects
        - Send products with minor defects for rework
        - Always provide a clear reason for your decision
        
        Respond with a JSON object:
        {
          "action_type": "approve|reject|rework",
          "product_id": "PRD-XXXX-XXXX",
          "reason": "explanation of decision"
        }
        """
    ).strip(),
    
    "optimized_throughput": textwrap.dedent(
        """
        You are an AI quality control supervisor optimizing production throughput.
        
        Your goal is to balance quality control with production efficiency:
        - Maintain high accuracy (>80%)
        - Process products quickly to prevent queue buildup
        - Adjust quality thresholds when appropriate
        - Minimize false negatives (defective products passing through)
        
        Available actions:
        - APPROVE: Accept product (fast)
        - REJECT: Reject product (removes from line)
        - REWORK: Send for correction (slower)
        - ADJUST_THRESHOLD: Change quality threshold (0.6-0.8 recommended)
        
        Monitor:
        - queue_length: products waiting (keep < 10)
        - production_stats: your performance metrics
        - current_threshold: quality cutoff point
        
        Respond with a JSON object:
        {
          "action_type": "approve|reject|rework|adjust_threshold",
          "product_id": "PRD-XXXX-XXXX",
          "reason": "explanation",
          "threshold_value": 0.70  // only for adjust_threshold
        }
        """
    ).strip(),
    
    "adaptive_control": textwrap.dedent(
        """
        You are an advanced AI quality control system with adaptive capabilities.
        
        Your responsibilities:
        - Maintain very high accuracy (>85%)
        - Dynamically adjust quality thresholds based on production conditions
        - Monitor machine health and request maintenance when needed
        - Optimize complex multi-factor decisions
        
        Available actions:
        - APPROVE, REJECT, REWORK: standard QC actions
        - ADJUST_THRESHOLD: adapt quality standards (provide threshold_value 0.0-1.0)
        - REQUEST_MAINTENANCE: flag machine issues
        - ESCALATE: escalate complex cases
        
        Monitor machine_status:
        - operational: normal
        - degraded: reduced performance (consider maintenance)
        
        Advanced strategy:
        - Lower threshold when machines degrade
        - Request maintenance proactively
        - Make 2-3 threshold adjustments during episode
        - Balance precision and recall
        
        Respond with a JSON object:
        {
          "action_type": "approve|reject|rework|adjust_threshold|request_maintenance|escalate",
          "product_id": "PRD-XXXX-XXXX",
          "reason": "detailed explanation",
          "threshold_value": 0.75,  // for adjust_threshold
          "notes": "additional context"  // optional
        }
        """
    ).strip(),
}

# ============================================================================
# Logging Functions (MANDATORY FORMAT)
# ============================================================================

def log_start(task: str, env: str, model: str) -> None:
    """Log episode start"""
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(
    step: int, action: str, reward: float, done: bool, error: Optional[str]
) -> None:
    """Log each step"""
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    """Log episode end"""
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


# ============================================================================
# Helper Functions
# ============================================================================

def build_user_prompt(observation, step: int) -> str:
    """Build user prompt from observation"""
    product = observation.current_product
    stats = observation.production_stats
    
    if not product:
        return "No product available. Episode ending."
    
    product_info = f"""
CURRENT PRODUCT:
- ID: {product.product_id}
- Type: {product.product_type.value}
- Quality Score: {product.quality_score:.2f}
- Defects: {', '.join([d.value for d in product.defects]) if product.defects else 'None'}
- Severity: {product.defect_severity.value}
- Production Line: {product.production_line}

QUEUE STATUS:
- Products waiting: {observation.queue_length}

PRODUCTION STATS:
- Total inspected: {stats.total_inspected}
- Approved: {stats.approved}
- Rejected: {stats.rejected}
- Reworked: {stats.reworked}
- Defects caught: {stats.defects_caught}
- False positives: {stats.false_positives}
- False negatives: {stats.false_negatives}
- Current threshold: {stats.current_threshold:.2f}

MACHINE STATUS:
"""
    
    for machine, status in observation.machine_status.items():
        product_info += f"- {machine}: {status}\n"
    
    product_info += f"\nRECENT ACTIONS:\n"
    for action in observation.recent_actions[-3:]:
        product_info += f"- {action}\n"
    
    product_info += f"\n{observation.message}\n"
    product_info += f"\nStep {step}/{MAX_STEPS}. What action do you take?"
    
    return product_info.strip()


def parse_model_response(response: str, product_id: str) -> ManufacturingQCAction:
    """Parse model response into action"""
    import json
    
    try:
        # Try to parse as JSON
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        data = json.loads(response)
        
        action_type_str = data.get("action_type", "approve").lower()
        action_type = ActionType.APPROVE  # default
        
        if "reject" in action_type_str:
            action_type = ActionType.REJECT
        elif "rework" in action_type_str:
            action_type = ActionType.REWORK
        elif "adjust" in action_type_str or "threshold" in action_type_str:
            action_type = ActionType.ADJUST_THRESHOLD
        elif "maintenance" in action_type_str:
            action_type = ActionType.REQUEST_MAINTENANCE
        elif "escalate" in action_type_str:
            action_type = ActionType.ESCALATE
        elif "approve" in action_type_str or "accept" in action_type_str:
            action_type = ActionType.APPROVE
        
        return ManufacturingQCAction(
            action_type=action_type,
            product_id=data.get("product_id", product_id),
            reason=data.get("reason", "Decision made by AI"),
            threshold_value=data.get("threshold_value"),
            notes=data.get("notes"),
        )
    except Exception as e:
        # Fallback: parse from text
        response_lower = response.lower()
        
        if "reject" in response_lower:
            action_type = ActionType.REJECT
        elif "rework" in response_lower:
            action_type = ActionType.REWORK
        elif "maintenance" in response_lower:
            action_type = ActionType.REQUEST_MAINTENANCE
        elif "adjust" in response_lower or "threshold" in response_lower:
            action_type = ActionType.ADJUST_THRESHOLD
        else:
            action_type = ActionType.APPROVE
        
        return ManufacturingQCAction(
            action_type=action_type,
            product_id=product_id,
            reason=response[:100],
        )


def get_model_action(
    client: OpenAI, observation, step: int
) -> ManufacturingQCAction:
    """Get action from model via the evaluator-provided LLM proxy.
    Always makes a real API call — never skips."""
    product_id = observation.current_product.product_id if observation.current_product else "NONE"
    user_prompt = build_user_prompt(observation, step)
    system_prompt = SYSTEM_PROMPTS.get(TASK_NAME, SYSTEM_PROMPTS["basic_inspection"])
    
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        
        response = (completion.choices[0].message.content or "").strip()
        print(f"[DEBUG] Model response: {response[:100]}", file=sys.stderr, flush=True)
        
        return parse_model_response(response, product_id)
    
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", file=sys.stderr, flush=True)
        # Fallback to safe default
        return ManufacturingQCAction(
            action_type=ActionType.APPROVE,
            product_id=product_id,
            reason="Fallback action due to model error",
        )


# ============================================================================
# Main Inference Loop
# ============================================================================

async def main() -> None:
    """Main inference function"""
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False
    env = None
    client = None
    
    # Log start IMMEDIATELY - must be the first structured output
    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)
    
    try:
        # Initialize OpenAI client using evaluator-provided credentials
        print(f"[DEBUG] API_KEY present: {bool(API_KEY)}, API_BASE_URL: {API_BASE_URL}, MODEL: {MODEL_NAME}", file=sys.stderr, flush=True)
        
        client = OpenAI(
            base_url=API_BASE_URL,
            api_key=API_KEY,
        )
        print(f"[DEBUG] OpenAI client created with base_url={API_BASE_URL}", file=sys.stderr, flush=True)
        
        # Create environment with error handling
        try:
            if IMAGE_NAME:
                print(f"[DEBUG] Creating environment from Docker image: {IMAGE_NAME}", file=sys.stderr, flush=True)
                env = await ManufacturingQCEnv.from_docker_image(IMAGE_NAME, task_name=TASK_NAME)
            else:
                print(f"[DEBUG] Creating local environment for task: {TASK_NAME}", file=sys.stderr, flush=True)
                env = ManufacturingQCEnv(task_name=TASK_NAME)
        except Exception as e:
            print(f"[DEBUG] Environment creation failed: {e}", file=sys.stderr, flush=True)
            print(f"[DEBUG] Falling back to local environment", file=sys.stderr, flush=True)
            env = ManufacturingQCEnv(task_name=TASK_NAME)
        
    except Exception as e:
        print(f"[DEBUG] Initialization error: {e}", file=sys.stderr, flush=True)
        log_end(success=False, steps=0, score=0.0, rewards=[])
        return
    
    try:
        # Reset environment
        observation = await env.reset()
        
        # Run episode
        for step in range(1, MAX_STEPS + 1):
            if not observation.current_product:
                break
            
            # Get action from model
            action = get_model_action(client, observation, step)
            
            # Take step
            observation, reward_obj, done, info = await env.step(action)
            
            reward = reward_obj.reward
            rewards.append(reward)
            steps_taken = step
            
            # Log step
            action_str = f"{action.action_type.value}({action.product_id})"
            log_step(step=step, action=action_str, reward=reward, done=done, error=None)
            
            if done:
                break
        
        # Calculate final score using grader
        grader = GRADERS.get(TASK_NAME)
        if grader:
            score = grader(env)
        else:
            # Fallback: normalize total reward
            score = max(0.0, min(1.0, (env.total_reward + 10) / 30))
        
        success = score >= SUCCESS_SCORE_THRESHOLD
        
    except Exception as e:
        print(f"[DEBUG] Episode error: {e}", file=sys.stderr, flush=True)
        success = False
    
    finally:
        if env is not None:
            try:
                await env.close()
            except Exception as e:
                print(f"[DEBUG] env.close() error: {e}", file=sys.stderr, flush=True)
        
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[DEBUG] Interrupted by user", file=sys.stderr, flush=True)
        exit(1)
    except Exception as e:
        print(f"[DEBUG] Fatal error: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc(file=sys.stderr)
        # Ensure we always have START+END pair on stdout for the evaluator
        print(f"[START] task={TASK_NAME} env={BENCHMARK} model={MODEL_NAME}", flush=True)
        print(f"[END] success=false steps=0 score=0.000 rewards=", flush=True)
        exit(1)
