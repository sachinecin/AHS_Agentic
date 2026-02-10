import pytest
import asyncio
from ahs_agentic.core.retrieval import SpeculativeRetriever


class TestSpeculativeRetriever:
    """Test suite for parallel-hop retrieval and concurrency limits."""
    
    @pytest.mark.asyncio
    async def test_parallel_hop_basic(self):
        """Test basic parallel query execution."""
        retriever = SpeculativeRetriever(max_parallel_hops=5)
        
        queries = ["query1", "query2", "query3"]
        results = await retriever.parallel_hop(queries)
        
        assert len(results) == 3
        assert all("query" in r for r in results)
    
    @pytest.mark.asyncio
    async def test_concurrency_limiting(self):
        """Verify that semaphore limits concurrent executions."""
        retriever = SpeculativeRetriever(max_parallel_hops=2)
        
        # Track concurrent executions
        concurrent_count = 0
        max_concurrent = 0
        
        async def monitored_search(query):
            nonlocal concurrent_count, max_concurrent
            async with retriever.semaphore:
                concurrent_count += 1
                max_concurrent = max(max_concurrent, concurrent_count)
                await asyncio.sleep(0.01)
                concurrent_count -= 1
                return {"query": query}
        
        queries = [f"query{i}" for i in range(10)]
        tasks = [monitored_search(q) for q in queries]
        await asyncio.gather(*tasks)
        
        assert max_concurrent <= 2, "Should never exceed max_parallel_hops"
    
    @pytest.mark.asyncio
    async def test_batch_with_backpressure(self):
        """Test batching strategy for high-volume scenarios."""
        retriever = SpeculativeRetriever(max_parallel_hops=3)
        
        queries = [f"query{i}" for i in range(25)]
        results = await retriever.batch_with_backpressure(queries, batch_size=5)
        
        assert len(results) == 25
        assert retriever.query_metrics["total_hops"] == 25
    
    @pytest.mark.asyncio
    async def test_empty_query_list(self):
        """Test handling of empty query list."""
        retriever = SpeculativeRetriever(max_parallel_hops=5)
        
        results = await retriever.parallel_hop([])
        
        assert results == []