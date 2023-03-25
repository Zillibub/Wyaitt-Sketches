from typing import Dict
import re
from wyaitt_sketches.promt_strategy.base_strategy import BaseStrategy
from wyaitt_sketches.api.sources.the_guardian import TheGuardianSource


class HeyKiddoStrategy(BaseStrategy):
    """
    This class implements a prompt scenario for generating a picture for today article.

    The scenario consists of the following steps:
    1. Fetching today's articles using the Guardian API.
    2. Selecting an article based on the title using GPT .
    3. Creating an explanation for a 5 year old for the selected article by combining the title
    and the first two paragraphs of the article.
    4. Creating an illustration description for the selected article.
    5. Selecting a style for the illustration.

    """

    def __init__(self):
        self.source = TheGuardianSource()

    def _select_article(self) -> Dict:
        articles = self.source.fetch_today_articles()

        titles = [article["webTitle"] for article in articles]
        titles_promt = " ".join([f"{i}. {x}" for i, x in enumerate(titles)])

        selected_title = self._get_completion(
            f"Which one of this titles is most suitable for a funny picture? "
            f"Reply only with one number.  {titles_promt}"
        )
        match = re.search(r'\d+', selected_title)
        if match:
            title_number = int(match.group())
        else:
            raise ValueError("Cannot parse title number")

        return articles[title_number]

    def evaluate(self):

        article = self._select_article()

