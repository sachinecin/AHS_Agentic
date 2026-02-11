# Security Policy

## Supported Versions

The following versions of AHS Agentic are currently supported with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

We recommend always using the latest stable release to ensure you have the most recent security patches and features.

---

## Reporting a Vulnerability

**We take security seriously.** If you discover a security vulnerability in AHS Agentic, please help us by responsibly disclosing it.

### 🔒 Private Disclosure Process

**DO NOT** create a public GitHub issue for security vulnerabilities. Instead:

1. **Email**: Send details to the project maintainers (create a security advisory on GitHub)
   - Use GitHub's Private Security Advisory feature: [github.com/sachinecin/AHS_Agentic/security/advisories/new](https://github.com/sachinecin/AHS_Agentic/security/advisories/new)
   
2. **Include**:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact assessment
   - Suggested fix (if available)
   - Your contact information for follow-up

3. **Response Timeline**:
   - **24 hours**: Initial acknowledgment of your report
   - **7 days**: Preliminary assessment and severity rating
   - **30 days**: Target for patch development and release
   - **90 days**: Public disclosure (coordinated with reporter)

### Vulnerability Severity Levels

We use the following severity classification:

| Severity | Description | Response Time |
|----------|-------------|---------------|
| **Critical** | Remote code execution, data breach, authentication bypass | 24 hours |
| **High** | Privilege escalation, significant data exposure | 7 days |
| **Medium** | Limited data exposure, denial of service | 14 days |
| **Low** | Information disclosure, minor security issues | 30 days |

---

## Security Best Practices for Users

### 1. API Key Management

**NEVER** hardcode API keys in your source code:

```python
# ❌ BAD - Exposes API keys
agent = HyperGraphAgent(
    llm_config={"api_key": "sk-abc123..."}
)

# ✅ GOOD - Use environment variables
import os
agent = HyperGraphAgent(
    llm_config={"api_key": os.getenv("OPENAI_API_KEY")}
)
```

### 2. Input Validation

Always validate user inputs before processing:

```python
# ✅ GOOD - Validate inputs
def process_query(user_input: str) -> dict:
    if not user_input or len(user_input) > 10000:
        raise ValueError("Invalid input length")
    
    # Sanitize potentially malicious inputs
    sanitized = user_input.strip()
    
    return agent.process(sanitized)
```

### 3. Access Control

Implement proper access controls for sensitive operations:

```python
# ✅ GOOD - Check permissions
def resolve_conflict(user_id: str, legacy_sop: str, new_regulation: str):
    if not user_has_permission(user_id, "conflict_resolution"):
        raise PermissionError("Unauthorized access")
    
    return agent.resolve_conflict(legacy_sop, new_regulation)
```

### 4. Network Security

Use secure connections for vector database and cache:

```python
# ✅ GOOD - Use TLS for remote connections
agent = HyperGraphAgent(
    vector_db_config={
        "provider": "qdrant",
        "host": "qdrant.example.com",
        "port": 6333,
        "https": True,  # Enable TLS
        "api_key": os.getenv("QDRANT_API_KEY")
    },
    tier2_cache_config={
        "provider": "redis",
        "host": "redis.example.com",
        "port": 6379,
        "ssl": True,  # Enable TLS
        "password": os.getenv("REDIS_PASSWORD")
    }
)
```

### 5. Data Privacy

Be cautious with sensitive data in logs and traces:

```python
# ✅ GOOD - Redact sensitive data
import logging

def log_query(query: str):
    # Redact PII before logging
    redacted = redact_pii(query)
    logging.info(f"Processing query: {redacted}")
```

### 6. Dependency Management

Keep dependencies up to date:

```bash
# Check for vulnerabilities
pip install safety
safety check

# Update dependencies
pip install --upgrade ahs-agentic
```

### 7. Rate Limiting

Implement rate limiting to prevent abuse:

```python
from functools import lru_cache
import time

@lru_cache(maxsize=1000)
def get_rate_limiter(user_id: str):
    return {"count": 0, "reset_time": time.time() + 3600}

def check_rate_limit(user_id: str, max_requests: int = 100):
    limiter = get_rate_limiter(user_id)
    if time.time() > limiter["reset_time"]:
        limiter["count"] = 0
        limiter["reset_time"] = time.time() + 3600
    
    if limiter["count"] >= max_requests:
        raise Exception("Rate limit exceeded")
    
    limiter["count"] += 1
```

---

## Known Security Considerations

### Graph State Persistence

**Risk**: Graph state may contain sensitive information.

**Mitigation**:
- Encrypt graph state at rest
- Use role-based access control (RBAC)
- Implement audit logging for state access

### Vector Embeddings

**Risk**: Embeddings can potentially leak information about source documents.

**Mitigation**:
- Use secure vector databases with encryption
- Implement access controls on embedding storage
- Consider differential privacy for sensitive embeddings

### Forensic Traces

**Risk**: Forensic traces may expose reasoning paths that contain sensitive data.

**Mitigation**:
- Redact PII from traces
- Implement access controls on trace retrieval
- Use time-limited trace retention policies

### LLM Prompt Injection

**Risk**: User inputs could manipulate LLM behavior.

**Mitigation**:
- Validate and sanitize all user inputs
- Use prompt templates with clear boundaries
- Implement output filtering

---

## Security Audit History

| Date | Auditor | Scope | Findings | Status |
|------|---------|-------|----------|--------|
| 2026-02-11 | Internal | Initial Release | N/A | ✅ Complete |

---

## Responsible Disclosure

We believe in responsible disclosure and will:

1. **Acknowledge** your report within 24 hours
2. **Assess** the vulnerability severity within 7 days
3. **Fix** the issue based on severity (see timeline above)
4. **Credit** you in our security advisory (unless you prefer anonymity)
5. **Coordinate** public disclosure timing with you

### Hall of Fame

We recognize security researchers who help make AHS safer:

*No vulnerabilities reported yet. Be the first!*

---

## Security Contact

- **GitHub Security Advisories**: [github.com/sachinecin/AHS_Agentic/security/advisories/new](https://github.com/sachinecin/AHS_Agentic/security/advisories/new)
- **Response Time**: Within 24 hours for critical issues

---

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OpenAI Security Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

---

**Thank you for helping keep AHS Agentic and its users safe!** 🔒
