from backend.retrieval.hybrid_search import (
    HybridSearcher
)

from backend.retrieval.reranker import (
    Reranker
)


searcher = HybridSearcher()

reranker = Reranker()

query = (
    "How is NLP used in Generative AI?"
)

results = searcher.search(
    query,
    "Generative AI_ A Beginner's Guide.pdf",
    top_k=10
)

reranked = (
    reranker.rerank(
        query,
        results,
        top_k=5
    )
)

print()

for i, chunk in enumerate(
    reranked,
    start=1
):

    print(
        f"Result {i}"
    )

    print(
        "-" * 40
    )

    print(
        f"Page: {chunk['page'] + 1}"
    )

    print()

    print(
        chunk["content"][:300]
    )

    print()