import json
import os
from dataclasses import asdict
from typing import List

from discovery import DiscoveryEngine
from extraction import ContentExtractor
from models import WebsiteReport, ExtractionResult

def process_website(target_url: str, max_articles_to_extract: int = 5) -> WebsiteReport:
    engine = DiscoveryEngine()
    extractor = ContentExtractor()
    
    normalized_url = engine.normalize_url(target_url)
    print(f"\n--- Processing: {normalized_url} ---")
    
    # 1. Sitemap discovery & link harvesting
    sitemaps = engine.discover_sitemaps(normalized_url)
    print(f"Discovered {len(sitemaps)} sitemap(s): {sitemaps}")
    
    raw_urls = []
    for sm in sitemaps:
        raw_urls.extend(engine.parse_sitemap_urls(sm))
        
    print(f"Discovered {len(raw_urls)} total raw URLs from sitemaps.")
    
    # 2. Hub Page Fallback Discovery (For websites like NextBridge using root slugs like /soc2-compliance.../)
    print("Checking common blog hub pages for direct links...")
    hub_pages = engine.discover_hub_pages(normalized_url)
    for hub in hub_pages:
        hub_links = engine.crawl_hub_for_links(hub, normalized_url)
        print(f"  Harvested {len(hub_links)} link(s) from hub page: {hub}")
        raw_urls.extend(hub_links)
        
    # 3. Filter candidate article URLs
    accepted_urls = engine.filter_candidate_urls(raw_urls)
    print(f"Accepted {len(accepted_urls)} likely article URLs based on deterministic rules.")
    
    report = WebsiteReport(
        website_url=normalized_url,
        discovered_sitemaps=sitemaps,
        total_candidate_urls=len(raw_urls),
        accepted_article_urls=len(accepted_urls)
    )
    
    # 4. Content Extraction on subset of candidate URLs
    sample_urls = accepted_urls[:max_articles_to_extract]
    print(f"Testing content extraction on top {len(sample_urls)} candidate article(s)...")
    
    for url in sample_urls:
        print(f"  Extracting: {url}")
        res_dict = extractor.extract_all(url)
        
        article_summary = {"url": url}
        
        if "trafilatura" in res_dict and res_dict["trafilatura"].content_length > 0:
            report.parsed_trafilatura_count += 1
            article_summary["trafilatura"] = asdict(res_dict["trafilatura"])
            
        report.article_results.append(article_summary)
        
    return report

def save_report_to_json(report: WebsiteReport, filename: str):
    os.makedirs("results", exist_ok=True)
    filepath = os.path.join("results", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, indent=2, ensure_ascii=False)
    print(f"Report saved to: {filepath}")

def print_summary_report(reports: List[WebsiteReport]):
    print("\n" + "="*60)
    print("           WEBSITE SCRAPING EVALUATION REPORT          ")
    print("="*60)
    
    for r in reports:
        print(f"\nWebsite: {r.website_url}")
        print(f"Discovered sitemap URLs: {len(r.discovered_sitemaps)}")
        print(f"Number of candidate URLs: {r.total_candidate_urls}")
        print(f"Number of URLs accepted as likely articles: {r.accepted_article_urls}")
        print(f"Number successfully parsed by Trafilatura: {r.parsed_trafilatura_count}")
        
        print("\n  Detailed Sample Articles Extracted:")
        for idx, art in enumerate(r.article_results, 1):
            print(f"\n  [{idx}] URL: {art['url']}")
            if "trafilatura" in art:
                t = art["trafilatura"]
                print(f"      Trafilatura  -> Title: {t['title']} | Date: {t['date']} | Author: {t['author']} | Content Len: {t['content_length']}")
                
    print("\n" + "="*60)

def main():
    target_websites = [
        ("https://nextbridge.com/", "nextbridge.json"),
        ("https://northbaysolutions.com/", "northbay.json")
    ]
    
    reports = []
    for site_url, output_filename in target_websites:
        report = process_website(site_url, max_articles_to_extract=3)
        save_report_to_json(report, output_filename)
        reports.append(report)
        
    print_summary_report(reports)

if __name__ == "__main__":
    main()
