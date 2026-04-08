"""
Manufacturing Quality Control Environment
==========================================

A real-world OpenEnv environment for AI agent training and evaluation.

This package implements a manufacturing quality control simulation where
agents must inspect products, identify defects, and make routing decisions.
"""

from manufacturing_qc_env import (
    ManufacturingQCEnv,
    ManufacturingQCAction,
    ManufacturingQCObservation,
    ManufacturingQCReward,
    ManufacturingQCState,
    ActionType,
    DefectType,
    ProductType,
    DefectSeverity,
    GRADERS,
)

__version__ = "1.0.0"
__author__ = "OpenEnv Hackathon Participant"

__all__ = [
    "ManufacturingQCEnv",
    "ManufacturingQCAction",
    "ManufacturingQCObservation",
    "ManufacturingQCReward",
    "ManufacturingQCState",
    "ActionType",
    "DefectType",
    "ProductType",
    "DefectSeverity",
    "GRADERS",
]