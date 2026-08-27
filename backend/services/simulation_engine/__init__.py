"""
Simulation & Synthetic High-Throughput Traffic Generator
Produces realistic payment flows, coordinated fraud ring spikes, and user recommendation clickstreams.
"""

from backend.services.simulation_engine.generator import FinancialTrafficGenerator, traffic_generator
from backend.services.simulation_engine.fraud_patterns import FraudPatternInjector
from backend.services.simulation_engine.clickstream_generator import ClickstreamGenerator

__all__ = [
    "FinancialTrafficGenerator",
    "traffic_generator",
    "FraudPatternInjector",
    "ClickstreamGenerator",
]
