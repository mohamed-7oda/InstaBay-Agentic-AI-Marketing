"""Offline, reproducible analytics for the synthetic challenge data."""

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


class AnalyticsAgent:
    def __init__(self, path: Path | None = None):
        self.path = path or ROOT / "data" / "engagement.csv"
        self.data = pd.read_csv(self.path)

    @staticmethod
    def weighted_engagement_rate(frame: pd.DataFrame) -> pd.Series:
        return ((frame["likes"] + frame["comments"] + 2 * frame["saves"] + 2 * frame["shares"]) / frame["reach"] * 100)

    def analyze(self) -> dict:
        data = self.data.copy()
        data["weighted_engagement_rate"] = self.weighted_engagement_rate(data)
        by_batch = data.groupby("batch")["weighted_engagement_rate"].mean().to_dict()
        before, after = by_batch["before"], by_batch["after"]
        top = data.loc[data["weighted_engagement_rate"].idxmax()]
        return {
            "average_likes": float(data["likes"].mean()),
            "average_reach": float(data["reach"].mean()),
            "best_post": top["post_id"],
            "best_format": top["content_type"],
            "by_batch": {key: round(value, 2) for key, value in by_batch.items()},
            "uplift_pct": round((after - before) / before * 100, 1),
            "top_pillar": data.groupby("pillar")["weighted_engagement_rate"].mean().idxmax(),
            "records": data.sort_values(["batch", "weighted_engagement_rate"], ascending=[True, False]).to_dict("records"),
        }
