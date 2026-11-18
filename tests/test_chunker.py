from ingestion.loader import load_pdf
from ingestion.chunker import chunk_documents


pdf_path = (
    "data/raw_docs/Generative AI_ A Beginner's Guide.pdf"
)

documents = load_pdf(pdf_path)

chunks = chunk_documents(documents)

print(f"Pages: {len(documents)}")

print(f"Chunks: {len(chunks)}")

print("\nFirst Chunk:\n")

print(chunks[0].page_content[:500])

print("\nMetadata:")

print(chunks[0].metadata)