# Trafilatura Deterministic Article Scraper

A lightweight, non-AI Python tool designed to discover and extract blogs, news, and insights from unseen websites deterministically using rule-based URL discovery and the **Trafilatura** library.

---

## 1. Features

- **Non-AI / No LLM Required**: Purely rule-based and deterministic discovery.
- **Automated Sitemap Discovery**: Finds `/sitemap.xml`, `/sitemap_index.xml`, and recursive sub-sitemaps (e.g., `post-sitemap.xml`, `page-sitemap.xml`).
- **Cloudflare / WAF Bypass**: Uses `httpx` for fast fetches with an automatic `trafilatura.fetch_url()` fallback when encountering 403 Forbidden or anti-bot security challenges.
- **Domain Boundary Guard**: Enforces strict domain limits to avoid crawling external links (e.g., third-party repositories).
- **Asset Sitemap Exclusion**: Ignores non-article sitemaps (`image-sitemap`, `video-sitemap`, `author-sitemap`) for fast, targeted crawls.
- **Hub Page Fallback Crawling**: Probes `/blog/`, `/insights/`, and `/news/` pages and applies a slug hyphen-density rule to detect articles posted directly at root (`domain.com/article-name/`).
- **Clean Content Extraction**: Powered by **Trafilatura** for boilerplate-free main body text, publication dates, and author metadata extraction.
- **Configurable Rules**: Centralized regex and scoring engine (`rules.py`) to easily tweak path exclusions and inclusion criteria.

## 2. Deterministic Scoring Rules & Heuristics (`rules.py`)

To distinguish blog articles from static site pages (like About, Contact, Careers, Terms) **without using AI or LLMs**, the project implements a deterministic scoring engine (`score_url`) based on 3 core rule sets:

### Rule 1: Explicit Path Keyword Matching
Modern websites often group articles under dedicated URL subfolders.
- **Inclusion Keywords**: `/blog/`, `/blogs/`, `/news/`, `/insights/`, `/article/`, `/posts/`.
- **How It Works**: If a URL contains any of these keywords in its path, it receives a **+50 point** score boost.
- **Example**: `northbaysolutions.com/insights/blog/scaling-genai/` $\rightarrow$ Matches `/insights/` & `/blog/` (High Candidate).

### Rule 2: Hyphen-Density Heuristic (Root-Slug Articles)
Many websites (like **NextBridge**) host blog posts directly under the root domain without `/blog/` prefixes.
- **How It Works**: Blog article titles are multi-word sentences converted into URL slugs with hyphens (`-`). Regular site pages usually have 0 to 1 hyphens (`/contact-us/`, `/about/`), whereas blog post titles almost always contain **2 or more hyphens**.
- **Threshold**: Slugs with $\ge 2$ hyphens receive a **+15 point** score boost.
- **Examples**:
  - `nextbridge.com/soc2-compliance-trust-security/` (3 hyphens) $\rightarrow$ **Article Accepted**
  - `nextbridge.com/how-generative-ai-increases-product-delivery/` (6 hyphens) $\rightarrow$ **Article Accepted**
  - `nextbridge.com/contact-us/` (1 hyphen) $\rightarrow$ Rejected / Ignored

### Rule 3: Exclusion Filter System
To eliminate non-article pages that might accidentally trigger hyphen thresholds or get picked up during hub crawling:
- **Exclusion Lists**: `/contact/`, `/about/`, `/privacy-policy/`, `/terms/`, `/careers/`, `/team/`, `/services/`, `/tag/`, `/category/`, `/author/`, `/page/`.
- **File Extension Filter**: Rejects assets like `.png`, `.jpg`, `.pdf`, `.svg`, `.css`, `.js`.
- **How It Works**: If a URL contains an exclusion pattern, `is_excluded_url()` returns `True`, immediately rejecting the candidate URL regardless of its score.

---

## 3. Project Structure

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
