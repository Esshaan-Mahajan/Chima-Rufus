from fastapi import FastAPI, Query, HTTPException
import uvicorn
from rufus_output import crawl_website_to_json  # Make sure rufus_output.py is in the same directory

app = FastAPI(title="Rufus Web Crawler API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Rufus Web Crawler API"}

@app.get("/scrape", summary="Scrape a website and return structured data")
def scrape(
    start_url: str = Query(..., description="The starting URL to crawl"),
    depth: int = Query(2, description="The depth to crawl (default is 2)"),
    keywords: str = Query("faq,about,contact,services", description="Comma-separated keywords to filter links")
):
    """
    Crawl the website starting from `start_url`, follow internal links that include any of the keywords provided,
    and return the scraped content in a structured JSON format.
    """
    # Convert the comma-separated keywords string into a list
    keyword_filters = [kw.strip() for kw in keywords.split(",") if kw.strip()]
    try:
        data = crawl_website_to_json(start_url, depth=depth, keyword_filters=keyword_filters)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
