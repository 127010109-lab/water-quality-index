"""
Core hydrochemical modeling, multi-index calculation, and reporting package.
"""

from .standards import DRINKING_WATER_STANDARDS, WAWQI_CATEGORIES, CCME_CATEGORIES, WATER_PRESETS
from .wqi_calculator import MultiWQIEngine
from .hydrochemistry import HydrochemistryEngine
from .dosing_calculator import EngineeringDosingCalculator
from .recommender import WaterTreatmentRecommender
from .report_generator import WaterReportGenerator

__all__ = [
    "DRINKING_WATER_STANDARDS",
    "WAWQI_CATEGORIES",
    "CCME_CATEGORIES",
    "WATER_PRESETS",
    "MultiWQIEngine",
    "HydrochemistryEngine",
    "EngineeringDosingCalculator",
    "WaterTreatmentRecommender",
    "WaterReportGenerator"
]
