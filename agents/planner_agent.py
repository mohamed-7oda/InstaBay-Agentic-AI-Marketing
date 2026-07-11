from agents.content_agent import ContentAgent
from agents.review_agent import ReviewAgent
from agents.publisher_agent import PublisherAgent
from agents.analytics_agent import AnalyticsAgent
from agents.optimization_agent import OptimizationAgent


class PlannerAgent:

    def __init__(self):
        self.content = ContentAgent()
        self.review = ReviewAgent()
        self.publisher = PublisherAgent()
        self.analytics = AnalyticsAgent()
        self.optimizer = OptimizationAgent()

    def run(self):

        # Generate Content
        post = self.content.generate_post()

        # Human Review
        approved = self.review.review(post)

        if approved:
            self.publisher.publish(post)

            report = self.analytics.analyze()

            self.optimizer.optimize(report)

        else:
            print("\nPost Rejected.")