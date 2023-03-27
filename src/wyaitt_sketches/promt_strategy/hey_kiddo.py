import re
import datetime
import logging
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
    content_description: str
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

        with open('actors/prompt_generator', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            self.prompt_generation_strategy = ' '.join(lines)

        with open('actors/content_descriptor', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            self.content_descriptor = ' '.join(lines)

    def _select_article(self, date: datetime.date = None) -> Dict:
        articles = self.source.fetch_articles(date)

        titles = [article["webTitle"] for article in articles]
        titles_prompt = " ".join([f"{i}. {x}" for i, x in enumerate(titles)])

        selected_title = self._get_completion(
            f"Which one of this titles is most suitable for a ironic picture? "
            f"Reply only with one number.  {titles_prompt}"
        )
        match = re.search(r'\d+', selected_title)
        if match:
            title_number = int(match.group())
        else:
            raise ValueError(f"Cannot parse title number {selected_title}")

        return articles[title_number]

    def evaluate(self, date: datetime.date = None) -> PromptOutput:
        """

        :param date: if None, d
        :return:
        """

        article = self._select_article(date)

        logging.debug(f"article: {article['webTitle']}")

        paragraphs = self.source.fetch_content(article["apiUrl"], 2)

        content_description = self._get_completion(
            f"Describe this {article['webTitle'] + ' '.join(paragraphs)}",
            self.content_descriptor
        )

        logging.debug(f"content_description: {content_description}")

        illustration_prompt = self._get_completion(
            f"Concept: {content_description}",
            self.prompt_generation_strategy
        )

        logging.debug(f"illustration_prompt: {illustration_prompt}")

        # illustration_style = self._get_completion(
        #     f"what is the best style for this picture? Answer in 3 words {illustration_prompt}",
        #     "an artist"
        # )
        #
        # logging.debug(f"illustration_style: {illustration_style}")

        prompt_output = PromptOutput(
            original_title=article['webTitle'],
            original_url=article["webUrl"],
            content_description=content_description,
            # illustration_prompt=illustration_prompt + illustration_style
            illustration_prompt=illustration_prompt
        )

        return prompt_output
