# Architecture Deep Dive

Technical internals of the AHS framework.

## Overview

AHS (Agentic Hyper-Graph Synapse) is built on three core pillars:

1. **Probabilistic Graph State** - Living graph that persists across queries
2. **Skeptic Subroutine** - Active conflict detection and resolution
3. **Multi-Tier Latent Memory** - Intelligent context management

## Component Architecture

```
┌─────────────────────────────────────────┐
│        Application Layer                │
│  (User Queries, API Endpoints)          │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│       HyperGraphAgent Core              │
│  - Query Processing                     │
│  - Fact Management                      │
│  - Conflict Orchestration               │
└──┬───────────┬────────────┬─────────────┘
   │           │            │
   ▼           ▼            ▼
┌────────┐ ┌────────┐ ┌──────────┐
│Skeptic │ │Retriev.│ │ Memory   │
│Subrout.│ │Engine  │ │ Manager  │
└────────┘ └────────┘ └──────────┘
   │           │            │
   └───────────┴────────────┘
               │
┌──────────────▼──────────────────────────┐
│       Storage Layer                     │
│  - Vector Database (Qdrant)             │
│  - Graph Storage (NetworkX)             │
│  - Metadata Store                       │
└─────────────────────────────────────────┘
```

## Detailed Component Design

### 1. Probabilistic Graph State

**Data Structure**:
```python
class GraphState:
    nodes: Dict[str, FactNode]      # O(1) lookup
    edges: List[SemanticEdge]       # Relationships
    tier1: PriorityQueue[FactNode]  # Active context
    tier2: Dict[str, FactNode]      # Dormant cache
    tier3: VectorDBProxy            # Deep storage
```

**Key Operations**:
- `add_node()`: O(1)
- `find_neighbors()`: O(k) where k = degree
- `detect_conflicts()`: O(N) where N = active nodes

### 2. Skeptic Subroutine

**Algorithm**:
```python
def detect_conflict(existing_fact, new_evidence):
    # 1. Compute semantic similarity
    similarity = cosine_similarity(
        existing_fact.vector,
        new_evidence.vector
    )
    
    # 2. Calculate conflict delta
    delta = 1.0 - similarity
    
    # 3. Threshold check
    if delta > threshold:
        # 4. Re-activate dormant facts
        related_facts = graph.find_related(existing_fact)
        
        # 5. Generate conflict report
        return ConflictReport(
            delta=delta,
            facts=[existing_fact, new_evidence],
            related_facts=related_facts
        )
```

### 3. Multi-Tier Memory

**Tier Promotion Logic**:
```python
def promote_to_tier1(fact):
    if fact.salience_score > 0.85:
        tier1.add(fact)
        tier2.remove(fact.id)
    
def demote_to_tier2(fact):
    if fact.access_count < threshold:
        tier2[fact.id] = fact
        tier1.remove(fact)

def archive_to_tier3(fact):
    vector_db.upsert(fact)
    tier2.pop(fact.id)
```

## Performance Characteristics

### Time Complexity

| Operation | Best Case | Average Case | Worst Case |
|-----------|-----------|--------------|------------|
| Add Fact | O(1) | O(1) | O(1) |
| Query Fact | O(1) | O(1) | O(1) |
| Detect Conflicts | O(1) cached | O(N) | O(N) |
| Parallel Retrieval | O(1) | O(1) | O(k) |

### Space Complexity

- **Graph State**: O(V + E)
- **Tier 1**: O(active_size)
- **Tier 2**: O(dormant_size)
- **Tier 3**: O(total_facts)

## Concurrency Model

### Async Execution

```python
# Semaphore-based concurrency control
class SpeculativeRetriever:
    def __init__(self, max_parallel_hops):
        self.semaphore = asyncio.Semaphore(max_parallel_hops)
    
    async def parallel_hop(self, queries):
        tasks = [self._limited_search(q) for q in queries]
        return await asyncio.gather(*tasks)
    
    async def _limited_search(self, query):
        async with self.semaphore:
            return await self._search(query)
```

## Data Persistence

### Graph Serialization

```python
# Save graph state
def save_state(path):
    state = {
        'nodes': serialize_nodes(self.nodes),
        'edges': serialize_edges(self.edges),
        'tier_mapping': self.tier_mapping
    }
    pickle.dump(state, open(path, 'wb'))
```

### Vector Database Integration

```python
# Sync to Qdrant
def sync_to_vector_db():
    tier3_facts = [n for n in nodes.values() if n.tier == 3]
    
    vector_db.upsert(
        collection_name="ahs_facts",
        points=[
            PointStruct(
                id=fact.id,
                vector=fact.vector,
                payload=fact.metadata
            )
            for fact in tier3_facts
        ]
    )
```

## Security Considerations

1. **Input Validation**: All facts sanitized before ingestion
2. **Access Control**: RBAC for multi-tenant deployments (roadmap)
3. **Encryption**: Tier 3 storage encrypted at rest
4. **Audit Logging**: All operations logged for compliance

## Extensibility Points

### Custom Resolvers

```python
agent.register_resolver("domain_expert", custom_function)
```

### Custom Embeddings

```python
agent.set_embedding_function(custom_embedding_fn)
```

### Custom Vector DB

```python
agent.set_vector_db(CustomVectorDBAdapter())
```

## Future Enhancements

- GPU-accelerated embeddings
- Distributed graph state
- Causal reasoning
- Temporal decay of facts

For implementation details, see [GitHub Repository](https://github.com/sachinecin/AHS_Agentic).
