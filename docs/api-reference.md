# API Reference

Complete API documentation for AHS Agentic.

---

## Core Components

### HyperGraphAgent

The main orchestrator for graph-based reasoning.

```python
from ahs_agentic import HyperGraphAgent
```

#### Constructor

```python
HyperGraphAgent(
    memory_mode: str = "latent-layering",
    retrieval_strategy: str = "speculative-parallel",
    skeptic_threshold: float = 0.85,
    vector_db_config: Optional[Dict] = None,
    tier2_cache_config: Optional[Dict] = None,
    llm_config: Optional[Dict] = None
)
```

**Parameters:**

- `memory_mode` (str): Memory architecture mode
  - `"latent-layering"` (default): 3-tier memory architecture
  - `"sequential"`: Traditional sequential processing
  
- `retrieval_strategy` (str): Retrieval optimization strategy
  - `"speculative-parallel"` (default): Parallel hop with predictive branching
  - `"standard"`: Sequential vector search
  
- `skeptic_threshold` (float): Conflict detection sensitivity (0.0-1.0)
  - `0.85` (default): Balanced sensitivity
  - `0.92`: High sensitivity (medical, safety-critical)
  - `0.88`: Medium sensitivity (legal, compliance)
  - Higher values = more sensitive to conflicts

- `vector_db_config` (dict, optional): Vector database configuration
  ```python
  {
      "provider": "qdrant",  # or "pinecone", "weaviate"
      "host": "localhost:6333",
      "collection": "ahs_facts",
      "dimension": 1536,
      "api_key": "optional-api-key"
  }
  ```

- `tier2_cache_config` (dict, optional): Tier 2 cache configuration
  ```python
  {
      "provider": "redis",  # or "memcached"
      "host": "localhost:6379",
      "ttl": 3600,
      "max_facts": 100000,
      "password": "optional-password"
  }
  ```

- `llm_config` (dict, optional): LLM provider configuration
  ```python
  {
      "provider": "openai",  # or "azure", "anthropic"
      "model": "gpt-4-turbo",
      "temperature": 0.1,
      "max_tokens": 2000,
      "api_key": "optional-api-key"
  }
  ```

**Example:**

```python
agent = HyperGraphAgent(
    memory_mode="latent-layering",
    retrieval_strategy="speculative-parallel",
    skeptic_threshold=0.85,
    vector_db_config={
        "provider": "qdrant",
        "host": "localhost:6333"
    }
)
```

---

#### Methods

##### `resolve_conflict()`

Detect and resolve conflicts between documents using the Skeptic Subroutine.

```python
async def resolve_conflict(
    self,
    legacy_sop: str,
    new_regulation: str,
    context: str = "Forensic Reconciliation Gap"
) -> Dict[str, Any]
```

**Parameters:**

- `legacy_sop` (str): Text of the existing document/policy
- `new_regulation` (str): Text of the new document/regulation
- `context` (str): Human-readable description of the reconciliation context

**Returns:**

Dictionary containing:
- `status` (str): `"conflict_detected"` or `"aligned"`
- `velocity_gain` (float): Performance improvement factor
- `reasoning_regret_reduction` (float): Error reduction (0.0-1.0)
- `token_savings` (float): Cost savings (0.0-1.0)
- `conflict_report` (dict, optional): Detailed conflict analysis when conflicts detected

**Example:**

```python
result = await agent.resolve_conflict(
    legacy_sop="Manual approval required for >$10K",
    new_regulation="Automated approval up to $50K",
    context="Financial Compliance"
)

print(f"Status: {result['status']}")
if result['status'] == 'conflict_detected':
    print(f"Delta: {result['conflict_report']['delta_score']}")
```

---

##### `ingest_document()`

Add a document to the knowledge graph.

```python
async def ingest_document(
    self,
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
    embedding_model: str = "text-embedding-ada-002"
) -> str
```

**Parameters:**

- `content` (str): Document text content
- `metadata` (dict, optional): Document metadata
  ```python
  {
      "source": "document-id",
      "category": "compliance",
      "version": "1.0",
      "date": "2026-02-11"
  }
  ```
- `embedding_model` (str): Embedding model to use

**Returns:**

- `document_id` (str): Unique identifier for the ingested document

**Example:**

```python
doc_id = await agent.ingest_document(
    content="Company policy text...",
    metadata={
        "source": "HR-Policy-2024",
        "category": "benefits"
    }
)
print(f"Ingested: {doc_id}")
```

---

##### `query()`

Query the knowledge graph.

```python
async def query(
    self,
    question: str,
    context: Optional[str] = None,
    max_results: int = 5
) -> Dict[str, Any]
```

**Parameters:**

- `question` (str): Natural language question
- `context` (str, optional): Additional context for the query
- `max_results` (int): Maximum number of relevant facts to retrieve

**Returns:**

