from backend.retrieval.vector_search import (
    VectorSearcher
)

from backend.retrieval.bm25_search import (
    BM25Searcher
)

from backend.retrieval.hybrid_search import (
    HybridSearcher
)

from backend.retrieval.reranker import (
    Reranker
)


class DebugService:

    def __init__(self):

        self.vector = VectorSearcher()

        self.bm25 = BM25Searcher()

        self.hybrid = HybridSearcher()

        self.reranker = Reranker()

    def debug(
        self,
        question,
        document_name
    ):

        vector_results = (
            self.vector.search(
                question,
                document_name,
                top_k=10
            )
        )

        bm25_results = (
            self.bm25.search(
                question,
                document_name,
                top_k=10
            )
        )

        hybrid_results = (
            self.hybrid.search(
                question,
                document_name,
                top_k=10
            )
        )

        reranked_results = (
            self.reranker.rerank(
                question,
                hybrid_results,
                top_k=5
            )
        )

        return {
            "vector_count":
            len(
                vector_results["documents"][0]
            ),

            "bm25_count":
            len(
                bm25_results
            ),

            "hybrid_count":
            len(
                hybrid_results
            ),

            "reranked_count":
            len(
                reranked_results
            ),

            "reranked_results":
            reranked_results
        }