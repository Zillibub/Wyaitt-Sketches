import json
import datetime
import requests
from typing import List, Dict
from wyaitt_sketches.core.settings import settings


class TheGuardianSource:

    def __init__(self):
        self.api_url = 'https://content.guardianapis.com/search'

    def fetch_today_articles(self) -> List[Dict]:
        """
        Features today article titles
        :return: list of today articles
        """
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        params = {
            'api-key': settings.the_guardian_api_key,
            'from-date': current_date,
            'to-date': current_date
        }

        response = requests.get(self.api_url, params=params)
        if response.status_code != 200:
            raise ValueError("Cannot retrieve data")

        return json.loads(response.text)['response']['results']

    def fetch_content(self, api_url: str, amount_of_paragraphs: int) -> List[str]:
        """

        :param api_url:
        :param amount_of_paragraphs:
        :return:
        """

