from backend.retrieval.hybrid_search import (
    HybridSearcher
)

searcher = HybridSearcher()

results = searcher.search(
    "NLP",
    "Generative AI_ A Beginner's Guide.pdf"
)

print()

print(
    "Results:",
    len(results)
)

print()

for i, result in enumerate(
    results,
    start=1
):

    print(
        f"Result {i}"
    )

    print(
        "-" * 40
    )

    print(
        f"Page: {result['page'] + 1}"
    )

    print()

    print(
        result["content"][:300]
    )

    print()