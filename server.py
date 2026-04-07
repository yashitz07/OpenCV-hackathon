"""
FastAPI Server for Manufacturing QC Environment
Serves the OpenEnv API endpoints for Hugging Face Spaces deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Dict, Optional
import os

from manufacturing_qc_env import (
    ManufacturingQCEnv,
    ManufacturingQCAction,
    ManufacturingQCObservation,
    ManufacturingQCReward,
    ManufacturingQCState,
    ActionType,
)

# Initialize FastAPI app
app = FastAPI(
    title="Manufacturing QC Environment",
    description="Real-world quality control environment for AI agents",
    version="1.0.0",
)

# Global environment instance
env_instance: Optional[ManufacturingQCEnv] = None


# ============================================================================
# Request/Response Models
# ============================================================================

class ResetRequest(BaseModel):
    """Request body for reset endpoint"""
    task: Optional[str] = "basic_inspection"
    config: Optional[Dict[str, Any]] = None


class StepRequest(BaseModel):
    """Request body for step endpoint"""
    action: Dict[str, Any]


class ResetResponse(BaseModel):
    """Response from reset endpoint"""
    observation: Dict[str, Any]


class StepResponse(BaseModel):
    """Response from step endpoint"""
    observation: Dict[str, Any]
    reward: Dict[str, Any]
    done: bool
    info: Dict[str, Any]


class StateResponse(BaseModel):
    """Response from state endpoint"""
    state: Dict[str, Any]


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Manufacturing QC Environment",
        "version": "1.0.0",
        "framework": "OpenEnv",
        "tasks": ["basic_inspection", "optimized_throughput", "adaptive_control"],
        "endpoints": {
            "reset": "/reset",
            "step": "/step",
            "state": "/state",
            "health": "/health",
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "manufacturing-qc-env"}


@app.post("/reset")
async def reset(request: ResetRequest = None):
    """
    Reset the environment to initial state
    
    Args:
        request: Optional reset configuration with task name
    
    Returns:
        Initial observation
    """
    global env_instance
    
    try:
        # Get task name from request or environment variable
        task_name = "basic_inspection"
        if request and request.task:
            task_name = request.task
        elif os.getenv("MANUFACTURING_QC_TASK"):
            task_name = os.getenv("MANUFACTURING_QC_TASK")
        
        # Create new environment instance
        env_instance = ManufacturingQCEnv(task_name=task_name)
        
        # Reset environment
        observation = await env_instance.reset()
        
        return JSONResponse(
            content={"observation": observation.model_dump()},
            status_code=200
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")


@app.post("/step")
async def step(request: StepRequest):
    """
    Execute one step in the environment
    
    Args:
        request: Action to take
    
    Returns:
        Observation, reward, done flag, and info
    """
    global env_instance
    
    if env_instance is None:
        raise HTTPException(
            status_code=400,
            detail="Environment not initialized. Call /reset first."
        )
    
    try:
        # Parse action
        action_data = request.action
        
        # Create action object
        action = ManufacturingQCAction(
            action_type=ActionType(action_data.get("action_type", "approve")),
            product_id=action_data.get("product_id"),
            reason=action_data.get("reason", ""),
            threshold_value=action_data.get("threshold_value"),
            notes=action_data.get("notes"),
        )
        
        # Execute step
        observation, reward, done, info = await env_instance.step(action)
        
        return JSONResponse(
            content={
                "observation": observation.model_dump(),
                "reward": reward.model_dump(),
                "done": done,
                "info": info,
            },
            status_code=200
        )
    
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Step failed: {str(e)}")


@app.get("/state")
async def state():
    """
    Get current environment state
    
    Returns:
        Current state of the environment
    """
    global env_instance
    
    if env_instance is None:
        raise HTTPException(
            status_code=400,
            detail="Environment not initialized. Call /reset first."
        )
    
    try:
        current_state = await env_instance.state()
        
        return JSONResponse(
            content={"state": current_state.model_dump()},
            status_code=200
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"State query failed: {str(e)}")


@app.post("/close")
async def close():
    """Close and cleanup the environment"""
    global env_instance
    
    if env_instance is None:
        return JSONResponse(
            content={"message": "No environment to close"},
            status_code=200
        )
    
    try:
        await env_instance.close()
        env_instance = None
        
        return JSONResponse(
            content={"message": "Environment closed successfully"},
            status_code=200
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Close failed: {str(e)}")


@app.get("/tasks")
async def list_tasks():
    """List available tasks"""
    return JSONResponse(
        content={
            "tasks": [
                {
                    "name": "basic_inspection",
                    "difficulty": "easy",
                    "description": "Inspect products and correctly identify obvious defects",
                    "max_steps": 15,
                },
                {
                    "name": "optimized_throughput",
                    "difficulty": "medium",
                    "description": "Balance quality control with production throughput efficiently",
                    "max_steps": 25,
                },
                {
                    "name": "adaptive_control",
                    "difficulty": "hard",
                    "description": "Dynamically adjust thresholds and request maintenance when needed",
                    "max_steps": 30,
                },
            ]
        },
        status_code=200
    )


# ============================================================================
# Application Startup
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize environment on startup"""
    print("Manufacturing QC Environment server starting...")
    print("Available tasks: basic_inspection, optimized_throughput, adaptive_control")
    print("Server ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global env_instance
    
    if env_instance is not None:
        await env_instance.close()
        env_instance = None
    
    print("Manufacturing QC Environment server shutting down...")


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found", "detail": str(exc)}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
