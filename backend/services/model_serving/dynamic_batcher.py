"""
Dynamic Micro-Batching Inference Engine
Queues concurrent single-item inference requests into compact batches to maximize throughput.
"""

import asyncio
import time
from typing import List, Any, Dict, Callable, Optional, Tuple
from backend.core.logging import get_logger

logger = get_logger("serving.batcher")


class DynamicBatcher:
    def __init__(
        self,
        batch_size: int = 32,
        max_latency_ms: float = 2.0,
        executor_func: Optional[Callable[[List[Any]], Any]] = None,
    ):
        self.batch_size = batch_size
        self.max_latency_ms = max_latency_ms
        self.executor_func = executor_func
        self._queue: List[Tuple[Any, asyncio.Future]] = []
        self._lock = asyncio.Lock()
        self._batch_task = None

    async def enqueue(self, item: Any) -> Any:
        loop = asyncio.get_running_loop()
        future = loop.create_future()

        async with self._lock:
            self._queue.append((item, future))
            if len(self._queue) >= self.batch_size:
                await self._flush_locked()
            elif self._batch_task is None:
                self._batch_task = asyncio.create_task(self._delayed_flush())

        return await future

    async def _delayed_flush(self):
        await asyncio.sleep(self.max_latency_ms / 1000.0)
        async with self._lock:
            self._batch_task = None
            if self._queue:
                await self._flush_locked()

    async def _flush_locked(self):
        if not self._queue:
            return
        batch = list(self._queue)
        self._queue.clear()

        items = [item for item, _ in batch]
        futures = [fut for _, fut in batch]

        try:
            if self.executor_func:
                results = await self.executor_func(items)
                for fut, res in zip(futures, results):
                    if not fut.done():
                        fut.set_result(res)
            else:
                for fut, it in zip(futures, items):
                    if not fut.done():
                        fut.set_result(it)
        except Exception as e:
            for fut in futures:
                if not fut.done():
                    fut.set_exception(e)
