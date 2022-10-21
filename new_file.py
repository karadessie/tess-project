import os
from newsdataapi import NewsDataApiClient

returned_response = {}


API_KEY = os.environ.get("NEWSDATA_API_KEY")
api = NewsDataApiClient(apikey=API_KEY)
response = api.news_api(category = "environment", country = "us")
for article in response["results"]:
    returned_response[article["title"]] = article["link"]