Dictionary containing:
- `answer` (str): Generated answer
- `confidence` (float): Confidence score (0.0-1.0)
- `sources` (list): Source documents used
- `forensic_trace` (list): Reasoning path

**Example:**

```python
result = await agent.query(
    question="What is the vacation policy?",
    context="HR Benefits"
)
print(result['answer'])
```

---

##### `get_metrics()`

Retrieve current performance metrics.

```python
def get_metrics(self) -> Dict[str, float]
```

**Returns:**

Dictionary containing:
- `decision_velocity` (float): Speed improvement factor
- `reasoning_regret` (float): Current error rate
- `token_efficiency` (float): Token usage efficiency

**Example:**

```python
metrics = agent.get_metrics()
print(f"Velocity: {metrics['decision_velocity']}x")
print(f"Error Rate: {metrics['reasoning_regret']:.2%}")
```

---

##### `get_forensic_trace()`

Retrieve the complete reasoning path for a query (audit trail).

```python
def get_forensic_trace(self, query_id: str) -> Dict[str, Any]
```

**Parameters:**

- `query_id` (str): Unique identifier of the query

**Returns:**

Dictionary containing:
- `query_id` (str): Query identifier
- `timestamp` (str): ISO timestamp
- `reasoning_path` (list): Step-by-step reasoning trace
- `sources_consulted` (list): Documents accessed
- `conflicts_detected` (list): Any conflicts identified

**Example:**

```python
trace = agent.get_forensic_trace("query-123")
for step in trace['reasoning_path']:
    print(f"- {step}")
```

---

### SkepticSubroutine

Conflict detection and resolution agent.

```python
from ahs_agentic import SkepticSubroutine
```

#### Constructor

```python
SkepticSubroutine(
    sensitivity_threshold: Optional[float] = None,
    domain_context: str = 'default'
)
```

**Parameters:**

- `sensitivity_threshold` (float, optional): Custom threshold (0.0-1.0)
- `domain_context` (str): Domain calibration
  - `"default"`: 0.85
  - `"medical"`: 0.92 (high precision)
  - `"legal"`: 0.88 (balanced)
  - `"technical"`: 0.85 (permissive)

**Example:**

```python
skeptic = SkepticSubroutine(
    domain_context="medical"
)
```

---

#### Methods

##### `evaluate_conflict()`

Evaluate conflict between two pieces of evidence.

```python
def evaluate_conflict(
    self,
    existing_fact_vector: np.ndarray,
    new_evidence_vector: np.ndarray,
    existing_fact_text: str = "",
    new_evidence_text: str = ""
) -> ConflictReport
```

**Parameters:**

- `existing_fact_vector` (ndarray): Embedding of existing fact
- `new_evidence_vector` (ndarray): Embedding of new evidence
- `existing_fact_text` (str, optional): Original text for traceability
- `new_evidence_text` (str, optional): New text for traceability

**Returns:**

`ConflictReport` object with:
- `conflict_detected` (bool): Whether conflict was detected
- `delta_score` (float): Semantic divergence score
- `existing_fact` (str): Original text
- `new_evidence` (str): New text
- `resolution_strategy` (str): Recommended resolution
- `confidence` (float): Confidence in detection

**Example:**

```python
import numpy as np

report = skeptic.evaluate_conflict(
    existing_fact_vector=np.array([1, 0, 0, 0]),
    new_evidence_vector=np.array([0, 1, 0, 0]),
    existing_fact_text="Policy A",
    new_evidence_text="Policy B"
)

if report.conflict_detected:
    print(f"Conflict! Delta: {report.delta_score}")
    print(f"Strategy: {report.resolution_strategy}")
```

---

##### `compute_conflict_delta()`

Compute semantic divergence between two vectors.

```python
def compute_conflict_delta(
    self,
    existing_fact_vector: np.ndarray,
    new_evidence_vector: np.ndarray
) -> float
```

**Returns:**

- `delta` (float): Divergence score (0.0 = identical, 1.0 = completely different)

**Example:**

```python
delta = skeptic.compute_conflict_delta(
    np.array([1, 0]),
    np.array([0, 1])
)
print(f"Divergence: {delta:.2f}")
```

---

##### `should_trigger()`

Determine if Skeptic should trigger based on delta.

```python
def should_trigger(self, delta: float) -> bool
```

**Returns:**

- `True` if delta exceeds threshold
- `False` otherwise

---

##### `get_conflict_statistics()`

Get aggregate statistics on conflicts detected.

```python
def get_conflict_statistics(self) -> Dict[str, float]
```

**Returns:**

Dictionary containing:
- `total_evaluations` (int): Total evaluations performed
- `total_conflicts` (int): Conflicts detected
- `conflict_rate` (float): Conflict detection rate
- `avg_delta` (float): Average delta score
- `current_threshold` (float): Current threshold setting

**Example:**

```python
stats = skeptic.get_conflict_statistics()
print(f"Conflict Rate: {stats['conflict_rate']:.2%}")
```

---

