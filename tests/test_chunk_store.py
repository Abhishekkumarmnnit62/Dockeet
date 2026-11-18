from backend.core.dependencies import (
    chunk_store
)

print(
    "Stored Chunks:",
    chunk_store.count()
)

print(
    "Documents:",
    chunk_store.list_documents()
)