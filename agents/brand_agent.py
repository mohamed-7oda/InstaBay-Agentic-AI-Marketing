import json


class BrandAgent:

    def __init__(self):
        with open("data/brand_rules.json", "r", encoding="utf-8") as file:
            self.brand = json.load(file)

    def get_brand(self):
        return self.brand

    def get_prompt(self):

        return f"""
Brand Name:
{self.brand['brand_name']}

Location:
{self.brand['location']}

Tone:
{self.brand['tone']}

Target Audience:
{", ".join(self.brand['target_audience'])}

Content Pillars:
{", ".join(self.brand['content_pillars'])}

Hashtags:
{" ".join(self.brand['hashtags'])}

Generate content that follows these brand rules.
"""