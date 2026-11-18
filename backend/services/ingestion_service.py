from backend.ingestion.loader import load_pdf
from backend.ingestion.chunker import chunk_documents

from backend.core.dependencies import (
    embedder,
    db,
    chunk_store
)
import uuid


class IngestionService:

    def ingest_pdf(
        self,
        pdf_path
    ):

        documents = load_pdf(
            pdf_path
        )

        document_name = (
            pdf_path.split("/")[-1]
            .split("\\")[-1]
        )

        chunks = chunk_documents(
            documents
        )
        ids = [
            str(uuid.uuid4())
            for _ in chunks
        ]

        for chunk in chunks:

            chunk.metadata[
                "document_name"
            ] = document_name

        embeddings = (
            embedder.embed_documents(
                chunks
            )
        )

        chunk_store.add_chunks(
            chunks,
            ids
        )

        db.add_documents(
            chunks,
            embeddings,
            ids
        )

        return {
            "document_name":
            document_name,

            "pages":
            len(documents),

            "chunks":
            len(chunks)
        }