from backend.services.query_service import (
    QueryService
)

rag = QueryService()

document_name = input(
    "Document name: "
)

question = input(
    "Ask a question: "
)

result = rag.ask(
    question,
    document_name
)

print("\nAnswer")
print("=" * 60)

print(
    result["answer"]
)

print("\nSources")
print("=" * 60)

for source in result["sources"]:

    print(source)