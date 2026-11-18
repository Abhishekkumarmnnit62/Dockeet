import chromadb
import uuid


class ChromaManager:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="rag_collection"
            )
        )

    def add_documents(
        self,
        chunks,
        embeddings,
        ids
    ):

        self.collection.add(
            documents=[
                chunk.page_content
                for chunk in chunks
            ],

            embeddings=embeddings.tolist(),

            metadatas=[
                chunk.metadata
                for chunk in chunks
            ],

            ids=ids
        )

    def count(self):

        return self.collection.count()

    def query(
        self,
        query_embedding,
        document_name,
        n_results=5
    ):
        if document_name == "all":
            results = self.collection.query(
                query_embeddings=[
                    query_embedding.tolist()
                ],
                n_results=n_results
            )

       

        else:
            results = self.collection.query(
                query_embeddings=[
                    query_embedding.tolist()
                ],
                where={
                    "document_name":
                    document_name
                },
                n_results=n_results
        )

        return results

    def peek(
        self,
        limit=3
    ):

        return self.collection.peek(
            limit=limit
        )

    def list_documents(self):

        data = self.collection.get(
            include=["metadatas"]
        )

        documents = set()

        for meta in data["metadatas"]:

            if (
                meta is not None
                and "document_name" in meta
            ):

                documents.add(
                    meta["document_name"]
                )

        return sorted(
            list(documents)
        )

    def delete_document(
        self,
        document_name
    ):

        data = self.collection.get()

        ids_to_delete = []

        for i, meta in enumerate(
            data["metadatas"]
        ):

            if (
                meta is not None
                and meta.get(
                    "document_name"
                ) == document_name
            ):

                ids_to_delete.append(
                    data["ids"][i]
                )

        if ids_to_delete:

            self.collection.delete(
                ids=ids_to_delete
            )

        return len(
            ids_to_delete
        )