"""
Regulatory Compliance Example for AHS Agentic

Real-world use case: Financial services regulatory compliance reconciliation.

Scenario: A fintech company needs to ensure their payment processing SOPs
comply with new federal regulations while maintaining state-specific requirements.

This example demonstrates:
- Multi-document compliance checking
- Conflict detection across regulatory frameworks
- Automated compliance reporting
- Risk assessment and prioritization
"""

from ahs_agentic import HyperGraphAgent
import asyncio
from typing import Dict, List, Any
from datetime import datetime
from enum import Enum


class ComplianceLevel(Enum):
    """Compliance status levels."""
    COMPLIANT = "✅ Fully Compliant"
    MINOR_GAP = "⚠️  Minor Compliance Gap"
    MAJOR_GAP = "❌ Major Compliance Gap"
    CONFLICT = "🚨 Regulatory Conflict"


class ComplianceChecker:
    """
    Automated compliance checking system for financial services.
    """
    
    def __init__(self):
        """Initialize compliance checker with legal-grade sensitivity."""
        self.agent = HyperGraphAgent(
            memory_mode="latent-layering",
            retrieval_strategy="speculative-parallel",
            skeptic_threshold=0.88  # Legal/compliance sensitivity
        )
    
    async def check_compliance(
        self,
        sop: Dict[str, str],
        federal_regs: Dict[str, str],
        state_regs: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Check SOP compliance against federal and state regulations.
        
        Args:
            sop: Company standard operating procedures
            federal_regs: Federal regulations
            state_regs: State-specific regulations
            
        Returns:
            Comprehensive compliance report
        """
        
        print("\n🏛️  REGULATORY COMPLIANCE CHECK")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().isoformat()}")
        print(f"SOPs: {len(sop)} documents")
        print(f"Federal Regulations: {len(federal_regs)} documents")
        print(f"State Regulations: {len(state_regs)} documents")
        print("=" * 80)
        
        compliance_issues = []
        
        # Step 1: Check SOP vs Federal Regulations
        print("\n1️⃣  Checking SOPs against Federal Regulations...")
        for sop_name, sop_content in sop.items():
            for reg_name, reg_content in federal_regs.items():
                issue = await self._check_pair(
                    sop_name, sop_content,
                    reg_name, reg_content,
                    "Federal"
                )
                if issue:
                    compliance_issues.append(issue)
        
        # Step 2: Check SOP vs State Regulations
        print("\n2️⃣  Checking SOPs against State Regulations...")
        for sop_name, sop_content in sop.items():
            for reg_name, reg_content in state_regs.items():
                issue = await self._check_pair(
                    sop_name, sop_content,
                    reg_name, reg_content,
                    "State"
                )
                if issue:
                    compliance_issues.append(issue)
        
        # Step 3: Check for conflicts between Federal and State
        print("\n3️⃣  Checking for Federal-State conflicts...")
        for fed_name, fed_content in federal_regs.items():
            for state_name, state_content in state_regs.items():
                issue = await self._check_pair(
                    fed_name, fed_content,
                    state_name, state_content,
                    "Federal-State Conflict"
                )
                if issue:
                    compliance_issues.append(issue)
        
        # Step 4: Generate compliance report
        report = self._generate_compliance_report(
            compliance_issues,
            len(sop),
            len(federal_regs),
            len(state_regs)
        )
        
        return report
    
    async def _check_pair(
        self,
        doc1_name: str,
        doc1_content: str,
        doc2_name: str,
        doc2_content: str,
        check_type: str
    ) -> Dict[str, Any] | None:
        """Check a pair of documents for compliance issues."""
        
        result = await self.agent.resolve_conflict(
            legacy_sop=doc1_content,
            new_regulation=doc2_content,
            context=f"{check_type} Compliance: {doc1_name} vs {doc2_name}"
        )
        
        if result['status'] == 'conflict_detected':
            conflict_report = result.get('conflict_report', {})
            delta = conflict_report.get('delta_score', 0)
            
            # Classify severity
            if delta > 0.95:
                level = ComplianceLevel.CONFLICT
                severity = "CRITICAL"
            elif delta > 0.90:
                level = ComplianceLevel.MAJOR_GAP
                severity = "HIGH"
            else:
                level = ComplianceLevel.MINOR_GAP
                severity = "MEDIUM"
            
            print(f"   {level.value}: {doc1_name} ↔ {doc2_name} (Δ={delta:.3f})")
            
            return {
                "doc1": doc1_name,
                "doc2": doc2_name,
                "check_type": check_type,
                "level": level,
                "severity": severity,
                "delta": delta,
                "description": f"Conflict between {doc1_name} and {doc2_name}",
                "detected_at": datetime.now().isoformat()
            }
        
        return None
    
    def _generate_compliance_report(
        self,
        issues: List[Dict[str, Any]],
        sop_count: int,
        federal_count: int,
        state_count: int
    ) -> Dict[str, Any]:
        """Generate comprehensive compliance report."""
        
        # Categorize issues by severity
        critical = [i for i in issues if i['severity'] == 'CRITICAL']
        high = [i for i in issues if i['severity'] == 'HIGH']
        medium = [i for i in issues if i['severity'] == 'MEDIUM']
        
        # Calculate compliance score
        total_checks = sop_count * (federal_count + state_count)
        issues_count = len(issues)
        compliance_score = ((total_checks - issues_count) / total_checks * 100) if total_checks > 0 else 100
        
        # Determine overall status
        if critical:
            overall_status = "🚨 CRITICAL - Immediate Action Required"
        elif high:
            overall_status = "⚠️  HIGH RISK - Review Within 7 Days"
        elif medium:
            overall_status = "⚠️  MEDIUM RISK - Review Within 30 Days"
        else:
            overall_status = "✅ COMPLIANT - No Issues Found"
        
        metrics = self.agent.get_metrics()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": overall_status,
            "compliance_score": round(compliance_score, 1),
            "summary": {
                "total_checks": total_checks,
                "issues_found": issues_count,
                "critical_issues": len(critical),
                "high_risk_issues": len(high),
                "medium_risk_issues": len(medium)
            },
            "issues": issues,
            "performance": {
                "decision_velocity": f"{metrics['decision_velocity']:.2f}x",
                "analysis_quality": f"{(1 - metrics['reasoning_regret']) * 100:.1f}%"
            },
            "recommendations": self._generate_recommendations(critical, high, medium)
        }
        
        return report
    
    def _generate_recommendations(
        self,
        critical: list,
        high: list,
        medium: list
    ) -> List[str]:
        """Generate actionable recommendations."""
        
        recommendations = []
        
        if critical:
            recommendations.append(
                f"🚨 URGENT: Address {len(critical)} critical compliance issue(s) immediately"
            )
            recommendations.append(
                "   → Halt affected operations until issues are resolved"
            )
            recommendations.append(
                "   → Consult with legal counsel"
            )
        
        if high:
            recommendations.append(
                f"⚠️  HIGH PRIORITY: Review {len(high)} high-risk issue(s) within 7 days"
            )
            recommendations.append(
                "   → Update SOPs to align with regulations"
            )
            recommendations.append(
                "   → Document remediation steps"
            )
        
        if medium:
            recommendations.append(
                f"📋 MEDIUM PRIORITY: Address {len(medium)} medium-risk issue(s) within 30 days"
            )
            recommendations.append(
                "   → Plan SOP updates for next review cycle"
            )
        
        if not (critical or high or medium):
            recommendations.append(
                "✅ No compliance issues found - maintain current practices"
            )
            recommendations.append(
                "📅 Schedule next review in 90 days"
            )
        
        return recommendations


async def main():
    """Main function demonstrating regulatory compliance checking."""
    
    print("🏛️  AHS Agentic - Regulatory Compliance Example")
    print("Scenario: FinTech Payment Processing Compliance Check")
    print("=" * 80)
    
    # Sample documents (simplified for demonstration)
    company_sops = {
        "Payment_Processing_SOP_v2024": """
        Payment Processing Standard Operating Procedure:
        - Manual approval required for all transactions over $10,000
        - Verification by two authorized personnel
        - Transaction logs retained for 5 years
        - Same-day processing for domestic transfers
        - International transfers processed within 3 business days
        """,
        
        "KYC_AML_SOP_v2024": """
        Know Your Customer (KYC) and Anti-Money Laundering (AML):
        - Customer identity verification required for accounts over $5,000
        - Enhanced due diligence for high-risk customers
        - Suspicious activity reports filed within 30 days
        - Annual customer risk assessments
        """
    }
    
    federal_regulations = {
        "Federal_Reg_2026_Payment": """
        Federal Payment Processing Regulation (2026):
        - Automated approval allowed for transactions up to $50,000 with AI oversight
        - Single authorized personnel sufficient with AI validation
        - Transaction logs must be retained for 7 years
        - Real-time processing required for domestic transfers
        - International transfers must be processed within 1 business day
        """,
        
        "Federal_Reg_2026_AML": """
        Updated Anti-Money Laundering Requirements (2026):
        - KYC verification required for all accounts, regardless of amount
        - Real-time monitoring of suspicious activities
        - Suspicious activity reports must be filed within 24 hours
        - Quarterly customer risk reassessments required
        """
    }
    
    state_regulations = {
        "CA_State_Reg_Payment": """
        California Payment Processing Requirements:
        - All transactions require human oversight (AI approval not sufficient)
        - Transaction logs retained for 10 years minimum
        - Consumer protection disclosures required for all transactions
        """
    }
    
    # Initialize compliance checker
    checker = ComplianceChecker()
    
    # Run compliance check
    report = await checker.check_compliance(
        sop=company_sops,
        federal_regs=federal_regulations,
        state_regs=state_regulations
    )
    
    # Display report
    print("\n" + "=" * 80)
    print("📊 COMPLIANCE REPORT")
    print("=" * 80)
    
    print(f"\n⏰ Generated: {report['timestamp']}")
    print(f"📈 Compliance Score: {report['compliance_score']}%")
    print(f"🎯 Status: {report['overall_status']}")
    
    print("\n📊 Summary:")
    print(f"   Total Checks: {report['summary']['total_checks']}")
    print(f"   Issues Found: {report['summary']['issues_found']}")
    print(f"   ├─ Critical: {report['summary']['critical_issues']}")
    print(f"   ├─ High Risk: {report['summary']['high_risk_issues']}")
    print(f"   └─ Medium Risk: {report['summary']['medium_risk_issues']}")
    
    if report['issues']:
        print("\n⚠️  Compliance Issues:")
        for i, issue in enumerate(report['issues'], 1):
            print(f"\n   Issue #{i}:")
            print(f"      Type: {issue['check_type']}")
            print(f"      Severity: {issue['severity']}")
            print(f"      Documents: {issue['doc1']} ↔ {issue['doc2']}")
            print(f"      Delta Score: {issue['delta']:.3f}")
    
    print("\n💡 Recommendations:")
    for rec in report['recommendations']:
        print(f"   {rec}")
    
    print("\n⚡ Performance:")
    print(f"   Analysis Speed: {report['performance']['decision_velocity']}")
    print(f"   Analysis Quality: {report['performance']['analysis_quality']}")
    
    print("\n✨ Compliance check completed!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
    
    print("\n💡 Integration Ideas:")
    print("   - Schedule automated daily compliance checks")
    print("   - Integrate with Slack/Teams for instant alerts")
    print("   - Connect to document management system (SharePoint, Confluence)")
    print("   - Export reports to compliance management platform")
    print("   - Set up CI/CD pipeline to block deployments on critical issues")
