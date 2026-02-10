# Performance Optimization Guide

Maximize throughput and minimize costs with AHS Agentic.

## Benchmarking Methodology

### Running Benchmarks

```bash
# Run all benchmarks
python benchmarks/benchmark_retrieval.py
python benchmarks/benchmark_memory.py

# Compare against baseline
python benchmarks/compare_baseline.py
```

### Performance Metrics

Key metrics to track:
- **Latency (p50, p95, p99)**: Query response time
- **Throughput**: Queries per second
- **Token Cost**: Cost per query
- **Memory Usage**: RAM consumption

## Latency Optimization

### 1. Parallel Retrieval

```python
# Bad: Sequential retrieval
for query in queries:
    result = await retriever.search(query)

# Good: Parallel retrieval
retriever = SpeculativeRetriever(max_parallel_hops=10)
results = await retriever.parallel_hop(queries)
```

**Impact**: 70% latency reduction

### 2. Tier Management

```python
# Optimize tier sizes for your use case
agent = HyperGraphAgent(
    tier1_size=128,    # Smaller active context
    tier2_size=1024,   # Larger dormant cache
)
```

### 3. Batch Processing

```python
# Process queries in batches
async def process_batch(queries, batch_size=20):
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i+batch_size]
        results = await retriever.parallel_hop(batch)
        yield results
```

## Memory Management

### Tier Optimization

```python
# Monitor tier usage
metrics = agent.get_tier_metrics()
print(f"Tier 1 Usage: {metrics['tier1_usage']}/{metrics['tier1_capacity']}")
print(f"Tier 2 Usage: {metrics['tier2_usage']}/{metrics['tier2_capacity']}")

# Adjust tier sizes dynamically
if metrics['tier1_usage'] > 0.9 * metrics['tier1_capacity']:
    agent.increase_tier1_size(256)
```

### Memory Cleanup

```python
# Periodic cleanup of deep storage
agent.cleanup_tier3(
    older_than_days=30,
    min_salience_score=0.3
)
```

## Token Cost Reduction

### Smart Tiering

```python
# Facts automatically demote to lower tiers
# Only Tier 1 incurs token costs

# Force demotion of rarely accessed facts
agent.demote_inactive_facts(inactive_threshold_minutes=10)
```

### Conflict Detection Optimization

```python
# Higher threshold = fewer Skeptic triggers = lower costs
skeptic = SkepticSubroutine(sensitivity_threshold=0.90)

# But watch false negative rate!
```

## Scaling Considerations

### Horizontal Scaling

```python
# Use multiple agent instances
agents = [HyperGraphAgent() for _ in range(10)]

# Load balance queries
async def load_balanced_query(query):
    agent = agents[hash(query) % len(agents)]
    return await agent.query(query)
```

### Database Optimization

```python
# Use connection pooling for vector DB
from qdrant_client import QdrantClient

client = QdrantClient(
    url="http://localhost:6333",
    timeout=10,
    pool_size=20  # Connection pool
)
```

## Monitoring and Profiling

### Built-in Metrics

```python
metrics = agent.get_metrics()
print(f"Average Latency: {metrics['avg_latency_ms']}ms")
print(f"P95 Latency: {metrics['p95_latency_ms']}ms")
print(f"Total Token Cost: ${metrics['total_token_cost']:.2f}")
```

### Custom Profiling

```python
import time

def profile_query(agent, query):
    start = time.time()
    result = agent.query(query)
    latency = (time.time() - start) * 1000
    
    print(f"Query: {query[:50]}...")
    print(f"Latency: {latency:.2f}ms")
    print(f"Token Cost: ${result['token_cost']:.4f}")
    
    return result
```

## Best Practices

1. **Use Parallel Retrieval** for multiple queries
2. **Optimize Tier Sizes** for your workload
3. **Monitor Token Costs** regularly
4. **Profile Critical Paths** to identify bottlenecks
5. **Use Batch Processing** for high-volume scenarios
6. **Scale Horizontally** when needed

For architecture details, see [Architecture Deep Dive](architecture-deep-dive.md).
