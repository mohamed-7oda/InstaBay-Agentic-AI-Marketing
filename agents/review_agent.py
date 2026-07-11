class ReviewAgent:

    def review(self, post):

        print("\n" + "=" * 60)
        print("Generated Post")
        print("=" * 60)

        print(post)

        print("=" * 60)

        choice = input("\nApprove this post? (y/n): ")

        return choice.lower() == "y"