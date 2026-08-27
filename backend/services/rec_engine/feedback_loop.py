"""
Streaming Feedback Processor
Consumes impression, click, and purchase events to update bandit parameters and model priors in real time.
"""

from typing import Dict, Any
from backend.services.rec_engine.contextual_bandit import LinUCBBandit, ThompsonSamplingBandit
from backend.core.logging import get_logger

logger = get_logger("rec.feedback")


class StreamingFeedbackProcessor:
    def __init__(self):
        self.linucb = LinUCBBandit()
        self.thompson = ThompsonSamplingBandit()

    def process_feedback_event(self, event_type: str, item_id: str, category: str, context_features: Dict[str, Any]) -> None:
        reward = 0.0
        if event_type == "click":
            reward = 0.2
            self.thompson.update_arm(category, converted=True)
        elif event_type == "add_to_cart":
            reward = 0.6
            self.thompson.update_arm(category, converted=True)
        elif event_type == "purchase":
            reward = 1.0
            self.thompson.update_arm(category, converted=True)

        context_vec = [float(v) for v in context_features.values() if isinstance(v, (int, float))]
        self.linucb.update_arm(category, context_vec, reward)
        logger.debug_ctx(f"Processed streaming feedback for item {item_id}: {event_type} (Reward: {reward})")


rec_feedback_processor = StreamingFeedbackProcessor()
