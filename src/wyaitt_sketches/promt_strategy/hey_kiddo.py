import re
import datetime
from typing import Dict
from dataclasses import dataclass
from wyaitt_sketches.promt_strategy.base_strategy import BaseStrategy
from wyaitt_sketches.api.sources.the_guardian import TheGuardianSource


@dataclass
class PromptOutput:
    """
    Result of hey kiddo strategy evaluation
    """
    original_title: str
    original_url: str
    illustration_prompt: str


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

    def _select_article(self, date: datetime.date = None) -> Dict:
        articles = self.source.fetch_articles(date)

        titles = [article["webTitle"] for article in articles]
        titles_prompt = " ".join([f"{i}. {x}" for i, x in enumerate(titles)])

        selected_title = self._get_completion(
            f"Which one of this titles is most suitable for a funny picture? "
            f"Reply only with one number.  {titles_prompt}"
        )
        match = re.search(r'\d+', selected_title)
        if match:
            title_number = int(match.group())
        else:
            raise ValueError("Cannot parse title number")

        return articles[title_number]

    def evaluate(self, date: datetime.date = None) -> PromptOutput:
        """

        :param date: if None, d
        :return:
        """

        article = self._select_article(date)

        paragraphs = self.source.fetch_content(article["apiUrl"], 2)

        content_description = self._get_completion(
            f"Explain this for a 5 year old {article['webTitle'] + ' '.join(paragraphs)} in a funny way",
            "an artist"
        )

        illustration_prompt = self._get_completion(
            f"describe this illustration {content_description} in 30 words sentence",
            "a graphic designer generating creative images. You provide ironic descriptive prompts"
        )

        illustration_style = self._get_completion(
            f"what is the best style for this picture? Answer in 3 words {illustration_prompt}",
            "an artist"
        )

        prompt_output = PromptOutput(
            original_title=article['webTitle'],
            original_url=article["webUrl"],
            illustration_prompt=illustration_prompt + illustration_style
        )

        return prompt_output
