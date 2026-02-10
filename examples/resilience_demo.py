"""
Demonstration of LLM Resilience Layer:
Shows how retry logic and prompt trimming work in practice.
"""
from src.ahs_agentic.core.resilience import (
    LLMResilientCaller,
    resilient_llm_call,
    RateLimitError
)
import time

def demo_basic_retry():
    """Demonstrate basic retry with exponential backoff"""
    print("=" * 60)
    print("DEMO 1: Rate Limit Retry with Exponential Backoff")
    print("=" * 60)
    
    attempt_count = 0
    
    @resilient_llm_call(max_attempts=4, min_wait=1, max_wait=10)
    def simulated_openai_call(prompt):
        nonlocal attempt_count
        attempt_count += 1
        
        print(f"\n🔄 Attempt {attempt_count}: Calling OpenAI API...")
        
        # Simulate rate limit on first 2 attempts
        if attempt_count < 3:
            print("❌ Rate limit exceeded! Backing off...")
            raise Exception("rate limit exceeded")
        
        print("✅ Success! API call completed.")
        return f"Response after {attempt_count} attempts"
    
    try:
        result = simulated_openai_call("Tell me about synthetic reasoning")
        print(f"\n🎉 Final Result: {result}")
    except RateLimitError:
        print("\n💥 Max attempts exceeded!")

def demo_context_trimming():
    """Demonstrate automatic prompt trimming for context windows"""
    print("\n\n" + "=" * 60)
    print("DEMO 2: Automatic Context Window Management")
    print("=" * 60)
    
    caller = LLMResilientCaller(model="gpt-4", max_tokens=200)
    
    # Create a massive prompt
    huge_prompt = """
    System: You are a helpful assistant.
    
    Context: """ + ("This is important context. " * 500) + """
    
    Question: What is the meaning of life?
    """
    
    print(f"\n📏 Original prompt: {caller.count_tokens(huge_prompt)} tokens")
    
    trimmed = caller.trim_prompt(huge_prompt, target_tokens=200)
    
    print(f"✂️  Trimmed prompt: {caller.count_tokens(trimmed)} tokens")
    print(f"\n📝 Trimmed content preview:\n{trimmed[:300]}...")

def demo_integrated_resilience():
    """Demonstrate full integration with HyperGraphAgent"""
    print("\n\n" + "=" * 60)
    print("DEMO 3: Integration with HyperGraphAgent")
    print("=" * 60)
    
    caller = LLMResilientCaller(max_tokens=4000)
    
    call_history = []
    
    @caller.resilient_llm_call(max_attempts=3, min_wait=1)
    def llm_reasoning_call(prompt):
        call_history.append({
            "timestamp": time.time(),
            "tokens": caller.count_tokens(prompt),
            "prompt_preview": prompt[:100]
        })
        
        # Simulate occasional failures
        if len(call_history) == 1:
            raise Exception("rate limit exceeded")
        
        return "Conflict resolved: Use latest regulation with grandfather clause"
    
    try:
        result = llm_reasoning_call(
            prompt="Analyze conflict between SOPv2 and Regulation2024..."
        )
        
        print(f"\n✅ Resolution: {result}")
        print(f"\n📊 Call Statistics:")
        for i, call in enumerate(call_history, 1):
            print(f"   Attempt {i}: {call['tokens']} tokens at {call['timestamp']:.2f}")
    
    except Exception as e:
        print(f"\n❌ Failed: {e}")


if __name__ == "__main__":
    print("🚀 AHS Resilience Layer Demo\n")
    
    demo_basic_retry()
    demo_context_trimming()
    demo_integrated_resilience()
    
    print("\n\n" + "=" * 60)
    print("✨ All demos completed!")
    print("=" * 60)