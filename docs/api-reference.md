# API Reference

Complete API documentation for AHS Agentic framework.

## Core Classes

### HyperGraphAgent

Main agent class that manages the probabilistic graph state.

```python
from ahs_agentic import HyperGraphAgent
```

#### Constructor

```python
HyperGraphAgent(
    skeptic: Optional[SkepticSubroutine] = None,
    max_parallel_hops: int = 5,
    tier1_size: int = 256,
    tier2_size: int = 2048,
    tier3_enabled: bool = True
)
```

**Parameters**:
- `skeptic` (SkepticSubroutine, optional): Conflict detection subroutine
- `max_parallel_hops` (int): Maximum concurrent retrieval operations
- `tier1_size` (int): Active context size in tokens
- `tier2_size` (int): Dormant cache size in tokens
- `tier3_enabled` (bool): Enable deep storage tier

#### Methods

##### `add_fact(content, source, embedding, **metadata)`

Add a new fact to the graph state.

**Parameters**:
- `content` (str): Human-readable fact content
- `source` (str): Source identifier
- `embedding` (np.ndarray): 768-dimensional embedding vector
- `**metadata`: Additional metadata (author, timestamp, etc.)

**Returns**: `str` - Unique fact ID

**Example**:
```python
fact_id = agent.add_fact(
    content="Patient allergic to penicillin",
    source="Hospital A",
    embedding=embedding_vector,
    timestamp="2026-02-10T15:30:00Z"
)
```

##### `detect_conflicts(threshold=None)`

Detect conflicts in the graph state.

**Parameters**:
- `threshold` (float, optional): Override default Skeptic threshold

**Returns**: `List[dict]` - List of conflict reports

**Example**:
```python
conflicts = agent.detect_conflicts()
for conflict in conflicts:
    print(conflict["description"])
```

##### `query(query_text, k=10)`

Query the graph state.

**Parameters**:
- `query_text` (str): Natural language query
- `k` (int): Number of results to return

**Returns**: `dict` - Query results with context

##### `get_metrics()`

Get performance metrics.

**Returns**: `dict` - Metrics dictionary

---

### SkepticSubroutine

Conflict detection and resolution engine.

```python
from ahs_agentic import SkepticSubroutine
```

#### Constructor

```python
SkepticSubroutine(sensitivity_threshold: float = 0.85)
```

**Parameters**:
- `sensitivity_threshold` (float): Conflict detection threshold (0.0-1.0)

#### Methods

##### `compute_conflict_delta(existing_fact_vector, new_evidence_vector)`

Compute semantic divergence between fact vectors.

**Parameters**:
- `existing_fact_vector` (np.ndarray): Embedding of existing fact
- `new_evidence_vector` (np.ndarray): Embedding of new evidence

**Returns**: `float` - Conflict delta score (0.0-1.0)

**Example**:
```python
skeptic = SkepticSubroutine(sensitivity_threshold=0.85)
delta = skeptic.compute_conflict_delta(vec1, vec2)
print(f"Conflict score: {delta:.2f}")
```

##### `should_trigger(delta)`

Determine if Skeptic should trigger based on delta.

**Parameters**:
- `delta` (float): Conflict delta score

**Returns**: `bool` - True if delta exceeds threshold

##### `generate_conflict_report(existing_premise, new_evidence, delta)`

Generate structured conflict report.

**Parameters**:
- `existing_premise` (str): Existing fact content
- `new_evidence` (str): New evidence content
- `delta` (float): Conflict delta score

**Returns**: `dict` - Structured conflict report

---

### SpeculativeRetriever

Parallel retrieval engine for vector databases.

```python
from ahs_agentic import SpeculativeRetriever
```

#### Constructor

```python
SpeculativeRetriever(max_parallel_hops: int = 5)
```

**Parameters**:
- `max_parallel_hops` (int): Maximum concurrent operations

#### Methods

##### `async parallel_hop(queries)`

Execute multiple queries in parallel.

**Parameters**:
- `queries` (List[str]): List of query strings

**Returns**: `List[dict]` - List of results

**Example**:
```python
import asyncio

retriever = SpeculativeRetriever(max_parallel_hops=5)
queries = ["query1", "query2", "query3"]
results = await retriever.parallel_hop(queries)
```

##### `async batch_with_backpressure(queries, batch_size=10)`

Process large query batches with backpressure control.

**Parameters**:
- `queries` (List[str]): List of queries
- `batch_size` (int): Batch size for processing

**Returns**: `List[dict]` - Aggregated results

---

## Utility Functions

### Embedding Generation

```python
from ahs_agentic.utils import generate_embedding

embedding = generate_embedding(text="Patient has diabetes", model="text-embedding-ada-002")
```

### Metric Tracking

```python
from ahs_agentic.utils.metrics import MetricsTracker

tracker = MetricsTracker()
tracker.log_query_latency(280)  # milliseconds
tracker.log_token_cost(0.03)    # dollars

summary = tracker.get_summary()
```

---

## Data Structures

### FactNode

```python
class FactNode:
    id: str
    content: str
    vector: np.ndarray
    salience_score: float
    tier: int  # 1, 2, or 3
    source_metadata: dict
    access_count: int
    last_accessed: datetime
    conflict_history: List[str]
```

### ConflictReport

```python
{
    "conflict_detected": bool,
    "delta_score": float,
    "conflicting_facts": List[dict],
    "resolution_strategy": str,
    "confidence": float,
    "recommended_action": str,
    "requires_human_review": bool
}
```

---

## Configuration

### Environment Variables

```bash
# Vector database connection
export QDRANT_URL="http://localhost:6333"
export QDRANT_API_KEY="your-api-key"

# OpenAI API (for embeddings)
export OPENAI_API_KEY="your-api-key"

# AHS configuration
export AHS_DEFAULT_THRESHOLD=0.85
export AHS_MAX_PARALLEL_HOPS=5
```

---

## Type Hints

AHS uses type hints throughout:

```python
from typing import Optional, List, Dict, Any
import numpy as np

def add_fact(
    content: str,
    source: str,
    embedding: np.ndarray,
    **metadata: Any
) -> str:
    ...
```

---

## Exceptions

### ConflictDetectionError

Raised when conflict detection fails.

```python
from ahs_agentic.exceptions import ConflictDetectionError

try:
    conflicts = agent.detect_conflicts()
except ConflictDetectionError as e:
    print(f"Conflict detection failed: {e}")
```

### RetrievalError

Raised when parallel retrieval fails.

```python
from ahs_agentic.exceptions import RetrievalError

try:
    results = await retriever.parallel_hop(queries)
except RetrievalError as e:
    print(f"Retrieval failed: {e}")
```

---

## Advanced Usage

### Custom Conflict Resolution

```python
from ahs_agentic import ConflictResolver

resolver = ConflictResolver()
resolver.register_strategy(
    name="domain_expert",
    handler=custom_resolution_function
)
```

### Graph Persistence

```python
# Save graph state
agent.save_state("graph_state.pkl")

# Load graph state
agent = HyperGraphAgent.load_state("graph_state.pkl")
```

---

For more examples, see [Examples](examples.md).
