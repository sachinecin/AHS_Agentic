# Getting Started with AHS Agentic

This guide will help you get up and running with AHS (Agentic Hyper-Graph Synapse) in minutes.

## Installation

### Requirements

- Python 3.9 or higher
- pip (latest version recommended)

### Install from PyPI

```bash
pip install ahs-agentic
```

### Install with Optional Dependencies

```bash
# Development dependencies (testing, linting, etc.)
pip install ahs-agentic[dev]

# Documentation dependencies
pip install ahs-agentic[docs]

# Benchmarking dependencies
pip install ahs-agentic[benchmark]

# All dependencies
pip install ahs-agentic[all]
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/sachinecin/AHS_Agentic.git
cd AHS_Agentic

# Install in development mode
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### Verify Installation

```python
import ahs_agentic
print(ahs_agentic.__version__)  # Should print: 1.0.0
```

## Basic Concepts

### 1. The Hyper-Graph State

Unlike traditional RAG systems that use linear context windows, AHS maintains a **graph state** where:
- **Nodes** represent facts or pieces of information
- **Edges** represent semantic relationships between facts
- **Conflicts** are first-class citizens that trigger special handling

```python
from ahs_agentic import HyperGraphAgent

# Create an agent with graph state
agent = HyperGraphAgent()

# Facts persist in the graph across queries
agent.add_fact("Patient John Doe is 45 years old")
agent.add_fact("John Doe has Type 2 diabetes")
agent.add_fact("John Doe is allergic to sulfa drugs")
```

### 2. The Skeptic Subroutine

The Skeptic actively monitors for conflicts between new evidence and existing facts:

```python
from ahs_agentic import SkepticSubroutine

# Initialize Skeptic with sensitivity threshold
skeptic = SkepticSubroutine(sensitivity_threshold=0.85)

# Skeptic computes conflict delta between facts
import numpy as np
vec1 = np.array([1.0, 0.0, 0.0])  # Existing fact embedding
vec2 = np.array([0.0, 1.0, 0.0])  # New evidence embedding

delta = skeptic.compute_conflict_delta(vec1, vec2)
if skeptic.should_trigger(delta):
    print("⚠️  Conflict detected!")
```

### 3. Speculative Parallel Retrieval

Execute multiple vector database queries concurrently for faster retrieval:

```python
from ahs_agentic import SpeculativeRetriever
import asyncio

# Create retriever with concurrency limit
retriever = SpeculativeRetriever(max_parallel_hops=5)

# Execute parallel searches
async def search():
    queries = [
        "Patient medical history",
        "Current medications",
        "Known allergies"
    ]
    results = await retriever.parallel_hop(queries)
    return results

# Run the search
results = asyncio.run(search())
```

### 4. Multi-Tier Memory

AHS automatically manages context across three tiers:
- **Tier 1 (Active)**: Currently relevant facts
- **Tier 2 (Dormant)**: Previously active facts, cached for quick re-activation
- **Tier 3 (Deep)**: Long-term storage in vector database

Facts automatically move between tiers based on usage patterns and salience scores.

## Your First AHS Agent

Let's build a simple medical record reconciliation agent:

```python
from ahs_agentic import HyperGraphAgent, SkepticSubroutine
import numpy as np

# Step 1: Initialize agent with Skeptic
agent = HyperGraphAgent(
    skeptic=SkepticSubroutine(sensitivity_threshold=0.85)
)

# Step 2: Add facts from different sources
agent.add_fact(
    content="Patient is allergic to penicillin",
    source="Hospital A Records",
    embedding=np.random.rand(768)  # In real use, generate proper embeddings
)

agent.add_fact(
    content="Patient prescribed amoxicillin 500mg",
    source="Pharmacy Database",
    embedding=np.random.rand(768)
)

# Step 3: Check for conflicts
conflicts = agent.detect_conflicts()

if conflicts:
    for conflict in conflicts:
        print(f"⚠️  Conflict: {conflict['description']}")
        print(f"   Sources: {conflict['sources']}")
        print(f"   Confidence: {conflict['confidence']:.2f}")
        print(f"   Recommended Action: {conflict['recommended_action']}")
else:
    print("✅ No conflicts detected")

# Step 4: Query the graph state
result = agent.query("What medications is the patient taking?")
print(f"\nQuery Result: {result}")
```

## Common Patterns

### Pattern 1: Batch Document Ingestion

```python
documents = [
    {"content": "...", "source": "Doc1", "embedding": ...},
    {"content": "...", "source": "Doc2", "embedding": ...},
    # ... more documents
]

