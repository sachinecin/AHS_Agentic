# Contributing to AHS Agentic

Thank you for your interest in contributing to AHS (Agentic Hyper-Graph Synapse)! We're building the future of enterprise AI reasoning, and we welcome contributions from developers, researchers, and AI practitioners.

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Branch Naming Conventions](#branch-naming-conventions)
5. [Commit Message Standards](#commit-message-standards)
6. [Pull Request Process](#pull-request-process)
7. [Code Review Checklist](#code-review-checklist)
8. [Testing Requirements](#testing-requirements)
9. [Documentation Standards](#documentation-standards)
10. [Performance Benchmarking](#performance-benchmarking)
11. [Reporting Bugs](#reporting-bugs)
12. [Feature Requests](#feature-requests)

---

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

**Key Principles**:
- Be respectful and constructive in all interactions
- Welcome diverse perspectives and experiences
- Focus on what's best for the community and the project
- Show empathy towards other community members

---

## Getting Started

### Prerequisites

- **Python**: 3.9, 3.10, 3.11, or 3.12
- **Git**: 2.30 or higher
- **pip**: Latest version
- **Make**: For running Makefile commands (optional)

### Development Setup

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then:
   git clone https://github.com/YOUR_USERNAME/AHS_Agentic.git
   cd AHS_Agentic
   ```

2. **Set up upstream remote**
   ```bash
   git remote add upstream https://github.com/sachinecin/AHS_Agentic.git
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   # Core dependencies
   pip install -e .
   
   # Development dependencies
   pip install -e ".[dev]"
   
   # Or using Make
   make install-dev
   ```

5. **Verify installation**
   ```bash
   python -c "import ahs_agentic; print(ahs_agentic.__version__)"
   make test
   ```

---

## Development Workflow

### 1. Create a Feature Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

Follow our coding standards (see below) and ensure all tests pass:

```bash
# Run linters
make lint

# Run tests
make test

# Run type checking
mypy src/
```

### 3. Commit Your Changes

Use semantic commit messages (see [Commit Message Standards](#commit-message-standards)):

```bash
git add .
git commit -m "feat: add skeptic confidence threshold calibration"
```

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
# Then create a Pull Request on GitHub
```

---

## Branch Naming Conventions

Use descriptive branch names following this pattern:

```
<type>/<short-description>
```

**Types**:
- `feature/` - New features (e.g., `feature/gpu-acceleration`)
- `fix/` - Bug fixes (e.g., `fix/memory-leak-tier2`)
- `docs/` - Documentation only (e.g., `docs/api-reference-update`)
- `refactor/` - Code refactoring (e.g., `refactor/graph-engine`)
- `test/` - Test additions or modifications (e.g., `test/skeptic-edge-cases`)
- `perf/` - Performance improvements (e.g., `perf/parallel-hop-optimization`)
- `chore/` - Maintenance tasks (e.g., `chore/update-dependencies`)

**Examples**:
```bash
feature/temporal-reasoning
fix/skeptic-false-positive-rate
docs/architecture-deep-dive
refactor/latent-memory-tiering
perf/vector-db-batching
```

---

## Commit Message Standards

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code change that neither fixes a bug nor adds a feature
- `perf`: Performance improvement
- `test`: Adding or updating tests
- `chore`: Maintenance tasks, dependency updates
- `ci`: CI/CD pipeline changes

### Scopes (Optional)

- `skeptic`: Skeptic Subroutine
- `retrieval`: Speculative Retrieval
- `memory`: Latent Memory System
- `graph`: Hyper-Graph Engine
- `core`: Core framework
- `docs`: Documentation
- `ci`: CI/CD

### Examples

```bash
feat(skeptic): add confidence score to conflict reports

Adds a confidence score (0.0-1.0) to Skeptic conflict reports
to help users assess the reliability of conflict detection.

Closes #123

---

fix(retrieval): prevent race condition in parallel hop

Fixed race condition where concurrent vector searches could
corrupt the result cache. Added semaphore protection.

---

docs(architecture): update graph schema design section

Updated ARCHITECTURE.md with detailed graph schema design
and complexity analysis.

---

perf(memory): optimize tier promotion with lazy loading

Reduced tier promotion overhead by 60% through lazy loading
of dormant facts only when accessed.

Benchmark: 280ms → 112ms (p95)
```

---

## Pull Request Process

### Before Submitting

1. ✅ All tests pass locally
2. ✅ Code is properly formatted (`make format`)
3. ✅ No linting errors (`make lint`)
4. ✅ Type hints are correct (`mypy src/`)
5. ✅ Documentation is updated
6. ✅ Benchmarks run (if applicable)
7. ✅ CHANGELOG.md is updated (for significant changes)

### PR Template

When creating a PR, fill out the template completely:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Technical Checklist
- [ ] Reasoning Regret impact assessed
- [ ] Skeptic Subroutine compatibility verified
- [ ] Decision Velocity implications documented
- [ ] Token cost impact analyzed

## Impact on Unit Economics
Describe cost/performance implications

## Breaking Changes
List any breaking changes

## Documentation Updates
- [ ] README.md updated
- [ ] API docs updated
- [ ] Examples added/updated

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Benchmarks run

## Related Issues
Closes #XXX
```

### Review Process

1. **Automated Checks**: CI must pass (linting, tests, coverage)
2. **Code Review**: At least 1 approval from maintainers
3. **Performance Review**: Benchmarks reviewed for regressions
4. **Documentation Review**: Docs must be clear and complete

**Review Timeline**: We aim to review PRs within 48 hours.

---

## Code Review Checklist

### For Authors

Before requesting review:

- [ ] Code follows PEP 8 style guidelines
- [ ] All functions have docstrings with type hints
- [ ] Complex logic has explanatory comments
- [ ] Error handling is comprehensive
- [ ] Tests cover edge cases
- [ ] Performance benchmarks run (if applicable)
- [ ] Breaking changes are documented
- [ ] Examples are updated

### For Reviewers

When reviewing:

- [ ] Code is clear and maintainable
- [ ] Logic is correct and efficient
- [ ] Tests are comprehensive
- [ ] Documentation is accurate
- [ ] No security vulnerabilities introduced
- [ ] Performance implications are acceptable
- [ ] Breaking changes are justified

---

## Testing Requirements

### Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── test_skeptic.py       # Skeptic Subroutine tests
├── test_retrieval.py     # Retrieval system tests
├── test_memory.py        # Memory layer tests
└── integration/
    ├── test_e2e.py       # End-to-end tests
    └── test_forensic.py  # Forensic reconciliation tests
```

### Test Categories

1. **Unit Tests**: Test individual functions/classes
   ```python
   def test_conflict_delta_computation():
       skeptic = SkepticSubroutine(sensitivity_threshold=0.85)
       vec1 = np.array([1.0, 0.0, 0.0])
       vec2 = np.array([0.0, 1.0, 0.0])
       delta = skeptic.compute_conflict_delta(vec1, vec2)
       assert delta > 0.85
   ```

2. **Integration Tests**: Test component interactions
   ```python
   @pytest.mark.asyncio
   async def test_skeptic_with_retrieval():
       retriever = SpeculativeRetriever(max_parallel_hops=5)
       skeptic = SkepticSubroutine(sensitivity_threshold=0.85)
       # Test integration
   ```

3. **Performance Tests**: Benchmark critical paths
   ```python
   def test_retrieval_performance(benchmark):
       retriever = SpeculativeRetriever(max_parallel_hops=5)
       queries = [f"query{i}" for i in range(100)]
       result = benchmark(retriever.parallel_hop, queries)
       assert result.latency_p95 < 500  # ms
   ```

### Coverage Requirements

- **Minimum Coverage**: 80%
- **Critical Paths**: 95% (Skeptic, Retrieval, Memory)
- **New Code**: 90%

Run coverage:
```bash
make test-cov
# Open htmlcov/index.html to view report
```

### Writing Good Tests

**DO**:
- ✅ Test one behavior per test
- ✅ Use descriptive test names
- ✅ Include docstrings explaining what's tested
- ✅ Test edge cases and error conditions
- ✅ Use fixtures for common setup
- ✅ Mock external dependencies (APIs, databases)

**DON'T**:
- ❌ Test implementation details
- ❌ Create flaky tests
- ❌ Write overly complex tests
- ❌ Skip error case testing
- ❌ Rely on test execution order

---

## Documentation Standards

### Code Documentation

1. **Module Docstrings**
   ```python
   """
   Skeptic Subroutine for conflict detection.
   
   This module implements the Skeptic Subroutine, which detects
   logical conflicts between new evidence and existing graph state
   using semantic vector divergence.
   """
   ```

2. **Class Docstrings**
   ```python
   class SkepticSubroutine:
       """
       Detects and resolves conflicts in the hyper-graph.
       
       The Skeptic Subroutine uses cosine similarity to compute
       conflict deltas between fact vectors. When delta exceeds
       the sensitivity threshold, dormant facts are re-activated
       for conflict resolution.
       
       Attributes:
           threshold (float): Sensitivity threshold (0.0-1.0)
           conflict_history (List[dict]): Historical conflicts
       
       Example:
           >>> skeptic = SkepticSubroutine(sensitivity_threshold=0.85)
           >>> delta = skeptic.compute_conflict_delta(vec1, vec2)
           >>> if skeptic.should_trigger(delta):
           ...     report = skeptic.generate_conflict_report(...)
       """
   ```

3. **Function Docstrings**
   ```python
   def compute_conflict_delta(
       self,
       existing_fact_vector: np.ndarray,
       new_evidence_vector: np.ndarray
   ) -> float:
       """
       Compute semantic divergence between fact vectors.
       
       Args:
           existing_fact_vector: Embedding of existing fact
           new_evidence_vector: Embedding of new evidence
       
       Returns:
           Conflict delta score (0.0 = identical, 1.0 = opposite)
       
       Raises:
           ValueError: If vectors have different dimensions
       
       Example:
           >>> vec1 = np.array([1.0, 0.0, 0.0])
           >>> vec2 = np.array([0.0, 1.0, 0.0])
           >>> delta = skeptic.compute_conflict_delta(vec1, vec2)
           >>> print(f"Conflict: {delta:.2f}")
           Conflict: 1.00
       """
   ```

### User Documentation

Update relevant docs in `docs/`:
- `getting-started.md` - For new user-facing features
- `api-reference.md` - For API changes
- `examples.md` - For new use cases
- `architecture-deep-dive.md` - For architectural changes

---

## Performance Benchmarking

### When to Benchmark

- New features that affect latency or throughput
- Optimizations to existing code
- Changes to Skeptic, Retrieval, or Memory systems

### Running Benchmarks

```bash
# Run all benchmarks
make benchmark

# Run specific benchmark
python benchmarks/benchmark_retrieval.py

# Compare against baseline
python benchmarks/compare_baseline.py
```

### Benchmark Requirements

**New features must not regress**:
- Query latency (p50, p95, p99)
- Token cost per query
- Memory usage
- Throughput (queries/second)

**Example Benchmark**:
```python
import pytest
from ahs_agentic.core.retrieval import SpeculativeRetriever

def test_retrieval_latency(benchmark):
    """Benchmark parallel retrieval latency."""
    retriever = SpeculativeRetriever(max_parallel_hops=5)
    queries = [f"query{i}" for i in range(20)]
    
    result = benchmark(lambda: retriever.parallel_hop(queries))
    
    # Assert performance requirements
    assert result.stats['mean'] < 0.3  # 300ms average
    assert result.stats['stddev'] < 0.1  # Low variance
```

### Reporting Results

Include benchmark results in PR description:
```markdown
## Benchmark Results

| Metric | Baseline | This PR | Change |
|--------|----------|---------|--------|
| Latency p50 | 280ms | 245ms | -12.5% ✅ |
| Latency p95 | 630ms | 580ms | -7.9% ✅ |
| Token Cost | $0.03 | $0.025 | -16.7% ✅ |
| Throughput | 350 q/s | 385 q/s | +10% ✅ |
```

---

## Reporting Bugs

### Before Reporting

1. **Search existing issues**: Your bug may already be reported
2. **Update to latest version**: Bug may already be fixed
3. **Reproduce consistently**: Ensure bug is reproducible

### Bug Report Template

Use the GitHub issue template (`.github/ISSUE_TEMPLATE/bug_report.md`):

```markdown
**AHS Component Affected**
- [ ] Speculative Retrieval
- [ ] Latent Layering
- [ ] Skeptic Subroutine
- [ ] Graph Engine
- [ ] Other: ___

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.10.8]
- AHS Version: [e.g., 1.0.0]

**Description**
Clear description of the bug

**Reproduction Steps**
1. Step 1
2. Step 2
3. ...

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happened

**Performance Impact** (if applicable)
- Query latency: X ms
- Token cost: $X
- Memory usage: X MB

**Logs/Screenshots**
Paste relevant logs or screenshots
```

---

## Feature Requests

### Feature Request Template

Use the GitHub issue template (`.github/ISSUE_TEMPLATE/feature_request.md`):

```markdown
**Problem Statement**
What problem does this feature solve?

**Proposed Solution**
How should the feature work?

**Impact on Core AHS Principles**
- Reasoning Regret: [increase/decrease/neutral]
- Decision Velocity: [impact description]
- Token Efficiency: [impact description]

**Performance Implications**
- Expected latency impact: ___
- Expected token cost impact: ___
- Expected memory usage: ___

**Breaking Change?**
- [ ] Yes
- [ ] No

If yes, describe migration path.

**Alternatives Considered**
What other approaches did you consider?
```

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, general discussion
- **Discord**: Real-time chat (https://discord.gg/ahs-framework)
- **Email**: dev@ahs-framework.ai

### Getting Help

- 📖 **Documentation**: https://github.com/sachinecin/AHS_Agentic/docs
- 💬 **Discussions**: https://github.com/sachinecin/AHS_Agentic/discussions
- 🐛 **Bug Reports**: https://github.com/sachinecin/AHS_Agentic/issues

---

## Recognition

Contributors will be recognized in:
- CHANGELOG.md (for significant contributions)
- GitHub Contributors page
- Annual contributor highlights

---

## Questions?

If you have questions about contributing, please:
1. Check the documentation
2. Search existing issues/discussions
3. Ask in Discord
4. Open a GitHub Discussion

Thank you for contributing to AHS Agentic! 🚀

---

**Last Updated**: 2026-02-10  
**Version**: 1.0.0
