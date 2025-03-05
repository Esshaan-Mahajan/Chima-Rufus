
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl_website_to_json(start_url, depth=2, keyword_filters=None, use_dynamic=False, instructions=None):
    """
    Crawl a website starting from start_url up to a specified depth.
    Optionally filter links based on keywords and use dynamic content fetching.
    The 'instructions' parameter is included as metadata.
    """
    visited_urls = set()
    
    # Process keyword filters: if empty string then no filtering.
    if keyword_filters is None:
        keyword_filters = ["faq", "about", "contact", "services"]
    else:
        if isinstance(keyword_filters, str):
            if keyword_filters.strip() == "":
                keyword_filters = []  # No filtering; crawl all internal links.
            else:
                keyword_filters = [kw.strip() for kw in keyword_filters.split(",") if kw.strip()]
    
    results = []
    queue = [(start_url, 0)]  # (url, current_depth)

    while queue:
        url, current_depth = queue.pop(0)
        if url in visited_urls or current_depth > depth:
            continue

        print(f"Scraping: {url}")
        visited_urls.add(url)
        html_content = fetch_page(url, use_dynamic=use_dynamic)
        if not html_content:
            continue

        page_text = extract_text(html_content)
        results.append({"url": url, "content": page_text})
        
        # Extract links and filter if keyword_filters is provided.
        links = extract_links(html_content, start_url)
        if keyword_filters:
            for link in links:
                if any(keyword.lower() in link.lower() for keyword in keyword_filters):
                    queue.append((link, current_depth + 1))
        else:
            for link in links:
                queue.append((link, current_depth + 1))
    
    return {"source": start_url, "instructions": instructions, "pages": results}

def fetch_page(url, use_dynamic=False):
    """
    Fetch the HTML content of a page.
    If use_dynamic is True, use Playwright to render JavaScript content.
    """
    if use_dynamic:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            print("Playwright is not installed. Install it via 'pip install playwright' and run 'playwright install'.")
            return None
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=10000)
                content = page.content()
                browser.close()
            return content
        except Exception as e:
            print(f"Dynamic content error fetching {url}: {e}")
            return None
    else:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

def extract_text(html):
    """Extract clean text from HTML."""
    if not html:
        return None
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n", strip=True)

def extract_links(html, base_url):
    """Extract all internal links from a page."""
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            links.add(full_url)
    return links

if __name__ == "__main__":
    # For testing: crawl a website and save output as a JSON file.
    start_url = "https://www.nyc.gov"  # Change as needed.
    data = crawl_website_to_json(start_url, depth=2, use_dynamic=False, instructions="Test crawl for NYC.gov")
    with open("rufus_output.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Crawling completed. Output saved to rufus_output.json")
