"""
Manufacturing Quality Control Environment
==========================================

A real-world OpenEnv environment simulating industrial quality control.
AI agents inspect products, identify defects, route items, and optimize production decisions.
"""

import asyncio
import json
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field


# ============================================================================
# Enums and Constants
# ============================================================================

class DefectType(str, Enum):
    """Types of defects that can occur in manufacturing"""
    NONE = "none"
    SCRATCH = "scratch"
    DENT = "dent"
    DISCOLORATION = "discoloration"
    CRACK = "crack"
    MISALIGNMENT = "misalignment"
    CONTAMINATION = "contamination"


class ProductType(str, Enum):
    """Types of products on the production line"""
    WIDGET_A = "widget_a"
    WIDGET_B = "widget_b"
    COMPONENT_X = "component_x"
    COMPONENT_Y = "component_y"


class ActionType(str, Enum):
    """Available actions for the agent"""
    INSPECT = "inspect"
    APPROVE = "approve"
    REJECT = "reject"
    REWORK = "rework"
    ESCALATE = "escalate"
    ADJUST_THRESHOLD = "adjust_threshold"
    REQUEST_MAINTENANCE = "request_maintenance"


class DefectSeverity(str, Enum):
    """Severity levels for defects"""
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"


# ============================================================================
# Pydantic Models - OpenEnv Spec
# ============================================================================

class Product(BaseModel):
    """Represents a product on the production line"""
    product_id: str = Field(..., description="Unique product identifier")
    product_type: ProductType = Field(..., description="Type of product")
    defects: List[DefectType] = Field(default_factory=list, description="List of defects present")
    defect_severity: DefectSeverity = Field(default=DefectSeverity.MINOR, description="Overall defect severity")
    production_line: int = Field(..., description="Production line number (1-3)")
    timestamp: int = Field(..., description="Production timestamp")
    dimensions: Dict[str, float] = Field(default_factory=dict, description="Product dimensions")
    quality_score: float = Field(..., ge=0.0, le=1.0, description="Quality score (0-1)")


class ProductionStats(BaseModel):
    """Production line statistics"""
    total_inspected: int = Field(default=0, description="Total products inspected")
    approved: int = Field(default=0, description="Products approved")
    rejected: int = Field(default=0, description="Products rejected")
    reworked: int = Field(default=0, description="Products sent for rework")
    false_positives: int = Field(default=0, description="Good products incorrectly rejected")
    false_negatives: int = Field(default=0, description="Defective products incorrectly approved")
    defects_caught: int = Field(default=0, description="Defects correctly identified")
    maintenance_requested: int = Field(default=0, description="Maintenance requests made")
    current_threshold: float = Field(default=0.7, description="Current quality threshold")


class ManufacturingQCObservation(BaseModel):
    """Observation returned by the environment"""
    current_product: Optional[Product] = Field(None, description="Current product being inspected")
    queue_length: int = Field(..., description="Number of products waiting for inspection")
    production_stats: ProductionStats = Field(..., description="Current production statistics")
    recent_actions: List[str] = Field(default_factory=list, description="History of recent actions")
    machine_status: Dict[str, str] = Field(default_factory=dict, description="Status of production machines")
    message: str = Field(..., description="Feedback or status message")


class ManufacturingQCAction(BaseModel):
    """Action taken by the agent"""
    action_type: ActionType = Field(..., description="Type of action to take")
    product_id: Optional[str] = Field(None, description="Product ID (if applicable)")
    reason: str = Field(..., description="Reason for the action")
    threshold_value: Optional[float] = Field(None, ge=0.0, le=1.0, description="New threshold (if adjusting)")
    notes: Optional[str] = Field(None, description="Additional notes")


class ManufacturingQCReward(BaseModel):
    """Reward returned by the environment"""
    reward: float = Field(..., description="Reward value")
    components: Dict[str, float] = Field(default_factory=dict, description="Breakdown of reward components")


