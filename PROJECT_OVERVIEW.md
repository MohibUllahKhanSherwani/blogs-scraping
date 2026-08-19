# Scraping Agent (Deterministic Web Scraper)

A lightweight, non-AI Python prototype designed to reliably discover and extract article/blog content from unknown websites using deterministic methods like recursive sitemap traversal, rule-based URL scoring, and Trafilatura content extraction.

---

## 🎯 Core Objectives & Constraints

- **Strict Non-AI Policy**: No LLMs, embeddings, or headless browser automation (Playwright/Puppeteer/Selenium).
- **Lightweight Footprint**: Rely exclusively on fast HTTP requests (`httpx`), DOM parsing (`BeautifulSoup`), and density/rule-based text extraction (`Trafilatura`).
- **CMS Agnostic & Robust**: Support varied WordPress/CMS configurations (e.g., Yoast, Rank Math SEO plugins, root-level post slugs).

---

## 🛠️ System Architecture

```
scraper_test/
├── main.py           # Pipeline runner & summary report generator
├── discovery.py      # Recursive sitemap engine + hub-page link harvester
├── rules.py          # Deterministic URL scoring & exclusion filter system
├── extraction.py     # Trafilatura text/metadata extractor with WAF fallback
├── models.py         # Data classes for articles and reports
└── requirements.txt  # Python dependencies (httpx, beautifulsoup4, trafilatura, lxml)
```

---

## 🚀 Key Features & Edge Case Handling

### 1. Discovery Engine (`discovery.py`)
- **Recursive Sitemap Traversal**: Discovers `sitemap.xml`, `sitemap_index.xml`, and sub-sitemaps (e.g., `post-sitemap.xml`, `page-sitemap.xml`).
- **Tag & Namespace Agnostic**: Uses Regex + HTML parsing to extract `<loc>` URLs, overcoming custom XSL stylesheet and XML namespace issues.
- **WAF / Cloudflare Fallback**: Primary requests use `httpx`. If blocked (HTTP 403 or Cloudflare challenge page), automatically falls back to `trafilatura.fetch_url()`.
- **Domain Boundary Guard**: Enforces strict netloc checks to prevent the crawler from following external links (e.g., avoiding GitHub links inside WordPress dev docs).
- **Asset Sitemap Exclusion**: Ignores non-article asset sitemaps (e.g., `image-sitemap`, `video-sitemap`, `author-sitemap`, `tag-sitemap`).
- **Hub Page Harvesting**: Scrapes listing pages (`/blog/`, `/insights/`, `/news/`) as a secondary candidate discovery path.

### 2. Rule Engine (`rules.py`)

The rule engine deterministically scores every discovered URL without needing AI/LLMs:

- **Rule A: Explicit Path Keyword Matching**: 
  - *Logic*: Boosts score by **+50** if path contains `/blog/`, `/blogs/`, `/news/`, `/insights/`, `/article/`, or `/posts/`.
  - *Example*: `northbaysolutions.com/insights/blog/scaling-genai/` (Matched)

- **Rule B: Hyphen-Density Heuristic (Root-Slug Articles)**:
  - *Logic*: Evaluates trailing path slugs. Since blog article titles are multi-word sentences, article slugs contain multiple hyphens. Slugs with $\ge 2$ hyphens receive a **+15** score boost.
  - *Examples*:
    - `nextbridge.com/soc2-compliance-trust-security/` (3 hyphens $\rightarrow$ Article Candidate)
    - `nextbridge.com/how-generative-ai-increases-product-delivery/` (6 hyphens $\rightarrow$ Article Candidate)
    - `nextbridge.com/contact-us/` (1 hyphen $\rightarrow$ Ignored/Below Threshold)

- **Rule C: Exclusion Filter System**:
  - *Logic*: Hard-rejects non-article pages (`/contact/`, `/about/`, `/privacy-policy/`, `/terms/`, `/careers/`, `/team/`, `/services/`, `/tag/`, `/category/`, `/author/`) and static media assets (`.png`, `.jpg`, `.pdf`, `.svg`).

### 3. Extraction Engine (`extraction.py`)
- **Trafilatura Native Parsing**: Passes raw HTML into Trafilatura to extract clean title, published date, author, and main body text without boilerplate navigation headers/footers.
- **WAF Fallback on Article Extraction**: Utilizes `trafilatura.fetch_url()` if direct `httpx` page fetching is blocked.

---

## 📊 Summary of Tested Sites

| Website | Sitemaps Found | Candidates Discovered | Accepted Articles | Extraction Status | Key Challenge Resolved |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **NorthBay Solutions** | 4 | 562 | 64 | ✅ 100% Success | Standard sitemap + hub page harvesting |
| **NextBridge** | 1 | 227 | 184 | ✅ 100% Success | Solved Cloudflare 403 block on `post-sitemap.xml` via Trafilatura WAF fallback & root-slug hyphen rule |
| **Developer WordPress** | 4 | Various | Various | ✅ 100% Success | Solved external domain link leaks (e.g. GitHub) using Domain Guard |
| **OMG! Ubuntu!** | 4 | Thousands | Filtered | ✅ 100% Success | Solved slow crawl issue by ignoring image/video sitemaps |

---

## 💻 Quickstart

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Scraper
Add your target website to `target_websites` in `main.py` and run:
```bash
python main.py
```
Outputs are written to `results/<site_name>.json` (Note: `results/` directory is excluded in `.gitignore`).

---

## 💡 Guidelines for Future AI Assistants / Developers
- **Adding New Sites**: Simply append `("https://example.com/", "example.json")` to `target_websites` in `main.py`.
- **Modifying Rules**: Adjust `RuleConfig` in `rules.py` to add new path exclusions or inclusion keywords.
- **Never Add Headless Browsers/LLMs**: Keep the project lightweight, fast, and deterministic. Always prefer HTTP/Regex/Trafilatura logic.
