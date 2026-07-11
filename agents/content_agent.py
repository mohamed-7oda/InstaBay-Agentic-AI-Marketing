from agents.brand_agent import BrandAgent
from utils.llm import ask_llm


class ContentAgent:

    def __init__(self):
        self.brand = BrandAgent()

    def generate_post(self):

        prompt = self.brand.get_prompt() + """

Generate ONE Instagram post for InstaBay Resort.

Requirements:

- Write in BOTH English and Arabic.
- Create an engaging caption.
- Add a Call To Action.
- Add 5 relevant hashtags.
- Keep the tone luxurious, relaxing, and friendly.

Return ONLY the final post.
"""

        return ask_llm(prompt)