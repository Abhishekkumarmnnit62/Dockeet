from backend.core.dependencies import (
    embedder,
    db
)


class VectorSearcher:

    def search(
        self,
        query,
        document_name,
        top_k=5
    ):

        query_embedding = (
            embedder.embed_query(
                query
            )
        )

        results = db.query(
            query_embedding,
            document_name=document_name,
            n_results=top_k
        )  

        return results