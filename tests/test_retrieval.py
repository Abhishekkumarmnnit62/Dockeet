from retrieval.vector_search import (
    VectorSearcher
)

searcher = VectorSearcher()

query = input(
    "Ask a question: "
)

results = searcher.search(
    query
)

print("\nResults")
print("=" * 60)

for i, doc in enumerate(
    results["documents"][0]
):

    print(
        f"\nResult {i+1}"
    )

    print("-" * 40)

    print(doc[:500])