
from backend.metrics.metrics_store import (
    MetricsStore
)

import numpy as np


class MetricsService:

    def __init__(self):
        self.store = MetricsStore()

    def record_request(
        self,
        latency,
        success,
        has_citation,
        prompt_tokens,
        completion_tokens,
        total_tokens,
        request_cost
    ):
        self.store.log_request(
            latency,
            success,
            has_citation,
            prompt_tokens,
            completion_tokens,
            total_tokens,
            request_cost
        )

    def get_metrics(self):
        cursor = self.store.cursor

        # =====================
        # Total Requests
        # =====================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM requests
            """
        )

        total_requests = cursor.fetchone()[0]

        # =====================
        # Failed Requests
        # =====================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM requests
            WHERE success = 0
            """
        )

        failed_requests = cursor.fetchone()[0]

        # =====================
        # Citation Count
        # =====================

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM requests
            WHERE has_citation = 1
            """
        )

        cited_requests = cursor.fetchone()[0]

        # =====================
        # Average Latency
        # =====================

        cursor.execute(
            """
            SELECT AVG(latency)
            FROM requests
            WHERE success = 1
            """
        )

        avg_latency = cursor.fetchone()[0] or 0

        # =====================
        # Defaults
        # =====================

        failure_rate = 0
        citation_rate = 0

        p50 = 0
        p90 = 0
        p99 = 0

        # =====================
        # Rates
        # =====================

        if total_requests > 0:
            failure_rate = round(
                (failed_requests / total_requests) * 100,
                2
            )

            citation_rate = round(
                (cited_requests / total_requests) * 100,
                2
            )

        # =====================
        # Percentiles
        # =====================

        cursor.execute(
            """
            SELECT latency
            FROM requests
            WHERE success = 1
            """
        )

        latencies = [
            row[0]
            for row in cursor.fetchall()
        ]

        if latencies:
            p50 = round(
                float(np.percentile(latencies, 50)),
                3
            )

            p90 = round(
                float(np.percentile(latencies, 90)),
                3
            )

            p99 = round(
                float(np.percentile(latencies, 99)),
                3
            )

        # =====================
        # Token Statistics
        # =====================
        # Note: I've fixed the execution order here so `fetchone()` grabs the token stats before the cursor executes the cost query.

        cursor.execute(
            """
            SELECT
                AVG(prompt_tokens),
                AVG(completion_tokens),
                AVG(total_tokens)
            FROM requests
            WHERE success = 1
            """
        )

        token_stats = cursor.fetchone() or (0, 0, 0)

        avg_prompt_tokens = round(token_stats[0] or 0, 2)
        avg_completion_tokens = round(token_stats[1] or 0, 2)
        avg_total_tokens = round(token_stats[2] or 0, 2)

        # =====================
        # Cost Statistics
        # =====================

        cursor.execute(
            """
            SELECT
                AVG(request_cost),
                SUM(request_cost)
            FROM requests
            WHERE success = 1
            """
        )

        cost_stats = cursor.fetchone() or (0, 0)

        avg_cost = round(cost_stats[0] or 0, 6)
        total_cost = round(cost_stats[1] or 0, 6)

        return {
            "requests": total_requests,
            "failure_rate": failure_rate,
            "citation_rate": citation_rate,
            "avg_latency": round(avg_latency, 3),
            "p50_latency": p50,
            "p90_latency": p90,
            "p99_latency": p99,
            "avg_prompt_tokens_per_request":
            avg_prompt_tokens,
            "avg_completion_tokens_per_request":
            avg_completion_tokens,
            "avg_total_tokens_per_request":
            avg_total_tokens,
            "avg_cost_per_request": avg_cost,
            "total_cost": total_cost,
        }
    def reset(self):
        self.store.reset()


metrics_service = MetricsService()

