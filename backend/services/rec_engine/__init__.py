"""
PulseRec: Real-Time Contextual Recommendation Engine
Two-Stage Retrieval + DLRM Multi-Task Ranking + Contextual Multi-Armed Bandits.
"""

from backend.services.rec_engine.vector_index import HNSWVectorIndex
from backend.services.rec_engine.dual_tower import DualTowerEmbeddingGenerator
from backend.services.rec_engine.dlrm_ranker import DLRMMultiTaskRanker
from backend.services.rec_engine.contextual_bandit import LinUCBBandit, ThompsonSamplingBandit
from backend.services.rec_engine.reranker import MaximalMarginalRelevanceReranker
from backend.services.rec_engine.feedback_loop import StreamingFeedbackProcessor, rec_feedback_processor
from backend.services.rec_engine.service import PulseRecService, rec_service

__all__ = [
    "HNSWVectorIndex",
    "DualTowerEmbeddingGenerator",
    "DLRMMultiTaskRanker",
    "LinUCBBandit",
    "ThompsonSamplingBandit",
    "MaximalMarginalRelevanceReranker",
    "StreamingFeedbackProcessor",
    "rec_feedback_processor",
    "PulseRecService",
    "rec_service",
]
