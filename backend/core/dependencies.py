from backend.ingestion.embedder import Embedder
from backend.database.chroma_client import ChromaManager
from backend.database.chunk_store import (
    ChunkStore
)
from backend.llm.groq_client import GroqClient


embedder = Embedder()

db = ChromaManager()

chunk_store = ChunkStore()

groq_client = GroqClient()