"""
Regulatory Compliance Checking Example

Monitor new regulations against existing policies for conflicts.
"""

import asyncio
import numpy as np
from ahs_agentic import SkepticSubroutine
from ahs_agentic.graph import HyperGraph


async def compliance_check_example():
    """
    Check regulatory compliance across policies.
    """
    print("📋 Regulatory Compliance Checking Example\n")
    
    skeptic = SkepticSubroutine(sensitivity_threshold=0.85)
    graph = HyperGraph()
    
    # Internal policies
    policies = [
        {"id": "pol_001", "content": "Data retention: minimum 7 years", "type": "internal"},
        {"id": "pol_002", "content": "Customer data encryption: AES-256 required", "type": "internal"},
        {"id": "pol_003", "content": "Access logs: maintained for 3 years", "type": "internal"},
    ]
    
    # New regulation
    regulation = {
        "id": "reg_001",
        "content": "GDPR Article 17: Right to erasure within 30 days",
        "type": "regulation"
    }
    
    print("📊 Loading Internal Policies...")
    for policy in policies:
        graph.add_node(
            node_id=policy["id"],
            content=policy["content"],
            vector=np.random.rand(768),
            type=policy["type"]
        )
        print(f"  ✓ {policy['content']}")
    
    print(f"\n📜 New Regulation: {regulation['content']}")
    graph.add_node(
        node_id=regulation["id"],
        content=regulation["content"],
        vector=np.random.rand(768),
        type=regulation["type"]
    )
    
    # Check for conflicts
    print("\n🔍 Checking for Compliance Conflicts...")
    
    # Simulate conflict with data retention policy
    delta = 0.88  # High conflict
    
    if delta > skeptic.threshold:
        print("  ⚠️  COMPLIANCE CONFLICT DETECTED!")
        print(f"     Policy: {policies[0]['content']}")
        print(f"     Regulation: {regulation['content']}")
        print(f"     Conflict Score: {delta:.2f}")
        print(f"     Risk Level: HIGH")
        print(f"     Action Required: Policy update needed")
    
    print("\n✅ Compliance check complete!")


if __name__ == "__main__":
    asyncio.run(compliance_check_example())
