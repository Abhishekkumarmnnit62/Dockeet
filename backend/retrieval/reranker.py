from sentence_transformers import (
    CrossEncoder
)


class Reranker:

    _model = None

    def __init__(self):

        if Reranker._model is None:

            print(
                "Loading reranker..."
            )

            Reranker._model = (
                CrossEncoder(
                    "cross-encoder/ms-marco-MiniLM-L-6-v2"
                )
            )

            print(
                "Reranker loaded!"
            )

        self.model = (
            Reranker._model
        )

    def rerank(
        self,
        query,
        chunks,
        top_k=5
    ):

        pairs = [
            (
                query,
                chunk["content"]
            )
            for chunk in chunks
        ]

        scores = (
            self.model.predict(
                pairs
            )
        )

        ranked = sorted(
            zip(
                chunks,
                scores
            ),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            item[0]
            for item in ranked[:top_k]
        ]