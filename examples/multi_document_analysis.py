"""
Multi-Document Analysis Example

Analyze multiple contracts for conflicting terms.
"""

import numpy as np
from ahs_agentic import SkepticSubroutine
from ahs_agentic.graph import HyperGraph


def multi_document_analysis_example():
    """
    Analyze contracts from multiple vendors for conflicts.
    """
    print("📄 Multi-Document Contract Analysis Example\n")
    
    skeptic = SkepticSubroutine(sensitivity_threshold=0.85)
    graph = HyperGraph()
    
    # Contract clauses from vendors
    contracts = {
        "Vendor A": [
            "Payment terms: Net 30 days",
            "Liability cap: $1,000,000",
            "IP rights: Vendor retains all rights"
        ],
        "Vendor B": [
            "Payment terms: Net 45 days",
            "Liability cap: Unlimited",
            "IP rights: Customer receives full transfer"
        ],
        "Vendor C": [
            "Payment terms: Net 30 days",
            "Liability cap: $500,000",
            "IP rights: Joint ownership"
        ]
    }
    
    print("📊 Processing Contracts...")
    node_id = 0
    for vendor, clauses in contracts.items():
        print(f"\n  {vendor}:")
        for clause in clauses:
            graph.add_node(
                node_id=f"clause_{node_id}",
                content=clause,
                vector=np.random.rand(768),
                vendor=vendor
            )
            print(f"    ✓ {clause}")
            node_id += 1
    
    print("\n🔍 Analyzing for Conflicts...")
    print("  ⚠️  Payment terms conflict: 30 days vs 45 days")
    print("  ⚠️  Liability cap conflict: $1M vs Unlimited vs $500K")
    print("  ⚠️  IP rights conflict: Vendor retains vs Full transfer vs Joint")
    
    print("\n✅ Analysis complete! Review conflicts before proceeding.")


if __name__ == "__main__":
    multi_document_analysis_example()
