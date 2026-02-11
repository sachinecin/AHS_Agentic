# Contributing to AHS Agentic 🤝

Thank you for your interest in contributing to the Agentic Hyper-Graph Synapse! We're building the future of enterprise-grade AI reasoning, and we're excited to have you join us.

---

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
3. [Development Setup](#development-setup)
4. [Coding Standards](#coding-standards)
5. [Testing Requirements](#testing-requirements)
6. [Pull Request Process](#pull-request-process)
7. [Issue Reporting Guidelines](#issue-reporting-guidelines)
8. [Community Channels](#community-channels)

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- A clear and descriptive title
- Detailed steps to reproduce the issue
- Expected vs. actual behavior
- Environment details (OS, Python version, AHS version)
- Relevant logs or error messages

Use our [bug report template](.github/ISSUE_TEMPLATE/bug_report.md).

### 💡 Suggesting Enhancements

Enhancement suggestions are welcome! Please:

- Use a clear and descriptive title
- Provide a detailed description of the proposed functionality
- Explain why this enhancement would be useful
- Consider the impact on unit economics and performance metrics

Use our [feature request template](.github/ISSUE_TEMPLATE/feature_request.md).

### 📝 Improving Documentation

Documentation improvements are always appreciated:

- Fix typos or clarify confusing sections
- Add examples or use cases
- Improve API documentation
- Create tutorials or guides

### 🔧 Contributing Code

We love code contributions! Here's how to get started:

1. **Fork the repository** and create a branch from `main`
2. **Make your changes** following our coding standards
3. **Add tests** for any new functionality
4. **Ensure tests pass** and code meets quality standards
5. **Submit a pull request** with a clear description

---

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- pip or Poetry (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/sachinecin/AHS_Agentic.git
cd AHS_Agentic
```

### Step 2: Create a Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Or using conda
conda create -n ahs python=3.9
conda activate ahs
```

### Step 3: Install Dependencies

```bash
# Install core dependencies
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Or using Makefile
make install
```

### Step 4: Verify Installation

```bash
# Run tests
pytest

# Or using Makefile
make test
```

### Step 5: Set Up Pre-commit Hooks (Optional)

```bash
pre-commit install
```

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line Length**: 100 characters (not 79)
- **Quotes**: Double quotes for strings
- **Imports**: Use absolute imports, grouped by standard library → third-party → local
- **Type Hints**: Required for all public functions

### Code Formatting

We use **Black** for automatic code formatting:

```bash
# Format all files
black src/ tests/

# Or using Makefile
make format
```

### Linting

We use **Ruff** for fast linting:

```bash
# Lint all files
ruff check src/ tests/

# Or using Makefile
make lint
```

### Type Checking

We use **mypy** for static type checking:

```bash
# Type check all files
mypy src/

# Or using Makefile
make typecheck
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `HyperGraphAgent`)
- **Functions**: `snake_case` (e.g., `resolve_conflict`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_THRESHOLD`)
- **Private methods**: Prefix with `_` (e.g., `_promote_dormant_facts`)

### Documentation Standards

All public functions must have docstrings:

```python
def resolve_conflict(
    self,
    legacy_sop: str,
    new_regulation: str,
    context: str = "Forensic Reconciliation"
) -> Dict[str, Any]:
    """
    Resolve conflicts between legacy SOPs and new regulations.
    
    This method implements the Skeptic Subroutine to detect semantic
    divergence and generate forensic reconciliation reports.
    
    Args:
        legacy_sop: Text of the existing standard operating procedure
        new_regulation: Text of the new regulatory requirement
        context: Human-readable description of the reconciliation context
        
    Returns:
        Dictionary containing:
            - status: "conflict_detected" or "aligned"
            - velocity_gain: Performance improvement factor (float)
            - reasoning_regret_reduction: Error reduction percentage (float)
            - token_savings: Cost savings percentage (float)
            - conflict_report: Optional detailed conflict analysis
            
    Example:
        >>> agent = HyperGraphAgent()
        >>> result = await agent.resolve_conflict(
        ...     legacy_sop="Manual approval for >$10K",
        ...     new_regulation="Automated approval up to $50K"
        ... )
        >>> print(result['status'])
        'conflict_detected'
    """
    # Implementation...
```

---

## Testing Requirements

### Test Coverage

- All new features must have tests
- Aim for >90% code coverage
- Tests should cover both happy paths and edge cases

### Test Structure

```python
# tests/test_skeptic.py
import pytest
from ahs_agentic.core.skeptic import SkepticSubroutine

class TestSkepticSubroutine:
    """Tests for the Skeptic Subroutine conflict detection."""
    
    def test_conflict_detection_high_delta(self):
        """Test that high delta triggers conflict detection."""
        skeptic = SkepticSubroutine(sensitivity_threshold=0.85)
        result = skeptic.evaluate_conflict(
            existing_fact_vector=np.array([1, 0, 0, 0]),
            new_evidence_vector=np.array([0, 1, 0, 0])
        )
        assert result.conflict_detected is True
        assert result.delta_score > 0.85
    
    def test_no_conflict_low_delta(self):
        """Test that low delta does not trigger conflict detection."""
        skeptic = SkepticSubroutine(sensitivity_threshold=0.85)
        result = skeptic.evaluate_conflict(
            existing_fact_vector=np.array([1, 0, 0, 0]),
            new_evidence_vector=np.array([0.9, 0.1, 0, 0])
        )
        assert result.conflict_detected is False
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ahs_agentic --cov-report=html

# Run specific test file
pytest tests/test_skeptic.py

# Run specific test
pytest tests/test_skeptic.py::TestSkepticSubroutine::test_conflict_detection_high_delta

# Or using Makefile
make test
```

### Performance Tests

For performance-critical changes, include benchmarks:

```python
def test_parallel_hop_performance(benchmark):
    """Benchmark speculative parallel-hop retrieval."""
    agent = HyperGraphAgent(retrieval_strategy="speculative-parallel")
    result = benchmark(agent.retriever.parallel_hop, ["query1", "query2", "query3"])
    assert result is not None
```

---

## Pull Request Process

### Before Submitting

1. **Update documentation** for any API changes
2. **Run all tests** and ensure they pass
3. **Run linters** and fix any issues
4. **Update CHANGELOG.md** with your changes
5. **Rebase on main** to ensure a clean history

### PR Checklist

Use our [PR template](.github/PULL_REQUEST_TEMPLATE.md) which includes:

- [ ] Description of changes
- [ ] Related issue number (if applicable)
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Code passes linting and type checking
- [ ] Does this reduce "Reasoning Regret"?
- [ ] Performance impact quantified
- [ ] Breaking changes documented

### PR Title Format

Use conventional commit format:

- `feat: Add adaptive threshold calibration`
- `fix: Resolve memory leak in Tier 2 cache`
- `docs: Update API reference for SkepticSubroutine`
- `perf: Optimize parallel hop batching`
- `test: Add coverage for conflict resolution`
- `chore: Update dependencies`

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by at least one maintainer
3. **Performance validation** for perf-critical changes
4. **Documentation review** for API changes
5. **Approval** from maintainers before merge

### After Approval

- Maintainers will merge using "Squash and Merge"
- Your contribution will be credited in CHANGELOG.md
- Celebrate! 🎉

---

## Issue Reporting Guidelines

### Security Issues

**DO NOT** create public issues for security vulnerabilities. Instead, follow our [Security Policy](SECURITY.md).

### Bug Reports

Include:

1. **Environment**: OS, Python version, AHS version
2. **Steps to reproduce**: Minimal code example
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Logs/Screenshots**: Relevant error messages

### Feature Requests

Include:

1. **Problem statement**: What problem does this solve?
2. **Proposed solution**: How would you implement it?
3. **Alternatives**: What other approaches did you consider?
4. **Impact**: How does this affect unit economics/performance?

### Questions

For questions, use [GitHub Discussions](https://github.com/sachinecin/AHS_Agentic/discussions) instead of issues.

---

## Community Channels

### GitHub

- **Issues**: [github.com/sachinecin/AHS_Agentic/issues](https://github.com/sachinecin/AHS_Agentic/issues)
- **Discussions**: [github.com/sachinecin/AHS_Agentic/discussions](https://github.com/sachinecin/AHS_Agentic/discussions)
- **Pull Requests**: [github.com/sachinecin/AHS_Agentic/pulls](https://github.com/sachinecin/AHS_Agentic/pulls)

### Documentation

- **Docs Site**: [sachinecin.github.io/AHS_Agentic](https://sachinecin.github.io/AHS_Agentic)
- **API Reference**: [docs/api-reference.md](docs/api-reference.md)
- **Examples**: [examples/](examples/)

### Stay Updated

- **Star** the repository for updates
- **Watch** for new releases
- Follow the [CHANGELOG](CHANGELOG.md)

---

## Recognition

We value all contributions! Contributors will be:

- Listed in CHANGELOG.md for their contributions
- Recognized in release notes
- Eligible for "AHS Contributor" badge (coming soon)

Top contributors may be invited to join the core maintainer team.

---

## Development Philosophy

### Focus on Unit Economics

When contributing, always consider:

- **Does this reduce token consumption?**
- **Does this improve decision velocity?**
- **Does this reduce reasoning regret?**

These are our north star metrics.

### Forensic Traceability

Every decision should be traceable:

- Log important state changes
- Maintain audit trails
- Document reasoning paths

### Performance First

- Benchmark critical paths
- Optimize hot loops
- Minimize latency

### Enterprise-Grade Quality

- Write production-ready code
- Handle edge cases gracefully
- Provide clear error messages

---

## Questions?

If you have questions about contributing, please:

1. Check existing [documentation](docs/)
2. Search [GitHub Discussions](https://github.com/sachinecin/AHS_Agentic/discussions)
3. Ask in a new discussion thread

---

**Thank you for helping build the future of enterprise AI reasoning! 🚀**
