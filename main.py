"""
AegisFlow AI Main Application Entry Point
Supports running API Gateway, Stream Worker, Simulation Generator, and Evaluation Benchmarks.
"""

import sys
import os
import argparse
import asyncio
import uvicorn

# Ensure repository root is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.core.config import settings
from backend.core.logging import configure_logging, get_logger

configure_logging(level="INFO", service_name="AegisFlow-AI")
logger = get_logger("aegisflow.main")


def run_gateway(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Starts the FastAPI API Gateway with WebSocket telemetry."""
    logger.info_ctx(f"Starting AegisFlow API Gateway on {host}:{port}")
    uvicorn.run("backend.services.gateway.app:app", host=host, port=port, reload=reload)


async def run_stream_processor():
    """Starts the distributed stream processing engine."""
    logger.info_ctx("Starting AegisFlow StreamEngine Processor...")
    from backend.services.stream_processor.engine import StreamProcessorEngine
    processor = StreamProcessorEngine()
    await processor.start()


def run_simulator(rate: int = 100, fraud_ratio: float = 0.05):
    """Starts the real-time financial transaction generator."""
    logger.info_ctx(f"Starting Traffic Simulator at {rate} EPS (fraud ratio: {fraud_ratio})...")
    from backend.services.simulation_engine.generator import SimulationEngine
    sim = SimulationEngine()
    sim.start(rate_per_second=rate, fraud_ratio=fraud_ratio)


def run_tests():
    """Runs test suite with coverage."""
    import pytest
    logger.info_ctx("Executing AegisFlow Unit & Integration Test Suite...")
    exit_code = pytest.main(["tests/", "-v", "--cov=backend", "--cov-report=term-missing"])
    sys.exit(exit_code)


def main():
    parser = argparse.ArgumentParser(
        description="AegisFlow AI: Enterprise Streaming Intelligence & Risk Mesh",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["gateway", "stream", "simulator", "test", "all"],
        default="gateway",
        help="Operating mode for AegisFlow platform",
    )
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Binding host for API gateway")
    parser.add_argument("--port", type=int, default=8000, help="Binding port for API gateway")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    parser.add_argument("--eps", type=int, default=100, help="Events per second for simulator")
    parser.add_argument("--fraud-ratio", type=float, default=0.05, help="Fraud injection ratio")

    args = parser.parse_args()

    if args.mode == "gateway":
        run_gateway(host=args.host, port=args.port, reload=args.reload)
    elif args.mode == "stream":
        asyncio.run(run_stream_processor())
    elif args.mode == "simulator":
        run_simulator(rate=args.eps, fraud_ratio=args.fraud_ratio)
    elif args.mode == "test":
        run_tests()
    elif args.mode == "all":
        logger.info_ctx("Starting full AegisFlow stack...")
        run_gateway(host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
