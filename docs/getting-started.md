# Getting Started with AHS Agentic

This guide will walk you through installing AHS Agentic and building your first agent.

---

## Table of Contents

1. [Installation](#installation)
2. [Environment Setup](#environment-setup)
3. [Your First Agent](#your-first-agent)
4. [Basic Operations](#basic-operations)
5. [Common Patterns](#common-patterns)
6. [Next Steps](#next-steps)

---

## Installation

### Prerequisites

Before installing AHS, ensure you have:

- **Python 3.9 or higher** ([Download](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** (for source installation)

### Option 1: Install via pip (Recommended)

```bash
pip install ahs-agentic
```

### Option 2: Install from source

```bash
git clone https://github.com/sachinecin/AHS_Agentic.git
cd AHS_Agentic
pip install -e .
```

### Option 3: Install with Poetry

```bash
poetry add ahs-agentic
```

### Verify Installation

```bash
python -c "import ahs_agentic; print(f'AHS version: {ahs_agentic.__version__}')"
```

Expected output:
```
AHS version: 1.0.0
```

---

## Environment Setup

### 1. API Keys

AHS requires an LLM API key. Create a `.env` file:

```bash
# .env
OPENAI_API_KEY=sk-your-api-key-here
QDRANT_API_KEY=your-qdrant-key-here  # Optional, for cloud Qdrant
REDIS_PASSWORD=your-redis-password   # Optional, for Tier 2 cache
```

**Security Note:** Never commit API keys to version control. Add `.env` to your `.gitignore`.

### 2. Vector Database Setup (Optional)

AHS can run with in-memory storage for testing, but for production we recommend:

#### Option A: Local Qdrant (Docker)

```bash
docker run -p 6333:6333 qdrant/qdrant
```

#### Option B: Cloud Qdrant

Sign up at [qdrant.tech](https://qdrant.tech) and get your API key.

### 3. Redis Cache Setup (Optional)

For optimal performance, set up Redis for Tier 2 caching:

```bash
# Using Docker
docker run -p 6379:6379 redis:latest

# Or using Homebrew (macOS)
brew install redis
redis-server
```

---

## Your First Agent

Let's create a simple agent that can answer questions about documents.

### Step 1: Import AHS

```python
# main.py
from ahs_agentic import HyperGraphAgent
import asyncio
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
```

### Step 2: Initialize the Agent

```python
# Initialize with basic configuration
agent = HyperGraphAgent(
    memory_mode="latent-layering",           # Enable 3-tier memory
    retrieval_strategy="speculative-parallel",  # Parallel hop retrieval
    skeptic_threshold=0.85                   # Conflict detection sensitivity
)

print("✅ AHS Agent initialized successfully!")
```

### Step 3: Process a Simple Query

```python
async def simple_query():
    # For demonstration, we'll use the resolve_conflict method
    # In a real scenario, you'd ingest documents first
    
    result = await agent.resolve_conflict(
        legacy_sop="All transactions require manual approval",
        new_regulation="Automated approval allowed for transactions under $50K",
        context="Payment Processing Policy"
    )
    
    print("\n📊 Results:")
    print(f"Status: {result['status']}")
    print(f"Velocity Gain: {result['velocity_gain']}x faster")
    print(f"Token Savings: {result['token_savings'] * 100}%")
    print(f"Reasoning Regret Reduction: {result['reasoning_regret_reduction'] * 100}%")

# Run the async function
asyncio.run(simple_query())
```

### Complete First Example

```python
# first_agent.py
from ahs_agentic import HyperGraphAgent
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def main():
    # Initialize agent
    agent = HyperGraphAgent(
        memory_mode="latent-layering",
        retrieval_strategy="speculative-parallel",
        skeptic_threshold=0.85
    )
    
    print("🧠 AHS Agent initialized!\n")
    
    # Example: Detect conflict between documents
    result = await agent.resolve_conflict(
        legacy_sop="Employees must request vacation 30 days in advance",
        new_regulation="Updated policy: 14 days advance notice is sufficient",
        context="HR Policy Reconciliation"
    )
    
    # Display results
    print("📊 Reconciliation Results:")
    print("-" * 50)
    print(f"Status: {result['status']}")
    print(f"Decision Velocity: {result['velocity_gain']}x improvement")
    print(f"Token Savings: {result['token_savings'] * 100:.1f}%")
    print(f"Reasoning Quality: {result['reasoning_regret_reduction'] * 100:.1f}% better")
    print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python first_agent.py
```

Expected output:

```
🧠 AHS Agent initialized!
🧠 AHS Synapse Core: Resolving 'HR Policy Reconciliation'
♻️  Promoting dormant facts for context: HR Policy Reconciliation

📊 Reconciliation Results:
--------------------------------------------------
Status: conflict_detected
Decision Velocity: 3.5x improvement
Token Savings: 60.0%
Reasoning Quality: 90.0% better
--------------------------------------------------
```

---

## Basic Operations

### Document Ingestion

```python
async def ingest_documents():
    agent = HyperGraphAgent()
    
    # Ingest a single document
    await agent.ingest_document(
        content="Company policy: All employees receive 15 vacation days annually.",
        metadata={
            "source": "HR-Policy-2024",
            "category": "benefits",
            "version": "1.0"
        }
    )
    
    print("✅ Document ingested into graph state")
```

### Query the Graph

```python
async def query_graph():
    agent = HyperGraphAgent()
    
    # Query for specific information
    result = await agent.query(
        question="What is the vacation policy?",
        context="HR Benefits"
    )
    
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']}")
```

### Access Metrics

```python
def check_metrics():
    agent = HyperGraphAgent()
    
    # Get current performance metrics
    metrics = agent.get_metrics()
    
    print(f"Decision Velocity: {metrics['decision_velocity']}x")
    print(f"Reasoning Regret: {metrics['reasoning_regret']:.2%}")
    print(f"Token Efficiency: {metrics['token_efficiency']:.2f}")
```

---

## Common Patterns

### Pattern 1: Conflict Resolution

Use this when you need to reconcile contradictory documents:

```python
async def reconcile_policies():
    agent = HyperGraphAgent(
        skeptic_threshold=0.85  # Higher = more sensitive
    )
    
    result = await agent.resolve_conflict(
        legacy_sop="Policy A: Manual signature required",
        new_regulation="Policy B: Electronic signatures accepted",
        context="Document Signing Policy"
    )
    
    if result['status'] == 'conflict_detected':
        print("⚠️  Conflict found!")
        print(f"Recommended action: {result['conflict_report']['resolution_strategy']}")
    else:
        print("✅ Policies are aligned")
```

### Pattern 2: Multi-Document Analysis

Analyze relationships across multiple documents:

```python
async def analyze_multiple_docs():
    agent = HyperGraphAgent()
    
    # Ingest multiple related documents
    documents = [
        {"content": "SOP-001: Quality standards", "metadata": {"type": "sop"}},
        {"content": "Regulation X: Quality requirements", "metadata": {"type": "regulation"}},
        {"content": "Audit-2024: Compliance findings", "metadata": {"type": "audit"}}
    ]
    
    for doc in documents:
        await agent.ingest_document(doc['content'], doc['metadata'])
    
    # Query across all documents
    result = await agent.query(
        question="Are our quality standards compliant with Regulation X?",
        context="Quality Compliance"
    )
    
    print(f"Compliance Status: {result['status']}")
```

### Pattern 3: Forensic Tracing

Retrieve the complete reasoning path for audit purposes:

```python
def get_audit_trail():
    agent = HyperGraphAgent()
    
    # After processing a query
    query_id = "some-query-id"
    
    # Get forensic trace
    trace = agent.get_forensic_trace(query_id)
    
    print("🔍 Audit Trail:")
    for step in trace['reasoning_path']:
        print(f"  - {step}")
```

### Pattern 4: Custom Configuration

Configure for specific use cases:

```python
# For high-stakes medical applications
medical_agent = HyperGraphAgent(
    memory_mode="latent-layering",
    retrieval_strategy="speculative-parallel",
    skeptic_threshold=0.92,  # Very high sensitivity
    vector_db_config={
        "provider": "qdrant",
        "collection": "medical_records",
        "dimension": 1536
    }
)

# For legal document review
legal_agent = HyperGraphAgent(
    skeptic_threshold=0.88,  # Balanced sensitivity
    vector_db_config={
        "provider": "pinecone",
        "index": "legal_contracts"
    }
)

# For technical documentation
tech_agent = HyperGraphAgent(
    skeptic_threshold=0.85,  # Lower sensitivity (terminology variance)
    retrieval_strategy="speculative-parallel"
)
```

---

## Next Steps

### Learn More

- **[Architecture Deep-Dive](../ARCHITECTURE.md)** - Understand how AHS works internally
- **[API Reference](api-reference.md)** - Explore the complete API
- **[Examples](../examples/)** - See real-world implementations

### Advanced Topics

- **[Production Deployment](../ARCHITECTURE.md#scalability-considerations)** - Deploy AHS at scale
- **[Performance Tuning](../ARCHITECTURE.md#performance-characteristics)** - Optimize for your use case
- **[Security Best Practices](../SECURITY.md)** - Secure your deployment

### Get Help

- **[GitHub Discussions](https://github.com/sachinecin/AHS_Agentic/discussions)** - Ask questions
- **[Issue Tracker](https://github.com/sachinecin/AHS_Agentic/issues)** - Report bugs
- **[Contributing Guide](../CONTRIBUTING.md)** - Contribute to AHS

---

## Troubleshooting

### Common Issues

**Problem:** `ImportError: No module named 'ahs_agentic'`

**Solution:** Ensure AHS is installed:
```bash
pip install ahs-agentic
```

---

**Problem:** `OpenAI API key not found`

**Solution:** Set your API key:
```bash
export OPENAI_API_KEY=sk-your-key-here
```

Or use a `.env` file with `python-dotenv`.

---

**Problem:** `Connection refused to Qdrant`

**Solution:** Start Qdrant locally:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

---

**Problem:** Slow performance

**Solution:** 
1. Enable Tier 2 caching with Redis
2. Use speculative-parallel retrieval
3. Check vector DB latency

---

## Example Projects

Check out these complete examples:

1. **[Basic Usage](../examples/basic_usage.py)** - Simple agent setup
2. **[Forensic Reconciliation](../examples/forensic_reconciliation.py)** - Conflict detection
3. **[Regulatory Compliance](../examples/regulatory_compliance.py)** - Real-world use case

---

**You're now ready to build with AHS! 🚀**

[← Back to Documentation](index.md) | [API Reference →](api-reference.md)
