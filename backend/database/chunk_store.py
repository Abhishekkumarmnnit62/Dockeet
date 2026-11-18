import sqlite3


class ChunkStore:

    def __init__(self):

        self.conn = sqlite3.connect(
            "chunk_store.db",
            check_same_thread=False
        )

        self.create_table()

    def create_table(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks (

                id TEXT PRIMARY KEY,

                document_name TEXT,

                page INTEGER,

                content TEXT

            )
            """
        )

        self.conn.commit()

    def add_chunks(
        self,
        chunks,
        ids
    ):

        cursor = self.conn.cursor()

        records = []

        for chunk, chunk_id in zip(
            chunks,
            ids
        ):

            records.append(
                (
                    chunk_id,

                    chunk.metadata.get(
                        "document_name",
                        "unknown"
                    ),

                    chunk.metadata.get(
                        "page",
                        0
                    ),

                    chunk.page_content
                )
            )

        cursor.executemany(
            """
            INSERT INTO chunks
            (
                id,
                document_name,
                page,
                content
            )
            VALUES (?, ?, ?, ?)
            """,
            records
        )

        self.conn.commit()

    def list_documents(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT DISTINCT
            document_name
            FROM chunks
            """
        )

        rows = cursor.fetchall()

        return [
            row[0]
            for row in rows
        ]

    def delete_document(
        self,
        document_name
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            DELETE FROM chunks
            WHERE document_name = ?
            """,
            (document_name,)
        )

        self.conn.commit()

    def document_exists(
        self,
        document_name
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM chunks
            WHERE document_name = ?
            """,
            (document_name,)
        )

        return (
            cursor.fetchone()[0]
            > 0
        )

    def get_document_count(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(
                DISTINCT document_name
            )
            FROM chunks
            """
        )

        return (
            cursor.fetchone()[0]
        )

    def count(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM chunks
            """
        )

        return (
            cursor.fetchone()[0]
        )

    def get_chunks_by_document(
        self,
        document_name
    ):

        cursor = self.conn.cursor()

        if document_name == "all":

            cursor.execute(
                """
                SELECT
                    id,
                    document_name,
                    page,
                    content
                FROM chunks
                """
            )

        else:

            cursor.execute(
                """
                SELECT
                    id,
                    document_name,
                    page,
                    content
                FROM chunks
                WHERE document_name = ?
                """,
                (document_name,)
            )

        rows = cursor.fetchall()

        return rows

    def close(self):

        self.conn.close()