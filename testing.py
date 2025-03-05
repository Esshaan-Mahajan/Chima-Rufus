
from Rufus import RufusClient
import os
from dotenv import load_dotenv

load_dotenv()  # Loads environment variables from a .env file if available

# Ensure your .env file contains:
# RUFUS_API_KEY=my_default_api_key
# RUFUS_BASE_URL=http://127.0.0.1:8000  (or your public URL)

api_key = os.getenv('RUFUS_API_KEY', 'my_default_api_key')
base_url = os.getenv('RUFUS_BASE_URL', 'http://127.0.0.1:8000')

client = RufusClient(api_key=api_key, base_url=base_url)

instructions = "We're making a chatbot for the HR department in San Francisco. Find relevant FAQs and contact information."
start_url = "https://www.sf.gov"
depth = 3
keywords = "faq,about,contact,services,hr"
use_dynamic = False  # Set to True if dynamic fetching is required

documents = client.scrape(start_url, depth=depth, keywords=keywords, use_dynamic=use_dynamic, instructions=instructions)
print("Scraped Documents:")
print(documents)
