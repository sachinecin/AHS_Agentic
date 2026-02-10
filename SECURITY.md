# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

The AHS Agentic team takes security seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by email to:

📧 **security@ahs-framework.ai**

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

### What to Include

Please include the following information in your report:

1. **Description**: A clear description of the vulnerability
2. **Impact**: What an attacker could do with this vulnerability
3. **Affected Components**: Which parts of AHS are affected
4. **Reproduction Steps**: Step-by-step instructions to reproduce the issue
5. **Proof of Concept**: If applicable, provide code or commands
6. **Suggested Fix**: If you have ideas on how to fix it
7. **Your Contact Info**: How we can reach you for follow-up

### Example Report

```
Subject: [SECURITY] Potential privilege escalation in graph state access

Description:
The graph state access control does not properly validate user permissions
when accessing dormant facts in Tier 2 memory, potentially allowing
unauthorized access to sensitive cached data.

Impact:
An attacker with basic API access could potentially retrieve dormant facts
from other users' graph states, leading to information disclosure.

Affected Components:
- ahs/memory/latent_layer.py (lines 145-167)
- ahs/core/synapse.py (lines 89-95)

Reproduction Steps:
1. Create two separate graph states for different users
2. Store sensitive data in User A's Tier 2 dormant cache
3. Use User B's API token to call reactivate_dormant_facts()
4. User B can access User A's cached data

Proof of Concept:
[Attach code or detailed steps]

Suggested Fix:
Add user_id validation in the reactivate_dormant_facts() method
before allowing access to Tier 2 cache.

Contact:
researcher@security-firm.com
```

## Security Update Process

1. **Acknowledgment**: We'll acknowledge receipt within 48 hours
2. **Assessment**: We'll assess the vulnerability and determine severity (Critical, High, Medium, Low)
3. **Fix Development**: We'll work on a fix (timeline depends on severity)
4. **Coordinated Disclosure**: We'll coordinate disclosure with you
5. **Release**: We'll release a security patch
6. **Advisory**: We'll publish a security advisory

### Timeline Targets

| Severity | Initial Response | Fix Target | Disclosure |
|----------|-----------------|------------|------------|
| Critical | 24 hours | 7 days | 14 days after fix |
| High | 48 hours | 14 days | 30 days after fix |
| Medium | 72 hours | 30 days | 60 days after fix |
| Low | 1 week | 90 days | 90 days after fix |

## Known Security Considerations for AI Agents

### 1. Prompt Injection Attacks

**Risk**: Malicious users could craft queries that manipulate the LLM to ignore safety guardrails.

**Mitigation**:
- Input sanitization in query decomposition
- Skeptic Subroutine validates unexpected behavioral changes
- Audit logging of all queries

### 2. Data Poisoning

**Risk**: Adversarial facts could be injected into the graph state to corrupt reasoning.

**Mitigation**:
- Source provenance tracking for all facts
- Conflict detection via Skeptic Subroutine
- Fact verification against trusted sources (roadmap)

### 3. Information Disclosure

**Risk**: Graph state might inadvertently leak sensitive information across security boundaries.

**Mitigation**:
- Multi-tenancy with strict isolation
- RBAC for fact visibility (roadmap)
- Encryption at rest for Tier 3 storage

### 4. Denial of Service

**Risk**: Resource exhaustion via excessive parallel hops or large graph states.

**Mitigation**:
- Semaphore-based concurrency limits
- Rate limiting per user/tenant
- Graph size quotas

### 5. Model Extraction

**Risk**: Adversary could query the system repeatedly to extract model weights or training data.

**Mitigation**:
- Rate limiting on API endpoints
- Query pattern anomaly detection
- Differential privacy techniques (roadmap)

### 6. Supply Chain Security

**Risk**: Vulnerabilities in dependencies (networkx, openai, qdrant-client, etc.)

**Mitigation**:
- Regular dependency audits
- Automated vulnerability scanning in CI/CD
- Pin dependencies to known-safe versions

## Security Best Practices for Users

### When Deploying AHS

1. **Network Security**
   - Deploy behind a firewall
   - Use HTTPS/TLS for all API communication
   - Implement IP whitelisting if possible

2. **Authentication & Authorization**
   - Use strong authentication (OAuth 2.0, SAML)
   - Implement API key rotation
   - Use RBAC for multi-user deployments

3. **Data Security**
   - Encrypt sensitive data at rest
   - Use encrypted vector databases
   - Implement data retention policies

4. **Monitoring & Logging**
   - Enable comprehensive audit logging
   - Monitor for anomalous query patterns
   - Set up alerts for security events

5. **Compliance**
   - Ensure GDPR compliance for EU data
   - Implement HIPAA safeguards for healthcare
   - Follow industry-specific regulations

### When Handling Sensitive Data

1. **Data Minimization**: Only store necessary facts in graph state
2. **Anonymization**: Remove PII before ingestion when possible
3. **Access Controls**: Limit who can query sensitive graph states
4. **Audit Trails**: Log all access to sensitive facts
5. **Data Lifecycle**: Implement automatic expiration for sensitive facts

## Vulnerability Disclosure Policy

We follow responsible disclosure principles:

1. **Private Disclosure**: Report vulnerabilities privately first
2. **Coordinated Timeline**: Work with us to coordinate public disclosure
3. **Credit**: We'll credit you in security advisories (if desired)
4. **No Legal Action**: We won't pursue legal action against security researchers who follow this policy

## Security Hall of Fame

We recognize security researchers who have responsibly disclosed vulnerabilities:

- *[Researcher Name]* - [Vulnerability Type] - [Month/Year]
- (To be populated as researchers contribute)

## Bug Bounty Program

We currently do not have a formal bug bounty program. However, we greatly appreciate security research and will:

- Acknowledge your contribution publicly (if desired)
- Provide swag and recognition
- Consider compensation for critical findings

We plan to launch a formal bug bounty program in Q3 2026.

## Contact

- **Security Issues**: security@ahs-framework.ai
- **General Questions**: hello@ahs-framework.ai
- **GPG Key**: Available at https://ahs-framework.ai/security/gpg-key.asc

## Additional Resources

- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [EU AI Act Compliance](https://artificialintelligenceact.eu/)

---

**Last Updated**: 2026-02-10  
**Version**: 1.0.0  

Thank you for helping keep AHS Agentic and its users safe! 🔒
