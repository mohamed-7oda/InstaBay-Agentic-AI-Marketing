class OptimizationAgent:
    def suggest(self, analytics: dict) -> list[tuple[str, str]]:
        return [
            ("success", f"Use more {analytics['best_format']}s: the strongest asset was {analytics['best_post']}"),
            ("info", f"Prioritize the {analytics['top_pillar']} pillar in the next batch."),
            ("info", "Keep a bilingual hook in the first line and a save-oriented CTA."),
            ("warning", "This is an offline synthetic-data recommendation; validate it with real Insights before scaling."),
        ]

    def optimize(self, analytics: dict) -> dict:
        return {
            "next_batch_mix": {"Reel": 3, "Carousel": 2, "Image": 1},
            "priority_pillar": analytics["top_pillar"],
            "posting_window": "20:00 Africa/Cairo",
            "reason": f"Synthetic weighted engagement rate increased {analytics['uplift_pct']}% after the first iteration.",
        }
