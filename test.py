"""Small offline acceptance test suite: `python test.py`."""

import unittest
from agents.analytics_agent import AnalyticsAgent
from agents.content_agent import ContentAgent
from agents.publisher_agent import PublisherAgent
from agents.review_agent import ReviewAgent


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.asset = ContentAgent().generate_post()

    def test_bilingual_reel_passes_quality_gate(self):
        result = ReviewAgent().review(self.asset)
        self.assertTrue(result["passed"])
        self.assertIn("reel_storyboard", self.asset)
        self.assertGreaterEqual(result["arabic_quality_score"], 4)
        self.assertNotIn("sunset by the red sea", self.asset["caption_ar"].lower())

    def test_publish_requires_approval_and_dry_run_has_plan(self):
        publisher = PublisherAgent(dry_run=True)
        with self.assertRaises(PermissionError):
            publisher.publish(self.asset, approved=False)
        result = publisher.publish(self.asset, approved=True)
        self.assertEqual(result["mode"], "dry_run")
        self.assertIn("create_container", result["plan"])

    def test_feedback_loop_has_positive_measured_uplift(self):
        report = AnalyticsAgent().analyze()
        self.assertGreater(report["uplift_pct"], 0)
        self.assertGreater(report["by_batch"]["after"], report["by_batch"]["before"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
