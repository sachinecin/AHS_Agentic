"""
Forensic Reconciliation Example for AHS Agentic

This advanced example demonstrates conflict resolution with full forensic
traceability for audit and compliance requirements.

Use Case: Reconciling multiple policy versions with complete audit trail.
"""

from ahs_agentic import HyperGraphAgent, SkepticSubroutine
import asyncio
import json
from datetime import datetime
from typing import Dict, Any


class ForensicReconciliationEngine:
    """
    Advanced reconciliation engine with forensic tracing capabilities.
    """
    
    def __init__(self):
        """Initialize the reconciliation engine with high-sensitivity detection."""
        self.agent = HyperGraphAgent(
            memory_mode="latent-layering",
            retrieval_strategy="speculative-parallel",
            skeptic_threshold=0.88  # Higher sensitivity for compliance work
        )
        self.audit_log = []
    
    async def reconcile_with_audit_trail(
        self,
        documents: Dict[str, str],
        context: str
    ) -> Dict[str, Any]:
        """
        Reconcile multiple documents and generate complete audit trail.
        
        Args:
            documents: Dictionary of document names to content
            context: Business context for reconciliation
            
        Returns:
            Complete reconciliation report with forensic trace
        """
        
        print(f"\n🔍 Starting Forensic Reconciliation: {context}")
        print("=" * 80)
        
        # Step 1: Log the reconciliation request
        request_id = f"REC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        self.log_event("RECONCILIATION_STARTED", {
            "request_id": request_id,
            "context": context,
            "document_count": len(documents),
            "timestamp": datetime.now().isoformat()
        })
        
        # Step 2: Compare documents pairwise
        conflicts = []
        doc_names = list(documents.keys())
        
        for i in range(len(doc_names) - 1):
            doc1_name = doc_names[i]
            doc2_name = doc_names[i + 1]
            
            print(f"\n📄 Comparing: {doc1_name} ↔ {doc2_name}")
            
            result = await self.agent.resolve_conflict(
                legacy_sop=documents[doc1_name],
                new_regulation=documents[doc2_name],
                context=f"{context}: {doc1_name} vs {doc2_name}"
            )
            
            if result['status'] == 'conflict_detected':
                conflict_detail = {
                    "doc1": doc1_name,
                    "doc2": doc2_name,
                    "delta": result.get('conflict_report', {}).get('delta_score', 0),
                    "velocity_gain": result['velocity_gain'],
                    "timestamp": datetime.now().isoformat()
                }
                conflicts.append(conflict_detail)
                print(f"   ⚠️  Conflict detected! Delta: {conflict_detail['delta']:.3f}")
                
                self.log_event("CONFLICT_DETECTED", conflict_detail)
            else:
                print(f"   ✅ No conflicts - documents aligned")
        
        # Step 3: Generate comprehensive report
        report = self.generate_forensic_report(
            request_id=request_id,
            context=context,
            documents=documents,
            conflicts=conflicts
        )
        
        self.log_event("RECONCILIATION_COMPLETED", {
            "request_id": request_id,
            "conflicts_found": len(conflicts),
            "timestamp": datetime.now().isoformat()
        })
        
        return report
    
    def log_event(self, event_type: str, data: Dict[str, Any]):
        """Log an event to the audit trail."""
        self.audit_log.append({
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_forensic_report(
        self,
        request_id: str,
        context: str,
        documents: Dict[str, str],
        conflicts: list
    ) -> Dict[str, Any]:
        """Generate a comprehensive forensic report."""
        
        metrics = self.agent.get_metrics()
        
        report = {
            "request_id": request_id,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "documents_analyzed": len(documents),
                "conflicts_detected": len(conflicts),
                "status": "CONFLICTS_FOUND" if conflicts else "ALL_ALIGNED",
                "confidence": "HIGH" if metrics['reasoning_regret'] < 0.05 else "MEDIUM"
            },
            "conflicts": conflicts,
            "performance_metrics": {
                "decision_velocity": f"{metrics['decision_velocity']:.2f}x",
                "reasoning_quality": f"{(1 - metrics['reasoning_regret']) * 100:.1f}%",
                "token_efficiency": f"{metrics['token_efficiency']:.2f}"
            },
            "audit_trail": self.audit_log,
            "recommendations": self.generate_recommendations(conflicts)
        }
        
        return report
    
    def generate_recommendations(self, conflicts: list) -> list:
        """Generate actionable recommendations based on conflicts."""
        if not conflicts:
            return ["✅ All documents are aligned - no action required"]
        
        recommendations = [
            "⚠️  Conflicts detected - manual review required",
            f"📊 Review {len(conflicts)} conflict(s) with legal/compliance team",
            "📝 Update conflicting documents to align with latest requirements",
            "🔄 Re-run reconciliation after updates to verify resolution"
        ]
        
        return recommendations
    
    def export_report(self, report: Dict[str, Any], filename: str):
        """Export report to JSON file."""
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n💾 Report exported to: {filename}")


async def main():
    """Main function demonstrating forensic reconciliation."""
    
    print("🧠 AHS Agentic - Forensic Reconciliation Example")
    print("=" * 80)
    
    # Example: Reconciling HR policies across multiple versions
    documents = {
        "HR_Policy_2024_v1": """
        Vacation Policy:
        - Employees receive 15 vacation days per year
        - Must request vacation 30 days in advance
        - Maximum 10 consecutive days off
        - Unused days do not roll over
        """,
        
        "HR_Policy_2024_v2": """
        Vacation Policy (Updated):
        - Employees receive 20 vacation days per year
        - Must request vacation 14 days in advance
        - Maximum 15 consecutive days off
        - Up to 5 unused days roll over to next year
        """,
        
        "HR_Policy_2026": """
        Vacation Policy (Latest):
        - Employees receive 20 vacation days per year
        - Must request vacation 7 days in advance for planned leave
        - No maximum consecutive days limit
        - Unlimited rollover of unused days
        - Flexible vacation scheduling encouraged
        """
    }
    
    # Initialize reconciliation engine
    engine = ForensicReconciliationEngine()
    
    # Perform reconciliation with full audit trail
    report = await engine.reconcile_with_audit_trail(
        documents=documents,
        context="HR Vacation Policy Evolution 2024-2026"
    )
    
    # Display report
    print("\n" + "=" * 80)
    print("📊 FORENSIC RECONCILIATION REPORT")
    print("=" * 80)
    
    print(f"\n🆔 Request ID: {report['request_id']}")
    print(f"📅 Timestamp: {report['timestamp']}")
    print(f"📝 Context: {report['context']}")
    
    print("\n📈 Summary:")
    print(f"   Documents Analyzed: {report['summary']['documents_analyzed']}")
    print(f"   Conflicts Detected: {report['summary']['conflicts_detected']}")
    print(f"   Status: {report['summary']['status']}")
    print(f"   Confidence: {report['summary']['confidence']}")
    
    print("\n⚡ Performance Metrics:")
    for key, value in report['performance_metrics'].items():
        print(f"   {key.replace('_', ' ').title()}: {value}")
    
    if report['conflicts']:
        print("\n⚠️  Conflicts Detected:")
        for i, conflict in enumerate(report['conflicts'], 1):
            print(f"\n   Conflict #{i}:")
            print(f"      Between: {conflict['doc1']} ↔ {conflict['doc2']}")
            print(f"      Delta Score: {conflict['delta']:.3f}")
            print(f"      Detected At: {conflict['timestamp']}")
    
    print("\n💡 Recommendations:")
    for rec in report['recommendations']:
        print(f"   {rec}")
    
    print("\n🔍 Audit Trail:")
    for event in report['audit_trail']:
        print(f"   [{event['timestamp']}] {event['event_type']}")
    
    # Export report
    engine.export_report(report, "reconciliation_report.json")
    
    print("\n✨ Forensic reconciliation completed!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
    
    print("\n💡 Next Steps:")
    print("   - Review reconciliation_report.json for full details")
    print("   - Use this pattern for compliance audits")
    print("   - Integrate with your CI/CD for automated policy checks")
