"""
Memory Performance Benchmarks

Benchmark multi-tier memory management performance.
"""

import time
import argparse
import json
import numpy as np
from ahs_agentic.memory import LatentMemoryManager, FactNode


def benchmark_tier_operations(num_facts: int = 1000) -> dict:
    """
    Benchmark memory tier operations.
    
    Args:
        num_facts: Number of facts to test with
    
    Returns:
        Dictionary with benchmark results
    """
    memory = LatentMemoryManager(tier1_size=256, tier2_size=2048)
    
    # Benchmark fact addition
    add_times = []
    for i in range(num_facts):
        fact = FactNode(
            id=f"fact_{i}",
            content=f"Test fact {i}",
            vector=np.random.rand(768),
            salience_score=0.5 + (i % 50) / 100,
            tier=1,
            source_metadata={}
        )
        
        start = time.time()
        memory.add_fact(fact)
        end = time.time()
        
        add_times.append((end - start) * 1000000)  # microseconds
    
    # Benchmark promotions
    promotion_times = []
    for i in range(min(50, num_facts)):
        fact_id = f"fact_{i}"
        if fact_id in memory.tier2:
            start = time.time()
            memory.promote_to_tier1(fact_id)
            end = time.time()
            promotion_times.append((end - start) * 1000000)
    
    # Calculate statistics
    add_avg = sum(add_times) / len(add_times)
    add_p95 = sorted(add_times)[int(len(add_times) * 0.95)]
    
    promotion_avg = sum(promotion_times) / len(promotion_times) if promotion_times else 0
    
    metrics = memory.get_metrics()
    
    return {
        "num_facts": num_facts,
        "add_fact_avg_us": round(add_avg, 2),
        "add_fact_p95_us": round(add_p95, 2),
        "promote_avg_us": round(promotion_avg, 2),
        "tier1_count": metrics["tier1_count"],
        "tier2_count": metrics["tier2_count"],
        "tier3_count": metrics["tier3_count"],
        "tier1_utilization": round(metrics["tier1_utilization"], 2),
    }


def main():
    """Main benchmark runner."""
    parser = argparse.ArgumentParser(description="Benchmark memory performance")
    parser.add_argument("--output", type=str, help="Output JSON file")
    parser.add_argument("--quick", action="store_true", help="Quick benchmark")
    args = parser.parse_args()
    
    print("🔍 Benchmarking Memory Performance\n")
    
    results = []
    
    for size in [100, 500, 1000]:
        print(f"Testing with {size} facts...")
        result = benchmark_tier_operations(num_facts=size)
        results.append(result)
        
        print(f"  Add Fact (avg): {result['add_fact_avg_us']:.2f}µs")
        print(f"  Add Fact (p95): {result['add_fact_p95_us']:.2f}µs")
        print(f"  Promote (avg): {result['promote_avg_us']:.2f}µs")
        print(f"  Tier 1: {result['tier1_count']} facts\n")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump({"memory_benchmarks": results}, f, indent=2)
        print(f"✅ Results saved to {args.output}")
    
    return results


if __name__ == "__main__":
    main()
