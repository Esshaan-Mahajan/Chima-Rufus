
import requests

class RufusClient:
    def __init__(self, api_key, base_url="http://127.0.0.1:8000"):
        self.api_key = api_key
        self.base_url = base_url

    def scrape(self, start_url, depth=2, keywords="faq,about,contact,services", use_dynamic=False):
        """
        Calls the Rufus /scrape endpoint to crawl the provided URL.
        """
        params = {
            "start_url": start_url,
            "depth": depth,
            "keywords": keywords,
            "use_dynamic": use_dynamic,
        }
        # Optionally, if you want to use the API key, you can pass it in headers:
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        response = requests.get(f"{self.base_url}/scrape", params=params, headers=headers)
        response.raise_for_status()
        return response.json()
