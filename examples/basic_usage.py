"""
Basic Usage Example for AHS Agentic

This example demonstrates the simplest way to get started with AHS.
It shows how to initialize an agent and perform basic operations.
"""

from ahs_agentic import HyperGraphAgent
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables (API keys)
load_dotenv()


async def main():
    """Main function demonstrating basic AHS usage."""
    
    print("🧠 AHS Agentic - Basic Usage Example")
    print("=" * 60)
    
    # Step 1: Initialize the HyperGraphAgent
    print("\n1️⃣  Initializing agent...")
    agent = HyperGraphAgent(
        memory_mode="latent-layering",           # Enable 3-tier memory
        retrieval_strategy="speculative-parallel",  # Parallel hop retrieval
        skeptic_threshold=0.85                   # Conflict detection sensitivity
    )
    print("   ✅ Agent initialized successfully!")
    
    # Step 2: Simple conflict resolution
    print("\n2️⃣  Performing conflict resolution...")
    result = await agent.resolve_conflict(
        legacy_sop="Employees must work from office 5 days per week",
        new_regulation="Updated policy: Hybrid work allowed (3 days office, 2 days remote)",
        context="Remote Work Policy Update"
    )
    
    # Step 3: Display results
    print("\n3️⃣  Results:")
    print("-" * 60)
    print(f"   Status: {result['status']}")
    print(f"   Decision Velocity: {result['velocity_gain']:.1f}x faster")
    print(f"   Token Savings: {result['token_savings'] * 100:.1f}%")
    print(f"   Reasoning Quality: {result['reasoning_regret_reduction'] * 100:.1f}% improvement")
    print("-" * 60)
    
    # Step 4: Check performance metrics
    print("\n4️⃣  Performance Metrics:")
    metrics = agent.get_metrics()
    print(f"   Decision Velocity: {metrics['decision_velocity']:.2f}x")
    print(f"   Reasoning Regret: {metrics['reasoning_regret']:.2%}")
    print(f"   Token Efficiency: {metrics['token_efficiency']:.2f}")
    
    print("\n✨ Example completed successfully!")
    print("=" * 60)


def example_synchronous():
    """
    For environments where async is not convenient,
    you can use asyncio.run() to execute async functions.
    """
    print("\n📝 Running synchronous wrapper example...")
    asyncio.run(main())


if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
    
    print("\n💡 Next Steps:")
    print("   - Try examples/forensic_reconciliation.py for advanced conflict resolution")
    print("   - Try examples/regulatory_compliance.py for a real-world use case")
    print("   - Read docs/getting-started.md for more details")
