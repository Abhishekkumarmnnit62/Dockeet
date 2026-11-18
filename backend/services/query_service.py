
import time

from backend.core.retrieval_dependencies import (
    hybrid_searcher,
    reranker
)

from backend.core.dependencies import (
    groq_client
)

from backend.observability.langfuse_client import (
    langfuse
)
from backend.metrics.metrics_service import (
    metrics_service
)


class QueryService:

    def __init__(self):
        self.searcher = hybrid_searcher
        self.reranker = reranker

    def ask(
        self,
        question,
        document_name,
        user_id=None,
        session_id=None,
    ):

        start_time = time.time()

        with langfuse.start_as_current_observation(
            as_type="span",
            name="rag-query",
            input={
                "question": question,
                "document": document_name
            }
        ) as trace:

            try:
                # =====================
                # Retrieval
                # =====================

                with langfuse.start_as_current_observation(
                    as_type="span",
                    name="retrieval",
                    input={
                        "question": question,
                        "document_name": document_name,
                        "top_k": 10
                    }
                ) as retrieval_span:

                    retrieved_chunks = (
                        self.searcher.search(
                            question,
                            document_name,
                            top_k=10
                        )
                    )

                    retrieval_span.update(
                        output={
                            "retrieved_chunks": len(retrieved_chunks)
                        },
                        metadata={
                            "chunks": [
                                {
                                    "document": chunk["document_name"],
                                    "page": chunk["page"] + 1,
                                    "preview": chunk["content"][:200]
                                }
                                for chunk in retrieved_chunks[:5]
                            ]
                        }
                    )

                # =====================
                # Reranker
                # =====================

                with langfuse.start_as_current_observation(
                    as_type="span",
                    name="reranker",
                    input={
                        "question": question,
                        "candidate_chunks": len(retrieved_chunks),
                        "top_k": 5
                    }
                ) as reranker_span:

                    # Save original retrieval order
                    retrieval_order = [
                        {
                            "rank": idx + 1,
                            "document": chunk["document_name"],
                            "page": chunk["page"] + 1
                        }
                        for idx, chunk in enumerate(retrieved_chunks)
                    ]

                    reranked_chunks = (
                        self.reranker.rerank(
                            question,
                            retrieved_chunks,
                            top_k=5
                        )
                    )

                    # Save reranked order
                    reranked_order = [
                        {
                            "rank": idx + 1,
                            "document": chunk["document_name"],
                            "page": chunk["page"] + 1
                        }
                        for idx, chunk in enumerate(reranked_chunks)
                    ]

                    reranker_span.update(
                        output={
                            "selected_chunks": len(reranked_chunks)
                        },
                        metadata={
                            "before_reranking": retrieval_order,
                            "after_reranking": reranked_order,
                            "reranked_results": [
                                {
                                    "document": chunk["document_name"],
                                    "page": chunk["page"] + 1,
                                    "preview": chunk["content"][:200]
                                }
                                for chunk in reranked_chunks
                            ]
                        }
                    )

                # =====================
                # Context Building
                # =====================

                context = "\n\n".join(
                    [
                        chunk["content"]
                        for chunk in reranked_chunks
                    ]
                )

                prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
say:
"I could not find the answer in the document."

Context:
{context}

Question:
{question}
"""

                # =====================
                # Generation
                # =====================

                with langfuse.start_as_current_observation(
                    as_type="generation",
                    name="groq-generation",
                    model="llama-3.3-70b-versatile",
                    input=prompt,
                ) as generation_span:

                    answer = groq_client.generate(prompt)

                    generation_span.update(
                        output=answer,
                        usage={
                            "input": groq_client.last_prompt_tokens,
                            "output": groq_client.last_completion_tokens,
                            "total": groq_client.last_total_tokens
                        }
                    )

                # =====================
                # Sources
                # =====================

                sources = []
                seen = set()

                for chunk in reranked_chunks:
                    source = (
                        chunk["document_name"],
                        chunk["page"]
                    )

                    if source not in seen:
                        seen.add(source)
                        sources.append(
                            {
                                "document": chunk["document_name"],
                                "page": chunk["page"] + 1
                            }
                        )

                # =====================
                # Trace Metadata
                # =====================

                latency = round(
                    time.time() - start_time,
                    3
                )

                request_cost = (
                    (
                        groq_client.last_prompt_tokens
                        / 1_000_000
                    ) * 0.59
                ) + (
                    (
                        groq_client.last_completion_tokens
                        / 1_000_000
                    ) * 0.79
                )

                metrics_service.record_request(
                    latency=latency,
                    success=True,
                    has_citation=len(sources) > 0,
                    prompt_tokens=groq_client.last_prompt_tokens,
                    completion_tokens=groq_client.last_completion_tokens,
                    total_tokens=groq_client.last_total_tokens,
                    request_cost=request_cost
                )

                trace.update(
                    output=answer,
                    metadata={
                        "latency_seconds": latency,
                        "retrieved_chunks": len(retrieved_chunks),
                        "reranked_chunks": len(reranked_chunks),
                        "sources": sources
                    }
                )

                return {
                    "answer": answer,
                    "sources": sources
                }

            except Exception as exc:

                metrics_service.record_request(
                    latency=0,
                    success=False,
                    has_citation=False,
                    prompt_tokens=0,
                    completion_tokens=0,
                    total_tokens=0,
                    request_cost=0
                )

                trace.update(
                    level="ERROR",
                    status_message=str(exc)
                )

                raise

            finally:
                langfuse.flush()

