class OptimizationAgent:

    def optimize(self, analytics):

        print("\n" + "=" * 60)
        print("Optimization Report")
        print("=" * 60)

        if analytics["best_post"] == "Reel":
            print("✓ Reels achieved the highest engagement.")
            print("Recommendation: Increase Reel content from 2 to 4 posts per week.\n")

        if analytics["average_likes"] > 250:
            print("✓ Current engagement is strong.")
            print("Recommendation: Continue using luxury and beach-focused content.\n")
        else:
            print("✓ Engagement is below target.")
            print("Recommendation: Test new content styles and posting times.")