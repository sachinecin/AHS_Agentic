"""
Tests for cost_tracker module.
"""
import pytest
from ahs_agentic.utils.cost_tracker import CostTracker, TokenUsage, track_tokens, get_tracker, _extract_tokens


class TestCostTracker:
    """Test suite for token tracking and cost estimation."""
    
    def test_calculate_cost_gpt4o(self):
        """Test cost calculation for GPT-4o."""
        tracker = CostTracker()
        cost = tracker.calculate_cost("gpt-4o", input_tokens=1000, output_tokens=500)
        
        # Expected: (1000/1M * $2.50) + (500/1M * $10.00) = $0.0025 + $0.005 = $0.0075
        assert abs(cost - 0.0075) < 0.0001
    
    def test_calculate_cost_gpt4o_mini(self):
        """Test cost calculation for GPT-4o-mini."""
        tracker = CostTracker()
        cost = tracker.calculate_cost("gpt-4o-mini", input_tokens=1000, output_tokens=500)
        
        # Expected: (1000/1M * $0.15) + (500/1M * $0.60) = $0.00015 + $0.0003 = $0.00045
        assert abs(cost - 0.00045) < 0.0001
    
    def test_calculate_cost_unknown_model_defaults_to_gpt4o(self):
        """Test that unknown models default to GPT-4o pricing."""
        tracker = CostTracker()
        cost_unknown = tracker.calculate_cost("unknown-model", input_tokens=1000, output_tokens=500)
        cost_gpt4o = tracker.calculate_cost("gpt-4o", input_tokens=1000, output_tokens=500)
        
        assert cost_unknown == cost_gpt4o
    
    def test_track_usage(self):
        """Test tracking a single LLM call."""
        tracker = CostTracker()
        
        usage = tracker.track_usage(
            function_name="test_function",
            model="gpt-4o",
            input_tokens=1000,
            output_tokens=500,
            latency_ms=123.45
        )
        
        assert usage.function_name == "test_function"
        assert usage.model == "gpt-4o"
        assert usage.input_tokens == 1000
        assert usage.output_tokens == 500
        assert usage.total_tokens == 1500
        assert usage.latency_ms == 123.45
        assert usage.estimated_cost_usd > 0
        
        # Verify tracker state
        assert len(tracker.usage_history) == 1
        assert tracker.total_tokens == 1500
        assert tracker.total_cost_usd > 0
    
    def test_get_summary_empty(self):
        """Test summary with no usage."""
        tracker = CostTracker()
        summary = tracker.get_summary()
        
        assert summary["total_calls"] == 0
        assert summary["total_tokens"] == 0
        assert summary["total_cost_usd"] == 0.0
        assert summary["average_latency_ms"] == 0.0
    
    def test_get_summary_with_usage(self):
        """Test summary with usage data."""
        tracker = CostTracker()
        
        tracker.track_usage("func1", "gpt-4o", 1000, 500, 100.0)
        tracker.track_usage("func2", "gpt-4o-mini", 800, 200, 50.0)
        tracker.track_usage("func3", "gpt-4o", 1500, 750, 150.0)
        
        summary = tracker.get_summary()
        
        assert summary["total_calls"] == 3
        assert summary["total_tokens"] == 1500 + 1000 + 2250
        assert summary["average_latency_ms"] == 100.0
        assert "by_model" in summary
        assert "gpt-4o" in summary["by_model"]
        assert "gpt-4o-mini" in summary["by_model"]
        assert summary["by_model"]["gpt-4o"]["calls"] == 2
        assert summary["by_model"]["gpt-4o-mini"]["calls"] == 1
    
    def test_breakdown_by_model(self):
        """Test cost breakdown by model."""
        tracker = CostTracker()
        
        tracker.track_usage("func1", "gpt-4o", 1000, 500, 100.0)
        tracker.track_usage("func2", "gpt-4o", 1000, 500, 100.0)
        tracker.track_usage("func3", "gpt-4o-mini", 800, 200, 50.0)
        
        breakdown = tracker._get_breakdown_by_model()
        
        assert "gpt-4o" in breakdown
        assert "gpt-4o-mini" in breakdown
        
        # GPT-4o: 2 calls
        assert breakdown["gpt-4o"]["calls"] == 2
        assert breakdown["gpt-4o"]["tokens"] == 3000
        
        # GPT-4o-mini: 1 call
        assert breakdown["gpt-4o-mini"]["calls"] == 1
        assert breakdown["gpt-4o-mini"]["tokens"] == 1000
    
    def test_token_usage_to_dict(self):
        """Test TokenUsage serialization."""
        usage = TokenUsage(
            timestamp="2026-01-01T00:00:00",
            function_name="test_func",
            model="gpt-4o",
            input_tokens=1000,
            output_tokens=500,
            total_tokens=1500,
            estimated_cost_usd=0.0075,
            latency_ms=123.45
        )
        
        data = usage.to_dict()
        
        assert data["timestamp"] == "2026-01-01T00:00:00"
        assert data["function"] == "test_func"
        assert data["model"] == "gpt-4o"
        assert data["tokens"]["input"] == 1000
        assert data["tokens"]["output"] == 500
        assert data["tokens"]["total"] == 1500
        assert data["cost_usd"] == 0.0075
        assert data["latency_ms"] == 123.45
    
    def test_export_to_json(self, tmp_path):
        """Test JSON export functionality."""
        tracker = CostTracker()
        tracker.track_usage("func1", "gpt-4o", 1000, 500, 100.0)
        
        output_file = tmp_path / "test_report.json"
        tracker.export_to_json(str(output_file))
        
        assert output_file.exists()
        
        import json
        with open(output_file, 'r') as f:
            data = json.load(f)
        
        assert "summary" in data
        assert "usage_history" in data
        assert data["summary"]["total_calls"] == 1
        assert len(data["usage_history"]) == 1