for doc in documents:
    agent.add_fact(
        content=doc["content"],
        source=doc["source"],
        embedding=doc["embedding"]
    )

# Check for conflicts after batch ingestion
conflicts = agent.detect_conflicts()
```

### Pattern 2: Streaming Updates

```python
# Add facts as they arrive
def on_new_fact(fact):
    agent.add_fact(
        content=fact["content"],
        source=fact["source"],
        embedding=fact["embedding"]
    )
    
    # Immediately check for conflicts
    conflicts = agent.detect_conflicts()
    if conflicts:
        handle_conflicts(conflicts)
```

### Pattern 3: Conflict Resolution with Human Review

```python
conflicts = agent.detect_conflicts()

for conflict in conflicts:
    if conflict["confidence"] > 0.95:
        # High confidence conflict - escalate to human
        escalate_to_human(conflict)
    elif conflict["confidence"] > 0.80:
        # Medium confidence - attempt automatic resolution
        resolution = agent.resolve_conflict(
            conflict,
            strategy="temporal_precedence"  # Newer fact wins
        )
    else:
        # Low confidence - log for later review
        log_for_review(conflict)
```

### Pattern 4: Performance Optimization

```python
# Use parallel retrieval for multiple queries
retriever = SpeculativeRetriever(max_parallel_hops=10)

async def process_batch(queries):
    # All queries execute concurrently
    results = await retriever.parallel_hop(queries)
    
    # Process results
    for query, result in zip(queries, results):
        agent.add_fact(
            content=result["content"],
            source=result["source"],
            embedding=result["embedding"]
        )

# Execute
queries = ["query1", "query2", "query3", ...]
asyncio.run(process_batch(queries))
```

## Configuration Options

### Skeptic Sensitivity

```python
# Conservative: Only obvious conflicts
skeptic = SkepticSubroutine(sensitivity_threshold=0.95)

# Balanced (default): Most conflicts with low false positives
skeptic = SkepticSubroutine(sensitivity_threshold=0.85)

# Aggressive: High sensitivity, may require more human review
skeptic = SkepticSubroutine(sensitivity_threshold=0.75)
```

### Parallel Retrieval Tuning

```python
# Low concurrency for rate-limited APIs
retriever = SpeculativeRetriever(max_parallel_hops=2)

# High concurrency for high-throughput scenarios
retriever = SpeculativeRetriever(max_parallel_hops=20)
```

### Memory Tier Configuration

```python
agent = HyperGraphAgent(
    tier1_size=256,      # Active context size (tokens)
    tier2_size=2048,     # Dormant cache size (tokens)
    tier3_enabled=True   # Enable deep storage
)
```

## Debugging and Logging

Enable detailed logging to understand what AHS is doing:

```python
import logging

# Set logging level
logging.basicConfig(level=logging.DEBUG)

# AHS will now output detailed logs
logger = logging.getLogger("ahs_agentic")
logger.setLevel(logging.DEBUG)
```

## Performance Monitoring

Track performance metrics:

```python
# Get query metrics
metrics = agent.get_metrics()

print(f"Total Queries: {metrics['total_queries']}")
print(f"Average Latency: {metrics['avg_latency_ms']}ms")
print(f"Conflicts Detected: {metrics['conflicts_detected']}")
print(f"Token Cost: ${metrics['total_token_cost']:.2f}")
```

## Next Steps

Now that you understand the basics:

1. **[Explore Examples](examples.md)** - See AHS in action with real-world scenarios
2. **[Read API Reference](api-reference.md)** - Detailed documentation of all classes and methods
3. **[Optimize Performance](performance.md)** - Learn how to maximize throughput and minimize costs
4. **[Deep Dive into Architecture](architecture-deep-dive.md)** - Understand the technical internals

## Troubleshooting

### Import Error

```
ImportError: No module named 'ahs_agentic'
```

**Solution**: Ensure AHS is installed: `pip install ahs-agentic`

### Conflict Detection Not Working

**Check**:
1. Are embeddings properly generated?
2. Is the Skeptic threshold appropriate for your use case?
3. Are facts actually conflicting (high semantic divergence)?

### Slow Performance

**Optimization**:
1. Increase `max_parallel_hops` for concurrent retrieval
2. Reduce `tier1_size` if context is too large
3. Use batch processing for multiple queries
4. Check vector database performance

## Getting Help

- **Documentation**: https://github.com/sachinecin/AHS_Agentic/docs
- **Issues**: https://github.com/sachinecin/AHS_Agentic/issues
- **Discussions**: https://github.com/sachinecin/AHS_Agentic/discussions
- **Discord**: https://discord.gg/ahs-framework

---

Happy building with AHS! 🚀
