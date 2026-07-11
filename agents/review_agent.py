"""Deterministic quality gate. Human approval remains mandatory for publishing."""

import re
from agents.brand_agent import BrandAgent


class ReviewAgent:
    def __init__(self):
        self.brand = BrandAgent().get_brand()

    def review(self, asset: dict) -> dict:
        required = ["caption_en", "caption_ar", "cta_en", "cta_ar", "hashtags", "visual_brief"]
        missing = [field for field in required if not asset.get(field)]
        arabic_chars = len(re.findall(r"[\u0600-\u06FF]", asset.get("caption_ar", "")))
        hashtag_ok = 3 <= len(asset.get("hashtags", [])) <= 10
        reel_ok = asset.get("content_type", "").lower() != "reel" or bool(asset.get("reel_storyboard"))
        brand_terms = ["red sea", "instabay", "إنستا", "البحر الأحمر"]
        corpus = f"{asset.get('caption_en', '')} {asset.get('caption_ar', '')}".lower()
        brand_score = 5 if sum(term in corpus for term in brand_terms) >= 2 else 4
        arabic_score = 5 if arabic_chars >= 60 and asset.get("cta_ar") else 3
        passed = not missing and arabic_chars >= 60 and hashtag_ok and reel_ok
        return {
            "passed": passed,
            "brand_consistency_score": brand_score,
            "arabic_quality_score": arabic_score,
            "checks": {
                "required_fields": not missing,
                "arabic_script_present": arabic_chars >= 60,
                "hashtag_count_valid": hashtag_ok,
                "reel_has_storyboard": reel_ok,
            },
            "notes": [] if passed else [f"Fix: {', '.join(missing) or 'Arabic/hashtag/Reel checks'}"],
            "human_approval_required": True,
        }
