# Chima-Rufus
Web crawler for RAG


## Summary of Approach

**Rufus** is an AI-driven web crawler designed to extract and synthesize web data into structured JSON documents that can be directly used in Retrieval-Augmented Generation (RAG) pipelines. The approach focuses on building a robust system that:

- **Crawls Websites Intelligently:**  
  Rufus accepts a user-defined prompt in the form of a starting URL, maximum crawl depth, and keyword filters. It recursively follows internal links while filtering out irrelevant pages, ensuring that the crawl is tailored to the user's needs.

- **Extracts and Synthesizes Data:**  
  Using Python's `requests` and `BeautifulSoup`, Rufus extracts clean, human-readable text from web pages. It also supports dynamic content rendering via Playwright for modern JavaScript-heavy websites. The extracted content is compiled into a structured JSON document containing the source URL, user instructions, and a list of crawled pages with their URLs and content.

- **Handles Complex Web Structures:**  
  Designed to navigate nested links, Rufus uses a recursive mechanism that follows internal links based on configurable depth and keyword filtering. This makes it capable of handling the diversity of web structures encountered across various websites.

- **Delivers Clean, Ready-to-Use Output:**  
  The final JSON output is designed to be immediately integrated into RAG systems, serving as a rich context or knowledge base for downstream retrieval or question-answering tasks.

## Challenges & Solutions

- **Handling Dynamically-Loaded Content:**  
  Many modern websites rely on JavaScript to load content dynamically. To overcome this, I integrated Playwright as an optional component, allowing Rufus to render and extract content from such pages.

- **Robust Link Extraction and Filtering:**  
  Extracting relevant links from diverse website structures was challenging. I implemented a recursive crawling mechanism with keyword-based filtering to ensure that only pertinent links are followed, reducing noise and enhancing output quality.

- **API Integration and Security:**  
  To make Rufus accessible to developers, I built a FastAPI-based endpoint secured with API key authentication. Additionally, I developed a client library (`RufusClient`) to abstract API calls, simplifying integration into downstream RAG pipelines.


## How Rufus Works

1. **Crawling and Extraction:**  
   - **Starting Point:** Rufus begins at a specified URL.
   - **Recursive Crawling:** It follows internal links up to a user-defined depth.
   - **Text Extraction:** For each page, it extracts clean text using `BeautifulSoup` and collects internal links that match provided keyword filters.

2. **Dynamic Content Support:**  
   - Optionally, Rufus uses Playwright to render pages that load content dynamically via JavaScript, ensuring that no vital information is missed.

3. **Structured Output:**  
   - The final output is a JSON document that includes:
     - `source`: The starting URL.
     - `instructions`: Metadata provided by the user explaining the purpose of the crawl.
     - `pages`: A list of objects, each containing a page's URL and its extracted content.

## Integration into a RAG Pipeline

The structured JSON output from Rufus is designed for seamless integration into RAG systems. Here’s how you can integrate Rufus:

1. **Deploy the API:**  
   - Host the FastAPI server on a cloud provider (e.g., Heroku, AWS, DigitalOcean). For this submission, the solution is configured for local testing, but it can easily be deployed publicly.

2. **Use the Client Library:**  
   - Install the Rufus package (via `pip install .` from the repository root or from PyPI) and use the provided `RufusClient` to initiate crawls.
   - Example usage is demonstrated in the `testing.py`  script.

3. **Feed the Output into the RAG System:**  
   - The JSON document produced by Rufus can be directly passed as a knowledge base or context input to your RAG system, enabling enhanced retrieval and generation capabilities.

## How to Set Up and Run Rufus

### For Windows Users

1. **Clone the Repository:**
   - Open Command Prompt or PowerShell.
   - Run the following commands:
     ```batch
     git clone https://github.com/Esshaan-Mahajan/Chima-Rufus.git
     cd Chima-Rufus
     ```

2. **Create and Activate a Virtual Environment:**
   - Create a virtual environment:
     ```batch
     python -m venv venv
     ```
   - Activate the virtual environment:
     ```batch
     venv\Scripts\activate
     ```

3. **Install Required Packages:**
   - Install the necessary dependencies:
     ```batch
     pip install fastapi uvicorn requests beautifulsoup4 python-dotenv
     pip install playwright  (if dynamic content support is required)
     playwright install
     ```

4. **Set Environment Variables:**
   - **Option 1:** Set variables directly in Command Prompt:
     ```batch
     set RUFUS_API_KEY=my_default_api_key
     set RUFUS_BASE_URL=http://127.0.0.1:8000
     ```
   - **Option 2:** Create a `.env` file in the project root with the following content:
     ```
     RUFUS_API_KEY=my_default_api_key
     RUFUS_BASE_URL=http://127.0.0.1:8000
     ```
     The `python-dotenv` package will automatically load these variables.

5. **Run the FastAPI Server:**
   - In your Command Prompt or PowerShell (with the virtual environment activated), run:
     ```batch
     python main.py
     ```
   - Verify that the server is running by navigating to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.

6. **Run the Rufus Client Example:**
   - Open a new Command Prompt or PowerShell window (with the virtual environment still activated) and run:
     ```batch
     python testing.py
     ```
   - This script uses the `RufusClient` to call the `/scrape` endpoint and prints the resulting JSON output.

### For Linux/Mac Users

1. **Clone the Repository:**
   - Open your terminal and run:
     ```bash
     git clone https://github.com/Esshaan-Mahajan/Chima-Rufus.git
     cd Chima-Rufus
     ```

2. **Create and Activate a Virtual Environment:**
   - Create a virtual environment:
     ```bash
     python3 -m venv venv
     ```
   - Activate the virtual environment:
     ```bash
     source venv/bin/activate
     ```

3. **Install Required Packages:**
   - Install the necessary dependencies:
     ```bash
     pip install fastapi uvicorn requests beautifulsoup4 python-dotenv
     pip install playwright  # if dynamic content support is required
     playwright install
     ```

4. **Set Environment Variables:**
   - **Option 1:** Temporarily set variables in your shell:
     ```bash
     export RUFUS_API_KEY=my_default_api_key
     export RUFUS_BASE_URL=http://127.0.0.1:8000
     ```
   - **Option 2:** Create a `.env` file in the project root with the following content:
     ```
     RUFUS_API_KEY=my_default_api_key
     RUFUS_BASE_URL=http://127.0.0.1:8000
     ```
     The `python-dotenv` package will load these automatically when running the scripts.

5. **Run the FastAPI Server:**
   - In your terminal (with the virtual environment activated), run:
     ```bash
     python main.py
     ```
   - Verify that the server is running by visiting [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

6. **Run the Rufus Client Example:**
   - Open another terminal window (with the virtual environment activated) and run:
     ```bash
     python testing.py
     ```
   - This will execute the client script that calls the `/scrape` endpoint and prints the structured JSON output.

### Deployment Note

For this submission, the solution is configured for local testing. If you decide to deploy Rufus publicly (e.g., on Heroku, AWS, or DigitalOcean), update the `RUFUS_BASE_URL` environment variable to point to your deployed API's URL (for example, `https://rufus-api.herokuapp.com`). The rest of the setup remains the same, ensuring that developers can easily switch between local testing and public deployment.

By following these instructions, users on any platform can set up, run, and test Rufus, and then integrate its output into their Retrieval-Augmented Generation (RAG) pipelines.


