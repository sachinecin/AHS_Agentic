---
name: Bug Report
about: Create a report to help us improve AHS Agentic
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description

<!-- A clear and concise description of what the bug is -->

## Steps to Reproduce

<!-- Detailed steps to reproduce the behavior -->

1. Initialize agent with '...'
2. Call method '....'
3. Provide input '....'
4. See error

## Expected Behavior

<!-- A clear and concise description of what you expected to happen -->

## Actual Behavior

<!-- A clear and concise description of what actually happened -->

## Error Message

<!-- If applicable, paste the full error message and stack trace -->

```python
# Paste error message here
```

## Code Example

<!-- Minimal code example that reproduces the issue -->

```python
from ahs_agentic import HyperGraphAgent

# Your code here that reproduces the bug
agent = HyperGraphAgent(...)
result = agent.resolve_conflict(...)
```

## Environment Details

- **OS**: [e.g., Ubuntu 22.04, macOS 14, Windows 11]
- **Python Version**: [e.g., 3.9.5, 3.10.8, 3.11.2]
- **AHS Version**: [e.g., 1.0.0]
- **Installation Method**: [pip, Poetry, source]
- **Vector DB**: [Qdrant, Pinecone, Weaviate, None]
- **Cache Provider**: [Redis, Memcached, None]
- **LLM Provider**: [OpenAI, Azure OpenAI, Anthropic]

## Dependencies

<!-- Output of `pip freeze | grep ahs` or relevant dependencies -->

```
ahs-agentic==1.0.0
# Other relevant packages
```

## Configuration

<!-- If applicable, share your configuration (redact sensitive data like API keys) -->

```python
agent_config = {
    "memory_mode": "latent-layering",
    "retrieval_strategy": "speculative-parallel",
    "skeptic_threshold": 0.85,
    # ...
}
```

## Impact

<!-- How does this bug affect your usage? -->

- [ ] Blocks critical functionality
- [ ] Causes incorrect results
- [ ] Performance degradation
- [ ] Minor inconvenience

## Potential Cause

<!-- If you have investigated, what do you think might be causing this? -->

## Attempted Solutions

<!-- What have you tried so far to fix or work around the issue? -->

## Additional Context

<!-- Add any other context about the problem here -->

## Related Issues

<!-- Link to related issues if any: #123, #456 -->

## Logs

<!-- If applicable, attach relevant log files (redact sensitive information) -->

<details>
<summary>Click to expand logs</summary>

```
Paste logs here
```

</details>

---

**Note**: Before submitting, please:
1. Search existing issues to avoid duplicates
2. Ensure you're using the latest version
3. Try to provide a minimal reproducible example
4. Redact any sensitive information (API keys, private data)
