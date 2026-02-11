"""
Token usage tracking and cost estimation for LLM calls.
"""
import functools
import time
from typing import Any, Callable, Dict
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class TokenUsage:
    """Track token usage for a single LLM call."""
    timestamp: str
    function_name: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    latency_ms: float
    
    # Class constant for consistent rounding
    COST_PRECISION = 6
    LATENCY_PRECISION = 2
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "function": self.function_name,
            "model": self.model,
            "tokens": {
                "input": self.input_tokens,
                "output": self.output_tokens,
                "total": self.total_tokens
            },
            "cost_usd": round(self.estimated_cost_usd, self.COST_PRECISION),
            "latency_ms": round(self.latency_ms, self.LATENCY_PRECISION)
        }


class CostTracker:
    """
    Track and estimate costs for LLM API calls.
    
    Pricing as of 2026 (GPT-4o):
    - Input: $2.50 per 1M tokens
    - Output: $10.00 per 1M tokens
    """
    
    # Rounding precision constants
    SUMMARY_COST_PRECISION = 4
    BREAKDOWN_COST_PRECISION = 4
    LATENCY_PRECISION = 2
    
    # Pricing per 1M tokens (USD)
    PRICING = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
        "gpt-4": {"input": 30.00, "output": 60.00},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    }
    
    def __init__(self):
        self.usage_history: list[TokenUsage] = []
        self.total_cost_usd: float = 0.0
        self.total_tokens: int = 0
    
    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in USD for given token usage."""
        if model not in self.PRICING:
            # Default to gpt-4o pricing if model unknown
            model = "gpt-4o"
        
        pricing = self.PRICING[model]
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        
        return input_cost + output_cost
    
    def track_usage(
        self,
        function_name: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float
    ) -> TokenUsage:
        """Track a single LLM call."""
        total_tokens = input_tokens + output_tokens
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        
        usage = TokenUsage(
            timestamp=datetime.now().isoformat(),
            function_name=function_name,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=cost,
            latency_ms=latency_ms
        )
        
        self.usage_history.append(usage)
        self.total_cost_usd += cost
        self.total_tokens += total_tokens
        
        return usage
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics."""
        if not self.usage_history:
            return {
                "total_calls": 0,
                "total_tokens": 0,
                "total_cost_usd": 0.0,
                "average_latency_ms": 0.0
            }
        
        avg_latency = sum(u.latency_ms for u in self.usage_history) / len(self.usage_history)
        
        return {
            "total_calls": len(self.usage_history),
            "total_tokens": self.total_tokens,
            "total_cost_usd": round(self.total_cost_usd, self.SUMMARY_COST_PRECISION),
            "average_latency_ms": round(avg_latency, self.LATENCY_PRECISION),
            "by_model": self._get_breakdown_by_model()
        }
    
    def _get_breakdown_by_model(self) -> Dict[str, Dict[str, Any]]:
        """Get cost breakdown by model."""
        breakdown = {}
        for usage in self.usage_history:
            if usage.model not in breakdown:
                breakdown[usage.model] = {
                    "calls": 0,
                    "tokens": 0,
                    "cost_usd": 0.0
                }
            breakdown[usage.model]["calls"] += 1
            breakdown[usage.model]["tokens"] += usage.total_tokens
            breakdown[usage.model]["cost_usd"] += usage.estimated_cost_usd
        
        # Round costs
        for model in breakdown:
            breakdown[model]["cost_usd"] = round(breakdown[model]["cost_usd"], self.BREAKDOWN_COST_PRECISION)
        
        return breakdown
    
    def export_to_json(self, filepath: str = "token_usage_report.json"):
        """Export usage history to JSON file."""
        report = {
            "summary": self.get_summary(),
            "usage_history": [u.to_dict() for u in self.usage_history]
        }
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Token usage report exported to {filepath}")

# Global tracker instance
_global_tracker = CostTracker()

def get_tracker() -> CostTracker:
    """Get the global cost tracker instance."""
    return _global_tracker

def track_tokens(model: str = "gpt-4o"):
    """
    Decorator to track token usage and cost for LLM calls.
    
    Usage:
        @track_tokens(model="gpt-4o")
        async def my_llm_call(...):
            # Your LLM call here
            return response
    
    The decorated function should return a dict or object with:
    - 'usage' key containing 'prompt_tokens' and 'completion_tokens'
    OR
    - 'input_tokens' and 'output_tokens' attributes
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            result = await func(*args, **kwargs)
            latency_ms = (time.time() - start_time) * 1000
            
            # Extract token usage
            input_tokens, output_tokens = _extract_tokens(result)
            
            # Track usage
            usage = _global_tracker.track_usage(
                function_name=func.__name__,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=latency_ms
            )
            
            # Print summary
            print(f"📊 {func.__name__} | {model}")
            print(f"   Tokens: {input_tokens} in + {output_tokens} out = {usage.total_tokens} total")
            print(f"   Cost: ${usage.estimated_cost_usd:.6f} USD | Latency: {latency_ms:.2f}ms")
            
            return result
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            latency_ms = (time.time() - start_time) * 1000
            
            # Extract token usage
            input_tokens, output_tokens = _extract_tokens(result)
            
            # Track usage
            usage = _global_tracker.track_usage(
                function_name=func.__name__,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=latency_ms
            )
            
            # Print summary
            print(f"📊 {func.__name__} | {model}")
            print(f"   Tokens: {input_tokens} in + {output_tokens} out = {usage.total_tokens} total")
            print(f"   Cost: ${usage.estimated_cost_usd:.6f} USD | Latency: {latency_ms:.2f}ms")
            
            return result
        
        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator

def _extract_tokens(result: Any) -> tuple[int, int]:
    """Extract input/output tokens from LLM response."""
    # OpenAI format
    if hasattr(result, 'usage'):
        usage = result.usage
        if hasattr(usage, 'prompt_tokens') and hasattr(usage, 'completion_tokens'):
            return usage.prompt_tokens, usage.completion_tokens
    
    # Dict format
    if isinstance(result, dict):
        if 'usage' in result:
            usage = result['usage']
            return usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0)
        if 'input_tokens' in result and 'output_tokens' in result:
            return result['input_tokens'], result['output_tokens']
    
    # Fallback
    return 0, 0
