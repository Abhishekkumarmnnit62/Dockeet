from ingestion.loader import load_pdf
from ingestion.chunker import chunk_documents
from ingestion.embedder import Embedder


pdf_path = (
    "data/raw_docs/Generative AI_ A Beginner's Guide.pdf"
)

documents = load_pdf(pdf_path)

chunks = chunk_documents(documents)

embedder = Embedder()

embeddings = embedder.embed_documents(
    chunks
)

print("\nResults")
print("-" * 50)

print(
    f"Documents: {len(documents)}"
)

print(
    f"Chunks: {len(chunks)}"
)

print(
    f"Embeddings: {len(embeddings)}"
)

print(
    f"Embedding Dimension: "
    f"{len(embeddings[0])}"
)
print(type(embeddings))
print(type(embeddings[0]))

print("\nFirst 10 values:")
print(embeddings[0][:10])