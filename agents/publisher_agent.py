"""Safe Meta Graph API adapter: dry-run by default, live publishing only after approval."""

import os
import time
from pathlib import Path
import requests


ROOT = Path(__file__).resolve().parents[1]


class PublisherAgent:
    def __init__(self, dry_run: bool = True, api_version: str = "v22.0"):
        self.dry_run = dry_run
        self.api_version = api_version
        self.base_url = f"https://graph.facebook.com/{api_version}"

    @staticmethod
    def _caption(asset: dict) -> str:
        return "\n\n".join([asset["caption_en"], asset["caption_ar"], " ".join(asset["hashtags"])])

    def build_publish_plan(self, asset: dict) -> dict:
        media_type = "REELS" if asset["content_type"].lower() == "reel" else "IMAGE"
        return {
            "create_container": {
                "endpoint": "/{ig_user_id}/media",
                "method": "POST",
                "payload": {"media_type": media_type, "caption": self._caption(asset), "media_url": "<public HTTPS media URL>"},
            },
            "poll_container": {"endpoint": "/{container_id}?fields=status_code,status", "until": "FINISHED"},
            "publish": {"endpoint": "/{ig_user_id}/media_publish", "method": "POST", "payload": {"creation_id": "{container_id}"}},
        }

    def publish(self, asset: dict, approved: bool, media_url: str | None = None) -> dict:
        if not approved:
            raise PermissionError("Human approval is required before any publishing action.")
        plan = self.build_publish_plan(asset)
        if self.dry_run:
            return {"mode": "dry_run", "status": "queued_for_human_confirmed_publish", "plan": plan}
        token, ig_user_id = os.getenv("META_ACCESS_TOKEN"), os.getenv("IG_USER_ID")
        if not token or not ig_user_id or not media_url:
            raise ValueError("Live mode requires META_ACCESS_TOKEN, IG_USER_ID, and a public media_url.")
        params = {"caption": self._caption(asset), "access_token": token}
        if asset["content_type"].lower() == "reel":
            params.update({"media_type": "REELS", "video_url": media_url, "share_to_feed": "true"})
        else:
            params["image_url"] = media_url
        created = requests.post(f"{self.base_url}/{ig_user_id}/media", data=params, timeout=30)
        created.raise_for_status()
        container_id = created.json()["id"]
        for _ in range(12):
            status = requests.get(f"{self.base_url}/{container_id}", params={"fields": "status_code,status", "access_token": token}, timeout=30)
            status.raise_for_status()
            if status.json().get("status_code") == "FINISHED":
                break
            time.sleep(5)
        else:
            raise TimeoutError("Meta container did not reach FINISHED within 60 seconds.")
        published = requests.post(f"{self.base_url}/{ig_user_id}/media_publish", data={"creation_id": container_id, "access_token": token}, timeout=30)
        published.raise_for_status()
        return {"mode": "live", "status": "published", "media_id": published.json()["id"], "plan": plan}
