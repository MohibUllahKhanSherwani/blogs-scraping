# Trafilatura Deterministic Article Scraper

A lightweight, non-AI Python tool designed to discover and extract blogs, news, and insights from unseen websites deterministically using rule-based URL discovery and the **Trafilatura** library.

---

## 1. Features

- **Non-AI / No LLM Required**: Purely rule-based and deterministic discovery.
- **Automated Sitemap Discovery**: Finds `/sitemap.xml`, `/sitemap_index.xml`, and `robots.txt` references automatically.
- **Hub Page Fallback Crawling**: Probes and extracts article links from `/blog/`, `/insights/`, and `/news/` listing pages for websites hosting articles directly under root slugs (e.g., `domain.com/article-name/`).
- **Clean Content Extraction**: Powered by **Trafilatura** for main body text, publication dates, and author metadata extraction without boilerplate HTML noise.
- **Configurable Rules**: Centralized regex and rule scoring system (`rules.py`) to easily tweak URL acceptance criteria.

---

## 2. Project Structure

```text
scraper_test/
    ├── main.py           # Evaluation runner and summary reporter
    ├── discovery.py      # Sitemap detection, XML parsing, and link harvesting
    ├── extraction.py     # Trafilatura content & metadata extraction wrapper
    ├── rules.py          # Configurable URL regex scoring and exclusion rules
    ├── models.py         # Data structures for results and reporting
    ├── requirements.txt  # Python dependencies
    ├── README.md         # Documentation & guide
    └── results/          # Output directory storing raw JSON extraction results
        ├── nextbridge.json
        └── northbay.json
```

---

## 3. Quickstart

### Step 1: Create & Activate Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Linux / macOS)
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Scraper
```bash
python main.py
```

---

## 4. How to Add a New Website

Open `main.py` and add your target domain URL to `target_websites`:

```python
target_websites = [
    ("https://nextbridge.com/", "nextbridge.json"),
    ("https://northbaysolutions.com/", "northbay.json"),
    ("https://yourwebsite.com/", "yourwebsite.json")  # Add new target here
]
```

---

## 5. Why Trafilatura?

Trafilatura uses advanced document text-density algorithms and DOM structure heuristics to remove boilerplate clutter (navbars, footers, cookie popups, related posts) automatically, returning clean text and structured metadata (`title`, `author`, `date`) without requiring external LLM API calls or heavy browser automation.
