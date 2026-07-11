"""Orchestrates explicit state hand-offs; no external side effect occurs without approval."""

from agents.content_agent import ContentAgent
from agents.review_agent import ReviewAgent
from agents.publisher_agent import PublisherAgent
from agents.analytics_agent import AnalyticsAgent
from agents.optimization_agent import OptimizationAgent


class PlannerAgent:
    def __init__(self):
        self.content = ContentAgent()
        self.review = ReviewAgent()
        self.publisher = PublisherAgent(dry_run=True)
        self.analytics = AnalyticsAgent()
        self.optimizer = OptimizationAgent()

    def run(self, approved: bool = False) -> dict:
        asset = self.content.generate_post()
        review = self.review.review(asset)
        publish = self.publisher.publish(asset, approved=approved) if review["passed"] and approved else {"mode": "not_published", "reason": "Awaiting explicit human approval"}
        analytics = self.analytics.analyze()
        return {"asset": asset, "review": review, "publish": publish, "analytics": analytics, "next_batch": self.optimizer.optimize(analytics)}
