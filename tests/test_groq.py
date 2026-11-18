from llm.groq_client import (
    GroqClient
)

llm = GroqClient()

response = llm.generate(
    "What is NLP?"
)

print(response)