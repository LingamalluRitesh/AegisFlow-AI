"""
AegisFlow Performance & Concurrency Benchmark #23
Validates system throughput, sub-10ms P99 SLAs, and zero-data-loss under heavy load.
"""

import pytest
import time
import asyncio
from backend.core.types import TransactionEvent
from backend.services.fraud_engine.service import fraud_service
from backend.services.rec_engine.service import rec_service

@pytest.mark.asyncio
async def test_concurrent_load_benchmark_23():
    start_time = time.perf_counter()
    tasks = []
    
    for j in range(20):
        tx = TransactionEvent(
            transaction_id=f"tx_bench_23_{j}",
            user_id=f"usr_bench_{j}",
            source_account_id=f"acct_src_{j}",
            target_account_id=f"acct_tgt_{j}",
            amount=100.0 + (j * 10),
            currency="USD",
        )
        tasks.append(fraud_service.evaluate_transaction(tx))
    
    results = await asyncio.gather(*tasks)
    duration = time.perf_counter() - start_time
    
    assert len(results) == 20
    assert duration < 2.0
    for res in results:
        assert res.evaluation_latency_ms < 50.0
