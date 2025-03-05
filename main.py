# main.py
from fastapi import FastAPI, Query, HTTPException, Security, status, Depends
from fastapi.security.api_key import APIKeyHeader
import uvicorn
import os
from rufus_output import crawl_website_to_json

# Retrieve the API key from the environment; default is "my_default_api_key".
API_KEY = os.getenv("RUFUS_API_KEY", "my_default_api_key")
API_KEY_NAME = "Authorization"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == f"Bearer {API_KEY}":
        return api_key_header
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

app = FastAPI(title="Rufus Web Crawler API")

@app.get("/")
def read_root():
    return {"message": "Welcome to Rufus Web Crawler API"}

@app.get("/scrape", summary="Scrape a website and return structured data", dependencies=[Depends(get_api_key)])
def scrape(
    start_url: str = Query(..., description="The starting URL to crawl"),
    depth: int = Query(2, description="The depth to crawl (default is 2)"),
    keywords: str = Query("faq,about,contact,services", description="Comma-separated keywords to filter links"),
    use_dynamic: bool = Query(False, description="Whether to use dynamic content fetching (requires playwright)"),
    instructions: str = Query("", description="User instructions for the crawl (metadata)")
):
    try:
        data = crawl_website_to_json(
            start_url, 
            depth=depth, 
            keyword_filters=keywords, 
            use_dynamic=use_dynamic, 
            instructions=instructions
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