class ManufacturingQCState(BaseModel):
    """Full environment state"""
    current_step: int = Field(..., description="Current step number")
    task_name: str = Field(..., description="Current task name")
    observation: ManufacturingQCObservation = Field(..., description="Current observation")
    done: bool = Field(..., description="Whether episode is complete")
    total_reward: float = Field(..., description="Cumulative reward")


# ============================================================================
# Task Definitions
# ============================================================================

@dataclass
class Task:
    """Defines a task for the agent"""
    name: str
    description: str
    difficulty: str
    max_steps: int
    success_criteria: Dict[str, Any]
    grader: Any = None


# ============================================================================
# Main Environment Class
# ============================================================================

class ManufacturingQCEnv:
    """
    Manufacturing Quality Control Environment
    
    Simulates a real-world manufacturing quality control scenario where
    an AI agent must inspect products, identify defects, and make routing decisions.
    """
    
    def __init__(self, task_name: str = "basic_inspection"):
        self.task_name = task_name
        self.tasks = self._define_tasks()
        self.current_task = self.tasks.get(task_name, self.tasks["basic_inspection"])
        
        # Environment state
        self.current_step = 0
        self.products_queue: List[Product] = []
        self.stats = ProductionStats()
        self.recent_actions: List[str] = []
        self.current_product: Optional[Product] = None
        self.done = False
        self.total_reward = 0.0
        
        # Machine status for advanced scenarios
        self.machine_status = {
            "line_1": "operational",
            "line_2": "operational",
            "line_3": "operational"
        }
        
    def _define_tasks(self) -> Dict[str, Task]:
        """Define the three tasks with increasing difficulty"""
        return {
            "basic_inspection": Task(
                name="basic_inspection",
                description="Inspect products and correctly identify obvious defects",
                difficulty="easy",
                max_steps=15,
                success_criteria={
                    "min_accuracy": 0.75,
                    "min_defects_caught": 5,
                    "max_false_positives": 2
                }
            ),
            "optimized_throughput": Task(
                name="optimized_throughput",
                description="Balance quality control with production throughput efficiently",
                difficulty="medium",
                max_steps=25,
                success_criteria={
                    "min_accuracy": 0.80,
                    "min_throughput": 20,
                    "max_false_negatives": 3,
                    "target_threshold": 0.70
                }
            ),
            "adaptive_control": Task(
                name="adaptive_control",
                description="Dynamically adjust thresholds and request maintenance when needed",
                difficulty="hard",
                max_steps=30,
                success_criteria={
                    "min_accuracy": 0.85,
                    "threshold_adjustments": 2,
                    "maintenance_requests": 1,
                    "min_defects_caught": 10,
                    "max_false_rate": 0.15
                }
            )
        }
    
    def _generate_product(self) -> Product:
        """Generate a random product with potential defects"""
        product_type = random.choice(list(ProductType))
        product_id = f"PRD-{self.current_step:04d}-{random.randint(1000, 9999)}"
        
        # 40% chance of having defects
        has_defect = random.random() < 0.4
        defects = []
        severity = DefectSeverity.MINOR
        quality_score = 1.0
        
        if has_defect:
            num_defects = random.choices([1, 2, 3], weights=[0.7, 0.25, 0.05])[0]
            defects = random.sample([d for d in DefectType if d != DefectType.NONE], num_defects)
            
            # Determine severity based on defect types
            critical_defects = {DefectType.CRACK, DefectType.CONTAMINATION}
            if any(d in critical_defects for d in defects):
                severity = DefectSeverity.CRITICAL
                quality_score = random.uniform(0.1, 0.4)
            elif len(defects) >= 2:
                severity = DefectSeverity.MODERATE
                quality_score = random.uniform(0.4, 0.6)
            else:
                severity = DefectSeverity.MINOR
                quality_score = random.uniform(0.6, 0.75)
        else:
            quality_score = random.uniform(0.8, 1.0)
        
        return Product(
            product_id=product_id,
            product_type=product_type,
            defects=defects,
            defect_severity=severity,
            production_line=random.randint(1, 3),
            timestamp=self.current_step,
            dimensions={
                "length": round(random.uniform(10.0, 50.0), 2),
                "width": round(random.uniform(10.0, 50.0), 2),
                "height": round(random.uniform(5.0, 30.0), 2)
            },
            quality_score=round(quality_score, 2)
        )
    
    def _populate_queue(self, count: int = 5):
        """Populate the product queue"""
        for _ in range(count):
            self.products_queue.append(self._generate_product())
    
    async def reset(self) -> ManufacturingQCObservation:
        """Reset the environment to initial state"""
        self.current_step = 0
        self.products_queue = []
        self.stats = ProductionStats()
        self.recent_actions = []
        self.done = False
        self.total_reward = 0.0
        
        # Reset machine status
        self.machine_status = {
            "line_1": "operational",
            "line_2": "operational",
            "line_3": "operational"
        }
        
        # Populate initial queue
        self._populate_queue(10)
        self.current_product = self.products_queue.pop(0) if self.products_queue else None
        
        return ManufacturingQCObservation(
            current_product=self.current_product,
            queue_length=len(self.products_queue),
            production_stats=self.stats,
            recent_actions=[],
            machine_status=self.machine_status,
            message=f"Environment reset. Starting task: {self.current_task.name}"
        )
    
    def _calculate_reward(self, action: ManufacturingQCAction) -> Tuple[float, Dict[str, float]]:
        """Calculate reward based on action taken"""
        components = {}
        total_reward = 0.0
        
        if not self.current_product:
            return 0.0, components
        
        product = self.current_product
        has_defects = len(product.defects) > 0
        quality_below_threshold = product.quality_score < self.stats.current_threshold
        
        if action.action_type == ActionType.APPROVE:
            if not has_defects or not quality_below_threshold:
                # Correct approval
                total_reward += 1.0
                components["correct_approval"] = 1.0
            else:
                # False negative (approved defective product)
                penalty = -2.0 if product.defect_severity in [DefectSeverity.CRITICAL, DefectSeverity.SEVERE] else -1.0
                total_reward += penalty
                components["false_negative"] = penalty
                self.stats.false_negatives += 1
        
        elif action.action_type == ActionType.REJECT:
            if has_defects and quality_below_threshold:
                # Correct rejection
                reward = 1.5 if product.defect_severity in [DefectSeverity.CRITICAL, DefectSeverity.SEVERE] else 1.0
                total_reward += reward
                components["correct_rejection"] = reward
                self.stats.defects_caught += 1
            else:
                # False positive (rejected good product)
                total_reward += -1.5
                components["false_positive"] = -1.5
                self.stats.false_positives += 1
        
        elif action.action_type == ActionType.REWORK:
            if has_defects and product.defect_severity in [DefectSeverity.MINOR, DefectSeverity.MODERATE]:
                # Good rework decision
                total_reward += 0.8
                components["good_rework"] = 0.8
            elif has_defects and product.defect_severity in [DefectSeverity.CRITICAL, DefectSeverity.SEVERE]:
                # Should have rejected, not reworked
                total_reward += -0.5
                components["should_reject"] = -0.5
            else:
                # Unnecessary rework
                total_reward += -1.0
                components["unnecessary_rework"] = -1.0
        
        elif action.action_type == ActionType.ADJUST_THRESHOLD:
            # Reward for thoughtful threshold adjustment
            if action.threshold_value is not None:
                if 0.6 <= action.threshold_value <= 0.8:
                    total_reward += 0.5
                    components["threshold_adjustment"] = 0.5
                    self.stats.current_threshold = action.threshold_value
        
        elif action.action_type == ActionType.REQUEST_MAINTENANCE:
            # Check if maintenance is actually needed
            needs_maintenance = any(status == "degraded" for status in self.machine_status.values())
            if needs_maintenance:
                total_reward += 2.0
                components["needed_maintenance"] = 2.0
                self.stats.maintenance_requested += 1
            else:
                total_reward += -0.5
                components["unnecessary_maintenance"] = -0.5
        
        # Efficiency bonus for keeping queue manageable
        if len(self.products_queue) < 5:
            total_reward += 0.2
            components["efficiency_bonus"] = 0.2
        
        return total_reward, components
    
    async def step(self, action: ManufacturingQCAction) -> Tuple[ManufacturingQCObservation, ManufacturingQCReward, bool, Dict[str, Any]]:
        """Execute one step in the environment"""
        if self.done:
            raise RuntimeError("Episode is done. Call reset() to start a new episode.")
        
        self.current_step += 1
        
        # Calculate reward
        reward_value, reward_components = self._calculate_reward(action)
        self.total_reward += reward_value
        
        # Update statistics
        self.stats.total_inspected += 1
        if action.action_type == ActionType.APPROVE:
            self.stats.approved += 1
        elif action.action_type == ActionType.REJECT:
            self.stats.rejected += 1
        elif action.action_type == ActionType.REWORK:
            self.stats.reworked += 1
        
        # Record action
        action_summary = f"Step {self.current_step}: {action.action_type.value} - {action.reason[:50]}"
        self.recent_actions.append(action_summary)
        if len(self.recent_actions) > 5:
            self.recent_actions.pop(0)
        
        # Randomly degrade machine status for adaptive task
        if self.task_name == "adaptive_control" and random.random() < 0.1:
            line = random.choice(list(self.machine_status.keys()))
            if self.machine_status[line] == "operational":
                self.machine_status[line] = "degraded"
        
        # Get next product
        if self.products_queue:
            self.current_product = self.products_queue.pop(0)
            # Add new product to queue to maintain flow
            if random.random() < 0.7:
                self.products_queue.append(self._generate_product())
        else:
            self.current_product = None
        
        # Check if episode is done
        if self.current_step >= self.current_task.max_steps or not self.current_product:
            self.done = True
        
        observation = ManufacturingQCObservation(
            current_product=self.current_product,
            queue_length=len(self.products_queue),
            production_stats=self.stats,
            recent_actions=self.recent_actions,
            machine_status=self.machine_status,
            message=f"Action processed. Reward: {reward_value:.2f}"
        )
        
        reward = ManufacturingQCReward(
            reward=reward_value,
            components=reward_components
        )
        
        info = {
            "step": self.current_step,
            "task": self.task_name,
            "accuracy": self._calculate_accuracy()
        }
        
        return observation, reward, self.done, info
    
    def _calculate_accuracy(self) -> float:
        """Calculate current accuracy"""
        if self.stats.total_inspected == 0:
            return 1.0
        errors = self.stats.false_positives + self.stats.false_negatives
        return max(0.0, 1.0 - (errors / self.stats.total_inspected))
    
    async def state(self) -> ManufacturingQCState:
        """Return current environment state"""
        observation = ManufacturingQCObservation(
            current_product=self.current_product,
            queue_length=len(self.products_queue),
            production_stats=self.stats,
            recent_actions=self.recent_actions,
            machine_status=self.machine_status,
            message="Current state"
        )
        
        return ManufacturingQCState(
            current_step=self.current_step,
            task_name=self.task_name,
            observation=observation,
            done=self.done,
            total_reward=self.total_reward
        )
    
    async def close(self):
        """Clean up resources"""
        self.products_queue = []
        self.current_product = None
    
    @classmethod
    async def from_docker_image(cls, image_name: Optional[str] = None, task_name: str = "basic_inspection"):
        """Create environment from Docker image (for compatibility)"""
        # For local development, just return a regular instance
        return cls(task_name=task_name)


