import pandas as pd


class AnalyticsAgent:

    def __init__(self):
        self.data = pd.read_csv("data/engagement.csv")

    def analyze(self):

        best_post = self.data.loc[self.data["Likes"].idxmax()]

        average_likes = self.data["Likes"].mean()
        average_comments = self.data["Comments"].mean()
        average_reach = self.data["Reach"].mean()

        print("\n" + "=" * 60)
        print("Analytics Report")
        print("=" * 60)

        print(f"Average Likes: {average_likes:.0f}")
        print(f"Average Comments: {average_comments:.0f}")
        print(f"Average Reach: {average_reach:.0f}")

        print("\nBest Performing Content")
        print(f"Post Type: {best_post['Post']}")
        print(f"Likes: {best_post['Likes']}")
        print(f"Reach: {best_post['Reach']}")

        return {
            "average_likes": average_likes,
            "average_comments": average_comments,
            "average_reach": average_reach,
            "best_post": best_post["Post"]
        }