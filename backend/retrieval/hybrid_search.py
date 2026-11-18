from backend.retrieval.vector_search import (
    VectorSearcher
)

from backend.retrieval.bm25_search import (
    BM25Searcher
)


class HybridSearcher:

    def __init__(self):

        self.vector_searcher = (
            VectorSearcher()
        )

        self.bm25_searcher = (
            BM25Searcher()
        )

    def search(
        self,
        query,
        document_name,
        top_k=5
    ):

        vector_results = (
            self.vector_searcher.search(
                query,
                document_name,
                top_k
            )
        )

        bm25_results = (
            self.bm25_searcher.search(
                query,
                document_name,
                top_k
            )
        )

        merged = []

        seen = set()

        # Chroma Results
        documents = (
            vector_results["documents"][0]
        )

        metadatas = (
            vector_results["metadatas"][0]
        )

        for doc, meta in zip(
            documents,
            metadatas
        ):

            chunk_key = (
                meta["page"],
                doc[:100]
            )

            if chunk_key not in seen:

                seen.add(
                    chunk_key
                )

                merged.append(
                    {
                        "content": doc,
                        "page": meta["page"],
                        "document_name": meta["document_name"]
                    }
                )

        # BM25 Results
        for result in bm25_results:

            chunk_key = (
                result["page"],
                result["content"][:100]
            )

            if chunk_key not in seen:

                seen.add(
                    chunk_key
                )

                merged.append(
                    {
                        "content":
                        result["content"],

                        "page":
                        result["page"],

                        "document_name": result["document_name"]
                    }
                )

        return merged[:top_k]