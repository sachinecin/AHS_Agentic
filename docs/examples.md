# Examples

Real-world usage examples for AHS Agentic.

## Example 1: Forensic Document Reconciliation

Reconcile conflicting information across multiple medical records.

```python
from ahs_agentic import HyperGraphAgent, SkepticSubroutine
import numpy as np

# Initialize agent
agent = HyperGraphAgent(
    skeptic=SkepticSubroutine(sensitivity_threshold=0.85)
)

# Add facts from different hospitals
hospital_a_facts = [
    {"content": "Patient: John Doe, Age: 45", "source": "Hospital A"},
    {"content": "Allergies: Penicillin, Sulfa drugs", "source": "Hospital A"},
    {"content": "Current Medications: Metformin 500mg", "source": "Hospital A"},
]

hospital_b_facts = [
    {"content": "Patient: John Doe, Age: 45", "source": "Hospital B"},
    {"content": "Allergies: Penicillin", "source": "Hospital B"},
    {"content": "Current Medications: Amoxicillin 250mg", "source": "Hospital B"},
]

# Add all facts
for fact in hospital_a_facts + hospital_b_facts:
    agent.add_fact(
        content=fact["content"],
        source=fact["source"],
        embedding=np.random.rand(768)  # Use real embeddings in production
    )

# Detect conflicts
conflicts = agent.detect_conflicts()

print(f"Found {len(conflicts)} conflicts:")
for conflict in conflicts:
    print(f"\n⚠️  {conflict['description']}")
    print(f"   Confidence: {conflict['confidence']:.2%}")
    print(f"   Action: {conflict['recommended_action']}")
```

## Example 2: Regulatory Compliance Checking

Monitor new regulations against existing policies.

```python
import asyncio
from ahs_agentic import HyperGraphAgent, SpeculativeRetriever

async def compliance_check():
    agent = HyperGraphAgent()
    retriever = SpeculativeRetriever(max_parallel_hops=10)
    
    # Load existing policies
    policies = [
        "Data retention: 7 years minimum",
        "Customer data encryption: AES-256 required",
        "Access logs: Must be maintained for 3 years"
    ]
    
    for policy in policies:
        agent.add_fact(policy, source="Internal Policy")
    
    # New regulation introduced
    new_regulation = "GDPR Article 17: Right to erasure within 30 days"
    agent.add_fact(new_regulation, source="GDPR")
    
    # Check for conflicts
    conflicts = agent.detect_conflicts()
    
    if conflicts:
        print("🚨 Compliance conflicts detected!")
        for conflict in conflicts:
            print(f"Policy: {conflict['existing']}")
            print(f"Regulation: {conflict['new']}")
            print(f"Risk Level: {conflict['severity']}")
    
    return conflicts

asyncio.run(compliance_check())
```

## Example 3: Multi-Document Analysis

Analyze multiple contracts for conflicting terms.

```python
from ahs_agentic import HyperGraphAgent

agent = HyperGraphAgent()

# Contract clauses from different vendors
contracts = {
    "Vendor A": [
        "Payment terms: Net 30 days",
        "Liability cap: $1M",
        "IP rights: Vendor retains all rights"
    ],
    "Vendor B": [
        "Payment terms: Net 45 days",
        "Liability cap: Unlimited",
        "IP rights: Customer receives full transfer"
    ],
    "Vendor C": [
        "Payment terms: Net 30 days",
        "Liability cap: $500K",
        "IP rights: Joint ownership"
    ]
}

# Add all clauses
for vendor, clauses in contracts.items():
    for clause in clauses:
        agent.add_fact(clause, source=vendor)

# Analyze for conflicts
conflicts = agent.detect_conflicts()
grouped = agent.group_conflicts_by_category(conflicts)

for category, items in grouped.items():
    print(f"\n📋 {category} Conflicts:")
    for item in items:
        print(f"  - {item['description']}")
```

## Example 4: Real-Time Streaming Updates

Process incoming facts in real-time with conflict detection.

```python
import asyncio
from ahs_agentic import HyperGraphAgent, SkepticSubroutine

async def streaming_processor():
    agent = HyperGraphAgent(
        skeptic=SkepticSubroutine(sensitivity_threshold=0.85)
    )
    
    async def process_fact(fact):
        # Add fact to graph
        fact_id = agent.add_fact(
            content=fact["content"],
            source=fact["source"],
            embedding=fact["embedding"]
        )
        
        # Immediate conflict check
        conflicts = agent.detect_conflicts()
        
        if conflicts:
            # Escalate high-confidence conflicts
            for conflict in conflicts:
                if conflict["confidence"] > 0.90:
                    await escalate_to_human(conflict)
                else:
                    await log_for_review(conflict)
        
        return fact_id
    
    # Simulate streaming facts
    fact_stream = [
        {"content": "Fact 1", "source": "Stream", "embedding": ...},
        {"content": "Fact 2", "source": "Stream", "embedding": ...},
        # ... more facts
    ]
    
    for fact in fact_stream:
        await process_fact(fact)

asyncio.run(streaming_processor())
```

## Example 5: Custom Conflict Resolution

Implement domain-specific conflict resolution strategies.

```python
from ahs_agentic import HyperGraphAgent, ConflictResolver

def medical_conflict_resolver(conflict):
    """Custom resolver for medical conflicts."""
    # Prioritize hospital records over pharmacy
    sources = [f["source"] for f in conflict["facts"]]
    
    if "Hospital" in sources[0]:
        return {"strategy": "trust_hospital", "winner": conflict["facts"][0]}
    elif all("Pharmacy" in s for s in sources):
        # Among pharmacies, use most recent
        return {"strategy": "most_recent", "winner": max(
            conflict["facts"], 
            key=lambda f: f["timestamp"]
        )}
    else:
        return {"strategy": "human_review", "winner": None}

# Register custom resolver
agent = HyperGraphAgent()
agent.register_resolver("medical", medical_conflict_resolver)

# Use custom resolver
conflicts = agent.detect_conflicts()
for conflict in conflicts:
    resolution = agent.resolve_conflict(conflict, strategy="medical")
    print(f"Resolved: {resolution['strategy']}")
```

For more details, see [API Reference](api-reference.md).
