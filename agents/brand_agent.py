"""Brand memory: the single source of truth used by every workflow stage."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BrandAgent:
    def __init__(self, path: Path | None = None):
        path = path or ROOT / "data" / "brand_rules.json"
        with path.open("r", encoding="utf-8") as file:
            self.brand = json.load(file)

    def get_brand(self) -> dict:
        return self.brand

    def get_prompt(self) -> str:
        """Compact grounding context for an optional external LLM."""
        return (
            f"Brand: {self.brand['brand_name']} ({self.brand['location']})\n"
            f"Voice: {self.brand['voice']}\n"
            f"Pillars: {', '.join(self.brand['content_pillars'])}\n"
            f"Visual direction: {self.brand['visual_direction']}\n"
            f"Audience: {', '.join(self.brand['target_audience'])}\n"
            f"Required languages: English and Arabic. Arabic must be original copy, "
            f"not a literal translation.\n"
            f"Hashtag system: {' '.join(self.brand['hashtags'])}"
        )