# ============================================================================
# Task Graders
# ============================================================================

class TaskGrader:
    """Base class for task graders"""
    
    @staticmethod
    def grade_basic_inspection(env: ManufacturingQCEnv) -> float:
        """Grade the basic inspection task (Easy)"""
        stats = env.stats
        criteria = env.current_task.success_criteria
        
        score = 0.0
        max_score = 3.0
        
        # Accuracy check (0-1.0 points)
        accuracy = env._calculate_accuracy()
        if accuracy >= criteria["min_accuracy"]:
            score += 1.0
        else:
            score += accuracy / criteria["min_accuracy"]
        
        # Defects caught check (0-1.0 points)
        defects_ratio = min(1.0, stats.defects_caught / criteria["min_defects_caught"])
        score += defects_ratio
        
        # False positives check (0-1.0 points)
        if stats.false_positives <= criteria["max_false_positives"]:
            score += 1.0
        else:
            penalty = min(1.0, (stats.false_positives - criteria["max_false_positives"]) * 0.2)
            score += max(0.0, 1.0 - penalty)
        
        return min(1.0, score / max_score)
    
    @staticmethod
    def grade_optimized_throughput(env: ManufacturingQCEnv) -> float:
        """Grade the optimized throughput task (Medium)"""
        stats = env.stats
        criteria = env.current_task.success_criteria
        
        score = 0.0
        max_score = 4.0
        
        # Accuracy check (0-1.0 points)
        accuracy = env._calculate_accuracy()
        if accuracy >= criteria["min_accuracy"]:
            score += 1.0
        else:
            score += accuracy / criteria["min_accuracy"]
        
        # Throughput check (0-1.0 points)
        throughput = stats.total_inspected
        throughput_ratio = min(1.0, throughput / criteria["min_throughput"])
        score += throughput_ratio
        
        # False negatives check (0-1.0 points)
        if stats.false_negatives <= criteria["max_false_negatives"]:
            score += 1.0
        else:
            penalty = min(1.0, (stats.false_negatives - criteria["max_false_negatives"]) * 0.25)
            score += max(0.0, 1.0 - penalty)
        
        # Threshold optimization (0-1.0 points)
        threshold_diff = abs(stats.current_threshold - criteria["target_threshold"])
        if threshold_diff <= 0.05:
            score += 1.0
        else:
            score += max(0.0, 1.0 - threshold_diff * 2)
        
        return min(1.0, score / max_score)
    
    @staticmethod
    def grade_adaptive_control(env: ManufacturingQCEnv) -> float:
        """Grade the adaptive control task (Hard)"""
        stats = env.stats
        criteria = env.current_task.success_criteria
        
        score = 0.0
        max_score = 5.0
        
        # Accuracy check (0-1.0 points)
        accuracy = env._calculate_accuracy()
        if accuracy >= criteria["min_accuracy"]:
            score += 1.0
        else:
            score += accuracy / criteria["min_accuracy"]
        
        # Defects caught check (0-1.0 points)
        defects_ratio = min(1.0, stats.defects_caught / criteria["min_defects_caught"])
        score += defects_ratio
        
        # Threshold adjustments (0-1.0 points)
        # Note: We track threshold changes by checking if current differs from default
        threshold_adjusted = abs(stats.current_threshold - 0.7) > 0.05
        if threshold_adjusted:
            score += 1.0
        else:
            score += 0.3
        
        # Maintenance requests (0-1.0 points)
        if stats.maintenance_requested >= criteria["maintenance_requests"]:
            score += 1.0
        else:
            score += stats.maintenance_requested / criteria["maintenance_requests"]
        
        # Overall false rate (0-1.0 points)
        if stats.total_inspected > 0:
            false_rate = (stats.false_positives + stats.false_negatives) / stats.total_inspected
            if false_rate <= criteria["max_false_rate"]:
                score += 1.0
            else:
                score += max(0.0, 1.0 - (false_rate - criteria["max_false_rate"]) * 3)
        
        return min(1.0, score / max_score)


# ============================================================================
# Grader Registry
# ============================================================================

GRADERS = {
    "basic_inspection": TaskGrader.grade_basic_inspection,
    "optimized_throughput": TaskGrader.grade_optimized_throughput,
    "adaptive_control": TaskGrader.grade_adaptive_control,
}
