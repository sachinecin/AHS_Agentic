"""
Demo of token tracking and cost estimation.
"""
import asyncio
from ahs_agentic import track_tokens, get_tracker, safety_check

# Simulated LLM response for demonstration
class MockLLMResponse:
    def __init__(self, prompt_tokens, completion_tokens):
        self.usage = type('obj', (object,), {
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens
        })()

@track_tokens(model="gpt-4o")
async def analyze_document(document: str):
    """Analyze a document with GPT-4o."""
    # Simulate LLM call
    await asyncio.sleep(0.1)
    
    # Return mock response with token usage
    return MockLLMResponse(prompt_tokens=1500, completion_tokens=500)

@track_tokens(model="gpt-4o-mini")
async def summarize_text(text: str):
    """Summarize text with GPT-4o-mini."""
    await asyncio.sleep(0.05)
    return MockLLMResponse(prompt_tokens=800, completion_tokens=200)

@safety_check(action_description="Update production database with new policy")
async def update_database(policy: str):
    """Update database - requires confirmation."""
    print(f"📝 Database updated with policy: {policy[:50]}...")
    return {"status": "success"}

async def main():
    print("🚀 AHS Cost Tracking Demo\n")
    
    # Run multiple LLM calls
    await analyze_document("Large regulatory document...")
    await summarize_text("Brief summary text...")
    await analyze_document("Another document...")
    
    # Get cost summary
    print("\n" + "="*60)
    print("📊 COST SUMMARY")
    print("="*60)
    tracker = get_tracker()
    summary = tracker.get_summary()
    print(f"Total Calls: {summary['total_calls']}")
    print(f"Total Tokens: {summary['total_tokens']:,}")
    print(f"Total Cost: ${summary['total_cost_usd']:.4f} USD")
    print(f"Avg Latency: {summary['average_latency_ms']:.2f}ms")
    print("\nBy Model:")
    for model, stats in summary['by_model'].items():
        print(f"  {model}: {stats['calls']} calls, ${stats['cost_usd']:.4f}")
    
    # Export report
    tracker.export_to_json("cost_report.json")
    
    # Demonstrate safety check
    print("\n" + "="*60)
    print("🔒 SAFETY CHECK DEMO")
    print("="*60)
    await update_database("New compliance policy v2.0")

if __name__ == "__main__":
    asyncio.run(main())
