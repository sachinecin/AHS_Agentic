"""
Forensic Document Reconciliation Example

This example demonstrates how to use AHS to reconcile conflicting
medical records from multiple hospitals.
"""

import asyncio
import numpy as np
from ahs_agentic import SkepticSubroutine, SpeculativeRetriever
from ahs_agentic.graph import HyperGraph
from ahs_agentic.memory import LatentMemoryManager, FactNode


async def forensic_reconciliation_example():
    """
    Reconcile patient medical records from multiple sources.
    """
    print("🏥 Forensic Medical Record Reconciliation Example\n")
    
    # Initialize components
    skeptic = SkepticSubroutine(sensitivity_threshold=0.85)
    retriever = SpeculativeRetriever(max_parallel_hops=5)
    graph = HyperGraph()
    memory = LatentMemoryManager(tier1_size=256, tier2_size=2048)
    
    # Simulate medical facts from different hospitals
    hospital_a_records = [
        {
            "content": "Patient John Doe, Age 45, Blood Type O+",
            "source": "Hospital A - Admissions",
            "vector": np.random.rand(768),
            "salience": 0.95
        },
        {
            "content": "Allergies: Penicillin, Sulfa drugs",
            "source": "Hospital A - Allergy Record",
            "vector": np.random.rand(768),
            "salience": 0.90
        },
        {
            "content": "Current Medications: Metformin 500mg BID",
            "source": "Hospital A - Pharmacy",
            "vector": np.random.rand(768),
            "salience": 0.88
        },
    ]
    
    hospital_b_records = [
        {
            "content": "Patient John Doe, Age 45, Blood Type O+",
            "source": "Hospital B - ER",
            "vector": np.random.rand(768),
            "salience": 0.95
        },
        {
            "content": "Allergies: Penicillin only",
            "source": "Hospital B - Allergy Record",
            "vector": np.random.rand(768),
            "salience": 0.85
        },
        {
            "content": "Current Medications: Amoxicillin 250mg TID, Metformin 500mg BID",
            "source": "Hospital B - Pharmacy",
            "vector": np.random.rand(768),
            "salience": 0.92
        },
    ]
    
    print("📊 Processing Hospital A Records...")
    for i, record in enumerate(hospital_a_records):
        fact = FactNode(
            id=f"hospital_a_{i}",
            content=record["content"],
            vector=record["vector"],
            salience_score=record["salience"],
            tier=1,
            source_metadata={"source": record["source"]}
        )
        memory.add_fact(fact)
        graph.add_node(
            node_id=fact.id,
            content=fact.content,
            vector=fact.vector,
            source=record["source"]
        )
        print(f"  ✓ {record['content'][:50]}...")
    
    print("\n📊 Processing Hospital B Records...")
    for i, record in enumerate(hospital_b_records):
        fact = FactNode(
            id=f"hospital_b_{i}",
            content=record["content"],
            vector=record["vector"],
            salience_score=record["salience"],
            tier=1,
            source_metadata={"source": record["source"]}
        )
        memory.add_fact(fact)
        graph.add_node(
            node_id=fact.id,
            content=fact.content,
            vector=fact.vector,
            source=record["source"]
        )
        print(f"  ✓ {record['content'][:50]}...")
    
    # Detect conflicts using Skeptic
    print("\n🔍 Running Skeptic Conflict Detection...")
    
    # Simulate conflict between allergy records
    allergy_a = hospital_a_records[1]["vector"]
    allergy_b = hospital_b_records[1]["vector"]
    allergy_delta = skeptic.compute_conflict_delta(allergy_a, allergy_b)
    
    if skeptic.should_trigger(allergy_delta):
        report = skeptic.generate_conflict_report(
            existing_premise=hospital_a_records[1]["content"],
            new_evidence=hospital_b_records[1]["content"],
            delta=allergy_delta
        )
        print(f"  ⚠️  CONFLICT DETECTED!")
        print(f"     Delta Score: {report['delta_score']:.2f}")
        print(f"     Existing: {report['existing_premise']}")
        print(f"     New: {report['new_evidence']}")
        print(f"     Resolution: {report['resolution_strategy']}")
    
    # Simulate conflict between medications (Amoxicillin is penicillin-derived!)
    med_a = hospital_a_records[2]["vector"]
    med_b = hospital_b_records[2]["vector"]
    med_delta = skeptic.compute_conflict_delta(med_a, med_b)
    
    if skeptic.should_trigger(med_delta):
        report = skeptic.generate_conflict_report(
            existing_premise=hospital_a_records[2]["content"],
            new_evidence=hospital_b_records[2]["content"],
            delta=med_delta
        )
        print(f"\n  ⚠️  CRITICAL CONFLICT DETECTED!")
        print(f"     Delta Score: {report['delta_score']:.2f}")
        print(f"     Existing: {report['existing_premise']}")
        print(f"     New: {report['new_evidence']}")
        print(f"     ⚠️  WARNING: Amoxicillin is a penicillin derivative!")
        print(f"     ⚠️  Patient is allergic to penicillin!")
        print(f"     Resolution: {report['resolution_strategy']}")
    
    # Show memory tier statistics
    print("\n💾 Memory Tier Statistics:")
    metrics = memory.get_metrics()
    print(f"  Tier 1 (Active): {metrics['tier1_count']} facts")
    print(f"  Tier 2 (Dormant): {metrics['tier2_count']} facts")
    print(f"  Tier 3 (Deep): {metrics['tier3_count']} facts")
    
    # Show graph statistics
    print("\n📊 Graph Statistics:")
    graph_metrics = graph.get_metrics()
    print(f"  Total Nodes: {graph_metrics['num_nodes']}")
    print(f"  Total Edges: {graph_metrics['num_edges']}")
    print(f"  Detected Conflicts: {graph_metrics['num_conflicts']}")
    
    print("\n✅ Forensic reconciliation complete!")
    print("   Conflicts have been flagged for physician review.")


if __name__ == "__main__":
    asyncio.run(forensic_reconciliation_example())
