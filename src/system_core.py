import logging
import os

# Enforce single-threaded execution for heavy libraries to prevent idle resource grabbing
# This must be done before importing numpy, torch, etc.
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["TORCH_NUM_THREADS"] = "1"

import uuid
from typing import Dict, Any, List

from src.core.ingestion.ingestor import Ingestor
from src.core.preprocess.preprocessor import Preprocessor
from src.core.analysis.analyzer import Analyzer
from src.models.embeddings.pinecone_handler import PineconeHandler

logger = logging.getLogger(__name__)

class Core:
    """
    Core orchestration class for the Transcendence T1 system.
    Handles the pipeline: Planning -> Ingestion -> Preprocess -> Storage -> Analysis.
    """

    def __init__(self):
        """
        Initialize the Core system and its components.
        """
        logger.info("Initializing Core system...")
        
        # Initialize components
        self.ingestor = Ingestor()
        self.preprocessor = Preprocessor()
        self.analyzer = Analyzer()
        
        # Initialize Vector DB
        self.vector_db = PineconeHandler(index_name="abc", namespace="intelligence")
        
        logger.info("Core system initialized.")

    def run_pipeline(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the full data processing pipeline.

        Args:
            input_data (Dict[str, Any]): The input data containing 'query' or 'source'.

        Returns:
            Dict[str, Any]: The results of the analysis.
        """
        logger.info("Starting pipeline execution...")
        
        query = input_data.get("query")
        sources = input_data.get("source")
        
        if not query and not sources:
            return {"status": "error", "message": "No query or sources provided."}

        # 1. Planning / Source Discovery
        if not sources and query:
            logger.info(f"Generating research plan for: {query}")
            sources = self.analyzer.generate_plan(query)
            if not sources:
                return {"status": "error", "message": "Could not generate valid sources."}
        elif isinstance(sources, str):
            sources = [sources]

        # 2. Ingestion
        logger.info(f"Ingesting from {len(sources)} sources...")
        raw_items = self.ingestor.fetch_osint(sources)
        
        processed_items = []
        summaries = []
        vectors_to_upsert = []

        # 3. Preprocessing & Storage Loop (Parallelized)
        import asyncio

        async def process_item(item):
            if item.get("status") == "success":
                content = item.get("content", "")
                url = item.get("url")
                
                # Preprocess (CPU bound, fast)
                clean_content = self.preprocessor.clean_text(content)
                
                if clean_content:
                    # Generate individual summary (I/O bound - LLM Call)
                    # We run this in a thread executor to avoid blocking the loop if it's synchronous requests
                    loop = asyncio.get_event_loop()
                    try:
                        summary = await loop.run_in_executor(None, self.analyzer.generate_summary, clean_content[:15000])
                    except Exception as e:
                        logger.error(f"Summary generation failed for {url}: {e}")
                        summary = "Error generating summary."

                    doc_id = str(uuid.uuid4())
                    return {
                        "valid": True,
                        "vector_tuple": (doc_id, clean_content, {"url": url, "query": query}),
                        "summary_text": f"Source: {url}\n{summary}",
                        "result_item": {"url": url, "summary": summary}
                    }
            return {"valid": False}

        # Create or retrieve event loop to run the tasks
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Run processing tasks concurrently
        task_list = [process_item(item) for item in raw_items]
        if task_list:
            if loop.is_running():
                 # Should not happen in this sync wrapper context, but for safety
                 logger.warning("Event loop already running, executing sequentially as fallback")
                 results = [loop.run_until_complete(t) for t in task_list] 
            else:
                 results = loop.run_until_complete(asyncio.gather(*task_list))
        else:
            results = []

        for res in results:
            if res["valid"]:
                vectors_to_upsert.append(res["vector_tuple"])
                summaries.append(res["summary_text"])
                processed_items.append(res["result_item"])

        # 4. Storage (Batch Upsert)
        if vectors_to_upsert:
            self.vector_db.upsert_vectors(vectors_to_upsert)

        # 5. Analysis (Executive Report)
        executive_report = "No data gathered."
        if summaries:
            executive_report = self.analyzer.generate_executive_report(summaries, query or "Provided Sources")

        logger.info("Pipeline execution completed.")
        
        return {
            "status": "completed", 
            "sources_processed": len(processed_items),
            "executive_report": executive_report,
            "detailed_results": processed_items
        }

if __name__ == "__main__":
    # Basic test
    logging.basicConfig(level=logging.INFO)
    core = Core()
    # Example usage
    # result = core.run_pipeline({"query": "latest advancements in solid state batteries 2024"})
    # print(result['executive_report'])

