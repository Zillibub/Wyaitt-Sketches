import datetime
import json
import pytest
from unittest.mock import patch, MagicMock
from wyaitt_sketches.api.sources.the_guardian import TheGuardianSource


@pytest.fixture
def today_articles():
    # Fixture to provide a sample list of articles
    return [{'id': 'article1', 'webTitle': 'Article 1'}, {'id': 'article2', 'webTitle': 'Article 2'}]


@pytest.fixture
def guardian(today_articles):
    # Fixture to provide an instance of TheGuardianSource class
    with patch.object(datetime, 'datetime') as mock_date:
        mock_date.now.return_value.strftime.return_value = '2022-01-01'
        guardian = TheGuardianSource()
    guardian.api_url = 'http://example.com'
    return guardian


def test_fetch_today_articles(guardian, today_articles):
    # Mock response from The Guardian API
    mock_response = MagicMock(status_code=200)
    mock_response.json.return_value = {'response': {'results': today_articles}}

    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response
        articles = guardian.fetch_today_articles()

    # Check that the response is parsed correctly
    assert articles == today_articles


def test_fetch_content(guardian):
    # Mock response from The Guardian API
    expected_result = ['First paragraph', 'Second paragraph', 'Third paragraph']
    mock_response = MagicMock(status_code=200, text=json.dumps({
        'response': {
            'content': {
                'fields': {
                    'body': '<div><p>First paragraph</p><p>Second paragraph</p><p>Third paragraph</p></div>'
                }
            }
        }
    }))

    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response
        content = guardian.fetch_content('http://example.com', 3)

    # Check that the response is parsed correctly
    assert content == expected_result


def test_fetch_content_error(guardian):
    # Test case when the API returns an error response
    mock_response = MagicMock(status_code=404)
    with patch('requests.get') as mock_get:
        mock_get.return_value = mock_response
        with pytest.raises(ValueError):
            guardian.fetch_content('http://example.com', 3)
