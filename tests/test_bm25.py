from backend.retrieval.bm25_search import (
    BM25Searcher
)

searcher = BM25Searcher()

results = searcher.search(
    "NLP",
    "Generative AI_ A Beginner's Guide.pdf"
)

print(results[:2])