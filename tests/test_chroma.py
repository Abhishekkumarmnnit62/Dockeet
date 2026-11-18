from database.chroma_client import ChromaManager

db = ChromaManager()

print(
    f"Stored Chunks: {db.count()}"
)