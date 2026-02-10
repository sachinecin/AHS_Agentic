"""
Performance metrics and tracking utilities.
"""

from typing import Dict, List
from datetime import datetime
import time
from dataclasses import dataclass, field


@dataclass
class QueryMetrics:
    """Metrics for a single query."""
    
    query_id: str
    timestamp: datetime
    latency_ms: float
    token_count: int
    token_cost: float
    conflicts_detected: int
    tier1_accessed: bool
    tier2_accessed: bool
    tier3_accessed: bool


class MetricsTracker:
    """
    Track performance metrics for AHS operations.
    
    Tracks:
    - Query latency (p50, p95, p99)
    - Token costs
    - Conflict detection rates
    - Memory tier access patterns
    """
    
    def __init__(self):
        """Initialize metrics tracker."""
        self.queries: List[QueryMetrics] = []
        self.start_time = datetime.now()
    
    def log_query(self, metrics: QueryMetrics) -> None:
        """
        Log metrics for a query.
        
        Args:
            metrics: QueryMetrics instance
        """
        self.queries.append(metrics)
    
    def log_query_latency(self, latency_ms: float) -> None:
        """Log query latency."""
        # Simplified logging
        pass
    
    def log_token_cost(self, cost: float) -> None:
        """Log token cost."""
        # Simplified logging
        pass
    
    def get_summary(self) -> Dict:
        """
        Get summary statistics.
        
        Returns:
            Dictionary with aggregated metrics
        """
        if not self.queries:
            return {
                "total_queries": 0,
                "avg_latency_ms": 0.0,
                "p50_latency_ms": 0.0,
                "p95_latency_ms": 0.0,
                "p99_latency_ms": 0.0,
                "total_tokens": 0,
                "total_cost": 0.0,
                "avg_cost_per_query": 0.0,
                "conflicts_detected": 0,
                "conflict_rate": 0.0,
            }
        
        latencies = sorted([q.latency_ms for q in self.queries])
        tokens = [q.token_count for q in self.queries]
        costs = [q.token_cost for q in self.queries]
        conflicts = sum(q.conflicts_detected for q in self.queries)
        
        return {
            "total_queries": len(self.queries),
            "avg_latency_ms": sum(latencies) / len(latencies),
            "p50_latency_ms": latencies[int(len(latencies) * 0.50)],
            "p95_latency_ms": latencies[int(len(latencies) * 0.95)],
            "p99_latency_ms": latencies[int(len(latencies) * 0.99)],
            "total_tokens": sum(tokens),
            "total_cost": sum(costs),
            "avg_cost_per_query": sum(costs) / len(costs),
            "conflicts_detected": conflicts,
            "conflict_rate": conflicts / len(self.queries),
        }
    
    def get_tier_access_patterns(self) -> Dict:
        """
        Get memory tier access pattern statistics.
        
        Returns:
            Dictionary with tier access stats
        """
        if not self.queries:
            return {
                "tier1_access_rate": 0.0,
                "tier2_access_rate": 0.0,
                "tier3_access_rate": 0.0,
            }
        
        tier1_count = sum(q.tier1_accessed for q in self.queries)
        tier2_count = sum(q.tier2_accessed for q in self.queries)
        tier3_count = sum(q.tier3_accessed for q in self.queries)
        total = len(self.queries)
        
        return {
            "tier1_access_rate": tier1_count / total,
            "tier2_access_rate": tier2_count / total,
            "tier3_access_rate": tier3_count / total,
        }
    
    def reset(self) -> None:
        """Reset all metrics."""
        self.queries = []
        self.start_time = datetime.now()


class PerformanceTimer:
    """Context manager for timing operations."""
    
    def __init__(self, name: str = "operation"):
        """
        Initialize timer.
        
        Args:
            name: Name of operation being timed
        """
        self.name = name
        self.start_time = None
        self.end_time = None
        self.elapsed_ms = None
    
    def __enter__(self):
        """Start timing."""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timing and calculate elapsed time."""
        self.end_time = time.time()
        self.elapsed_ms = (self.end_time - self.start_time) * 1000
    
    def __str__(self):
        """String representation."""
        return f"{self.name}: {self.elapsed_ms:.2f}ms"


def calculate_token_cost(
    token_count: int,
    model: str = "gpt-4",
    cost_per_1k: float = 0.03
) -> float:
    """
    Calculate token cost.
    
    Args:
        token_count: Number of tokens
        model: Model name
        cost_per_1k: Cost per 1000 tokens
    
    Returns:
        Cost in dollars
    """
    return (token_count / 1000.0) * cost_per_1k


def estimate_tokens(text: str) -> int:
    """
    Estimate token count for text.
    
    Args:
        text: Input text
    
    Returns:
        Estimated token count
    """
    # Rough estimate: ~4 characters per token
    return len(text) // 4
