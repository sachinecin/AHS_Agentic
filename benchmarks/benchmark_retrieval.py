"""
Retrieval Performance Benchmarks

Benchmark speculative parallel-hop retrieval performance.
"""

import asyncio
import time
import argparse
import json
from typing import List
from ahs_agentic import SpeculativeRetriever


async def benchmark_parallel_retrieval(
    num_queries: int = 100,
    max_parallel_hops: int = 5
) -> dict:
    """
    Benchmark parallel retrieval performance.
    
    Args:
        num_queries: Number of queries to execute
        max_parallel_hops: Maximum concurrent operations
    
    Returns:
        Dictionary with benchmark results
    """
    retriever = SpeculativeRetriever(max_parallel_hops=max_parallel_hops)
    queries = [f"query_{i}" for i in range(num_queries)]
    
    # Warmup
    await retriever.parallel_hop(queries[:10])
    
    # Benchmark
    latencies = []
    
    for i in range(0, num_queries, 10):
        batch = queries[i:i+10]
        
        start = time.time()
        await retriever.parallel_hop(batch)
        end = time.time()
        
        latency_ms = (end - start) * 1000
        latencies.append(latency_ms)
    
    # Calculate statistics
    latencies.sort()
    p50 = latencies[int(len(latencies) * 0.50)]
    p95 = latencies[int(len(latencies) * 0.95)]
    p99 = latencies[int(len(latencies) * 0.99)]
    avg = sum(latencies) / len(latencies)
    
    return {
        "num_queries": num_queries,
        "max_parallel_hops": max_parallel_hops,
        "latency_p50_ms": round(p50, 2),
        "latency_p95_ms": round(p95, 2),
        "latency_p99_ms": round(p99, 2),
        "latency_avg_ms": round(avg, 2),
        "throughput_qps": round(num_queries / (sum(latencies) / 1000), 2)
    }


async def benchmark_concurrency_levels():
    """Benchmark different concurrency levels."""
    print("🔍 Benchmarking Retrieval Performance\n")
    
    results = []
    
    for hops in [1, 2, 5, 10, 20]:
        print(f"Testing with max_parallel_hops={hops}...")
        result = await benchmark_parallel_retrieval(
            num_queries=100,
            max_parallel_hops=hops
        )
        results.append(result)
        
        print(f"  Latency p50: {result['latency_p50_ms']}ms")
        print(f"  Latency p95: {result['latency_p95_ms']}ms")
        print(f"  Throughput: {result['throughput_qps']} q/s\n")
    
    return results


def main():
    """Main benchmark runner."""
    parser = argparse.ArgumentParser(description="Benchmark retrieval performance")
    parser.add_argument("--output", type=str, help="Output JSON file")
    parser.add_argument("--quick", action="store_true", help="Quick benchmark")
    args = parser.parse_args()
    
    results = asyncio.run(benchmark_concurrency_levels())
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump({"retrieval_benchmarks": results}, f, indent=2)
        print(f"✅ Results saved to {args.output}")
    
    return results


if __name__ == "__main__":
    main()
