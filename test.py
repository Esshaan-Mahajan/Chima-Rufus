
from Rufus import RufusClient
import os

# Set the API key from environment variables (or use a default for testing)
api_key = os.getenv('RUFUS_API_KEY', 'your_default_api_key')

# Set the base URL for your deployed API; here, we assume it's running locally.
client = RufusClient(api_key=api_key, base_url="http://127.0.0.1:8000")

instructions = "Find information about product features and customer FAQs."
# Set all parameters for the API call
start_url = "https://www.sf.gov/"
depth = 2
keywords = "features,faq,pricing"
use_dynamic = True

# Call the scrape method
documents = client.scrape(start_url, depth=depth, keywords=keywords, use_dynamic=use_dynamic)

print("Scraped Documents:")
print(documents)



