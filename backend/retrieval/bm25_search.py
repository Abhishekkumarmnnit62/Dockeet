from rank_bm25 import BM25Okapi

from backend.core.dependencies import (
    chunk_store
)


class BM25Searcher:

    def search(
        self,
        query,
        document_name,
        top_k=5
    ):

        rows = (
            chunk_store.get_chunks_by_document(
                document_name
            )
        )

        if not rows:

            return []

        chunk_data = []

        tokenized_docs = []

        for row in rows:
            chunk_id = row[0]
            document_name = row[1]
            page = row[2]
            content = row[3]

            chunk_data.append(
                {
                    "id": chunk_id,
                    "document_name": document_name,
                    "page": page,
                    "content": content
                }
            )

            tokenized_docs.append(
                content.lower().split()
            )

        bm25 = BM25Okapi(
            tokenized_docs
        )

        scores = bm25.get_scores(
            query.lower().split()
        )

        ranked = sorted(
            zip(chunk_data, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            item[0]
            for item in ranked[:top_k]
        ]