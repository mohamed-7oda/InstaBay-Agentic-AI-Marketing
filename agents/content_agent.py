"""Creates schema-shaped bilingual assets. It works without a paid model key."""

from datetime import date
from agents.brand_agent import BrandAgent


class ContentAgent:
    ARABIC_TOPIC_MAP = {
        "sunset by the red sea": "غروب على البحر الأحمر",
        "sunrise swim": "سباحة عند الشروق",
        "spa ritual": "طقوس السبا",
        "golden-hour dinner": "عشاء وقت الغروب",
        "snorkelling": "مغامرة سنوركلينغ",
        "family escape": "عطلة عائلية",
        "poolside reset": "استراحة بجانب المسبح",
    }

    def __init__(self):
        self.brand = BrandAgent().get_brand()

    def generate_post(
        self,
        topic: str = "sunset by the Red Sea",
        pillar: str = "Beach & Nature",
        content_type: str = "Reel",
        optimized: bool = False,
    ) -> dict:
        """Return a publishable, reviewable asset; no network/model call is required."""
        topic_ar = self.ARABIC_TOPIC_MAP.get(topic.strip().lower(), "لحظة هادئة على البحر الأحمر")
        hook_en = "Save this for your next Red Sea escape."
        hook_ar = "احفظوا هذا المنشور لعطلتكم القادمة على البحر الأحمر."
        caption_en = (
            f"{hook_en}\n\n{topic.title()} at InstaBay is the pause your week has been asking for: "
            "clear water, an unhurried morning, and a little room to breathe. "
            "Which moment would you choose first?"
        )
        caption_ar = (
            f"{hook_ar}\n\nفي إنستا باي، {topic_ar} ليست مجرد لقطة جميلة؛ إنها مساحة للهدوء: "
            "مياه صافية، صباح على مهل، ووقت لكم. أي لحظة ستختارون أولاً؟"
        )
        hashtags = self.brand["hashtags"][:5] + ["#RedSeaEscape", "#HurghadaHotels"]
        asset = {
            "id": f"{date.today().isoformat()}-{pillar.lower().replace(' ', '-')}",
            "status": "draft",
            "content_type": content_type,
            "pillar": pillar,
            "topic": topic,
            "topic_ar": topic_ar,
            "optimized": optimized,
            "caption_en": caption_en,
            "caption_ar": caption_ar,
            "cta_en": "Save this post and plan your InstaBay stay.",
            "cta_ar": "احفظوا المنشور وخططوا لإقامتكم في إنستا باي.",
            "hashtags": hashtags,
            "visual_brief": (
                "9:16 vertical, natural turquoise water and warm sunset light; "
                "relaxed-luxury, candid guests, no text baked into the image."
            ),
            "generation_mode": "deterministic-template",
        }
        if content_type.lower() == "reel":
            asset["reel_storyboard"] = [
                {"seconds": "0-2", "visual": "Turquoise-water reveal", "on_screen": "Your Red Sea reset / استراحة على البحر الأحمر"},
                {"seconds": "3-8", "visual": "Guest opens balcony doors", "on_screen": "Slow mornings / صباح على مهل"},
                {"seconds": "9-16", "visual": "Snorkelling then poolside drink", "on_screen": "Dive in / انطلقوا"},
                {"seconds": "17-24", "visual": "Sunset table for two", "on_screen": "Save your escape / احفظوا لحظتكم"},
            ]
            asset["reel_audio_direction"] = "Warm, upbeat instrumental; subtle sea ambience; 24 seconds."
        return asset
