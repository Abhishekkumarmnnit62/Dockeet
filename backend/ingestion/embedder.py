from sentence_transformers import SentenceTransformer


class Embedder:

    _model = None

    def __init__(
        self,
        model_name="BAAI/bge-small-en-v1.5"
    ):

        if Embedder._model is None:

            print(
                "Loading embedding model..."
            )

            Embedder._model = (
                SentenceTransformer(
                    model_name
                )
            )

            print(
                "Model loaded successfully!"
            )

        self.model = (
            Embedder._model
        )

    def embed_documents(
        self,
        chunks
    ):

        texts = [
            chunk.page_content
            for chunk in chunks
        ]

        embeddings = (
            self.model.encode(
                texts,
                show_progress_bar=True
            )
        )

        return embeddings

    def embed_query(
        self,
        query
    ):

        return self.model.encode(
            query
        )