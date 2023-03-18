import json
import datetime
import requests
from typing import List
from wyaitt_sketches.core.settings import settings


class TheGuardianSource:

    def __init__(self):
        self.api_url = 'https://content.guardianapis.com/search'

    def fetch(self) -> List[str]:
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

        data = json.loads(response.text)

        titles = []
        for article in data['response']['results']:
            titles.append(article["webTitle"])
        return titles