### SpeculativeRetriever

Parallel vector search with predictive branching.

```python
from ahs_agentic import SpeculativeRetriever
```

#### Constructor

```python
SpeculativeRetriever(
    max_parallel_hops: int = 5,
    vector_db_config: Optional[Dict] = None
)
```

**Parameters:**

- `max_parallel_hops` (int): Maximum parallel queries (1-10)
- `vector_db_config` (dict, optional): Vector DB configuration

---

#### Methods

##### `parallel_hop()`

Execute multiple vector searches in parallel.

```python
async def parallel_hop(
    self,
    queries: List[str]
) -> List[Dict[str, Any]]
```

**Parameters:**

- `queries` (list): List of query strings

**Returns:**

- List of result dictionaries with retrieved facts

**Example:**

```python
retriever = SpeculativeRetriever(max_parallel_hops=5)

results = await retriever.parallel_hop([
    "Extract requirements from SOP",
    "Find related regulations",
    "Identify conflicts"
])

for result in results:
    print(result)
```

---

## Data Types

### ConflictReport

```python
@dataclass
class ConflictReport:
    conflict_detected: bool
    delta_score: float
    existing_fact: str
    new_evidence: str
    resolution_strategy: str
    confidence: float
```

**Resolution Strategies:**

- `"ACCEPT_NEW_EVIDENCE"`: No conflict, accept new information
- `"SOFT_MERGE"`: Minor differences, merge compatible
- `"DORMANT_FACT_REACTIVATION"`: Moderate conflict, reactivate context
- `"HARD_CONFLICT_REPLACE"`: Major conflict, flag for review

---

## Configuration

### Vector Database Providers

#### Qdrant

```python
vector_db_config = {
    "provider": "qdrant",
    "host": "localhost:6333",
    "collection": "ahs_facts",
    "dimension": 1536,
    "api_key": "optional"
}
```

#### Pinecone

```python
vector_db_config = {
    "provider": "pinecone",
    "api_key": "your-api-key",
    "environment": "us-west1-gcp",
    "index": "ahs-index",
    "dimension": 1536
}
```

#### Weaviate

```python
vector_db_config = {
    "provider": "weaviate",
    "url": "http://localhost:8080",
    "api_key": "optional",
    "class_name": "AHSFacts"
}
```

---

### Cache Providers

#### Redis

```python
tier2_cache_config = {
    "provider": "redis",
    "host": "localhost:6379",
    "port": 6379,
    "db": 0,
    "password": "optional",
    "ssl": False,
    "ttl": 3600
}
```

---

### LLM Providers

#### OpenAI

```python
llm_config = {
    "provider": "openai",
    "model": "gpt-4-turbo",
    "api_key": os.getenv("OPENAI_API_KEY"),
    "temperature": 0.1,
    "max_tokens": 2000
}
```

#### Azure OpenAI

```python
llm_config = {
    "provider": "azure",
    "model": "gpt-4",
    "api_key": os.getenv("AZURE_OPENAI_KEY"),
    "api_base": "https://your-resource.openai.azure.com/",
    "api_version": "2024-02-01",
    "deployment_name": "gpt-4-deployment"
}
```

---

## Error Handling

### Common Exceptions

```python
from ahs_agentic.exceptions import (
    AHSException,
    ConfigurationError,
    VectorDBError,
    ConflictDetectionError
)

try:
    agent = HyperGraphAgent(invalid_config)
except ConfigurationError as e:
    print(f"Configuration error: {e}")

try:
    result = await agent.resolve_conflict(...)
except ConflictDetectionError as e:
    print(f"Conflict detection failed: {e}")
```

---

## Performance Tuning

### Optimization Tips

1. **Enable Tier 2 Caching**
   ```python
   agent = HyperGraphAgent(
       tier2_cache_config={"provider": "redis", ...}
   )
   ```

2. **Adjust Skeptic Threshold**
   ```python
   # Lower threshold = fewer conflicts detected = faster
   agent = HyperGraphAgent(skeptic_threshold=0.80)
   ```

3. **Limit Parallel Hops**
   ```python
   retriever = SpeculativeRetriever(max_parallel_hops=3)
   ```

4. **Use Smaller Embeddings**
   ```python
   vector_db_config = {"dimension": 768}  # vs 1536
   ```

---

## Migration Guide

### From LangChain

```python
# LangChain
from langchain.vectorstores import Qdrant
from langchain.chains import RetrievalQA

qa = RetrievalQA.from_chain_type(...)
result = qa.run(query)

# AHS Agentic
from ahs_agentic import HyperGraphAgent

agent = HyperGraphAgent()
result = await agent.query(question=query)
```

---

## Next Steps

- **[Getting Started Guide](getting-started.md)** - Build your first agent
- **[Architecture](../ARCHITECTURE.md)** - Deep technical dive
- **[Examples](../examples/)** - Real-world implementations

---

[← Back to Documentation](index.md)
