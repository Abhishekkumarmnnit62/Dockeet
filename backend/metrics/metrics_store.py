import sqlite3


class MetricsStore:

    def __init__(self):
        self.conn = sqlite3.connect(
            "metrics.db",
            check_same_thread=False
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latency REAL,
                success INTEGER,
                has_citation INTEGER,
                prompt_tokens INTEGER,
                completion_tokens INTEGER,
                total_tokens INTEGER,
                request_cost REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def log_request(
        self,
        latency,
        success,
        has_citation,
        prompt_tokens,
        completion_tokens,
        total_tokens,
        request_cost
    ):
        self.cursor.execute(
            """
            INSERT INTO requests
            (
                latency,
                success,
                has_citation,
                prompt_tokens,
                completion_tokens,
                total_tokens,
                request_cost
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                latency,
                success,
                has_citation,
                prompt_tokens,
                completion_tokens,
                total_tokens,
                request_cost
            )
        )
        self.conn.commit()
    def reset(self):
        self.cursor.execute(
            """
            DELETE FROM requests
            """
        )
        self.conn.commit()