class TestExtractTokens:
    """Test token extraction from various response formats."""
    
    def test_extract_tokens_openai_format(self):
        """Test extraction from OpenAI-style response."""
        class MockUsage:
            prompt_tokens = 1000
            completion_tokens = 500
        
        class MockResponse:
            usage = MockUsage()
        
        response = MockResponse()
        input_tokens, output_tokens = _extract_tokens(response)
        
        assert input_tokens == 1000
        assert output_tokens == 500
    
    def test_extract_tokens_dict_format_with_usage(self):
        """Test extraction from dict with usage key."""
        response = {
            'usage': {
                'prompt_tokens': 1000,
                'completion_tokens': 500
            }
        }
        
        input_tokens, output_tokens = _extract_tokens(response)
        
        assert input_tokens == 1000
        assert output_tokens == 500
    
    def test_extract_tokens_dict_format_direct(self):
        """Test extraction from dict with direct token keys."""
        response = {
            'input_tokens': 1000,
            'output_tokens': 500
        }
        
        input_tokens, output_tokens = _extract_tokens(response)
        
        assert input_tokens == 1000
        assert output_tokens == 500
    
    def test_extract_tokens_fallback(self):
        """Test fallback for unknown formats."""
        response = "some string"
        
        input_tokens, output_tokens = _extract_tokens(response)
        
        assert input_tokens == 0
        assert output_tokens == 0


class TestTrackTokensDecorator:
    """Test the track_tokens decorator."""
    
    @pytest.mark.asyncio
    async def test_decorator_async_function(self):
        """Test decorator with async function."""
        class MockResponse:
            def __init__(self):
                self.usage = type('obj', (object,), {
                    'prompt_tokens': 1000,
                    'completion_tokens': 500
                })()
        
        @track_tokens(model="gpt-4o")
        async def mock_llm_call():
            return MockResponse()
        
        # Clear global tracker
        tracker = get_tracker()
        tracker.usage_history.clear()
        tracker.total_cost_usd = 0.0
        tracker.total_tokens = 0
        
        result = await mock_llm_call()
        
        assert result is not None
        assert len(tracker.usage_history) == 1
        assert tracker.usage_history[0].model == "gpt-4o"
        assert tracker.usage_history[0].input_tokens == 1000
        assert tracker.usage_history[0].output_tokens == 500
    
    def test_decorator_sync_function(self):
        """Test decorator with sync function."""
        class MockResponse:
            def __init__(self):
                self.usage = type('obj', (object,), {
                    'prompt_tokens': 800,
                    'completion_tokens': 200
                })()
        
        @track_tokens(model="gpt-4o-mini")
        def mock_llm_call():
            return MockResponse()
        
        # Clear global tracker
        tracker = get_tracker()
        tracker.usage_history.clear()
        tracker.total_cost_usd = 0.0
        tracker.total_tokens = 0
        
        result = mock_llm_call()
        
        assert result is not None
        assert len(tracker.usage_history) == 1
        assert tracker.usage_history[0].model == "gpt-4o-mini"
        assert tracker.usage_history[0].input_tokens == 800
        assert tracker.usage_history[0].output_tokens == 200


class TestGlobalTracker:
    """Test global tracker instance."""
    
    def test_get_tracker_returns_same_instance(self):
        """Test that get_tracker always returns the same instance."""
        tracker1 = get_tracker()
        tracker2 = get_tracker()
        
        assert tracker1 is tracker2
