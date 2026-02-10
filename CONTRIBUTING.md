# Contributing to AHS Agentic

Thank you for your interest in contributing to the Agentic Hyper-Graph Synapse project!

## Code of Conduct
Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs
- Use the GitHub issue tracker
- Include detailed reproduction steps
- Provide system information and error logs
- Tag with `bug` label

### Suggesting Enhancements
- Check existing issues first
- Clearly describe the use case
- Explain the expected vs. current behavior
- Tag with `enhancement` label

### Pull Requests

#### Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation
7. Commit with clear messages (`git commit -m 'Add amazing feature'`)
8. Push to your branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

#### PR Checklist
- [ ] Does this reduce "Reasoning Regret"?
- [ ] Have you tested the "Skeptic Subroutine" triggers?
- [ ] Performance check: Impact on Decision Velocity?
- [ ] Token overhead reduction measured?
- [ ] Documentation updated?
- [ ] Tests added/updated?
- [ ] Code follows style guidelines?

### Development Setup

```bash
# Clone the repository
git clone https://github.com/sachinecin/AHS_Agentic.git
cd AHS_Agentic

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8 src/
black src/
mypy src/
```

### Coding Standards
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all public functions
- Maintain test coverage above 80%
- Keep functions focused and modular

### Architecture Principles
- **Non-Destructive**: Never lose data; always layer
- **Traceable**: Every decision must have provenance
- **Efficient**: Optimize for token usage and latency
- **Skeptical**: Always validate against conflicts

## Community

- **GitHub Discussions**: For questions and ideas
- **Issues**: For bugs and feature requests
- **Pull Requests**: For code contributions

## Recognition
Contributors will be recognized in our README and release notes.

Thank you for making AHS better! 🚀
