"""
Scrape the 14 'What Is...?' Workbook texts from christmind.info
These are the actual ACIM Workbook texts (public domain).
"""
import requests
import time
import json
from bs4 import BeautifulSoup

# Map of section key -> christmind.info URL slug
WHATIS_URLS = {
    "forgiveness": "https://www.christmind.info/t/acimoe/workbook/forgiveness/",
    "salvation": "https://www.christmind.info/t/acimoe/workbook/salvation/",
    "the_world": "https://www.christmind.info/t/acimoe/workbook/world/",
    "sin": "https://www.christmind.info/t/acimoe/workbook/sin/",
    "the_body": "https://www.christmind.info/t/acimoe/workbook/body/",
    "the_christ": "https://www.christmind.info/t/acimoe/workbook/christ/",
    "the_holy_spirit": "https://www.christmind.info/t/acimoe/workbook/holy-spirit/",
    "the_real_world": "https://www.christmind.info/t/acimoe/workbook/real-world/",
    "the_second_coming": "https://www.christmind.info/t/acimoe/workbook/second-coming/",
    "the_last_judgment": "https://www.christmind.info/t/acimoe/workbook/last-judgment/",
    "creation": "https://www.christmind.info/t/acimoe/workbook/creation/",
    "the_ego": "https://www.christmind.info/t/acimoe/workbook/ego/",
    "a_miracle": "https://www.christmind.info/t/acimoe/workbook/miracle/",
    "what_am_i": "https://www.christmind.info/t/acimoe/workbook/what-am-i/",
}

results = {}

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; personal study app)"
}

for key, url in WHATIS_URLS.items():
    print(f"Fetching {key} from {url}...")
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Try to find the main content area
        # christmind.info uses various content containers
        content = None
        
        # Try common content selectors
        for selector in ["article", "main", ".content", "#content", ".page-content", ".transcript"]:
            content = soup.select_one(selector)
            if content:
                break
        
        if not content:
            content = soup.find("body")
        
        if content:
            # Remove nav, header, footer, script, style elements
            for tag in content.find_all(["nav", "header", "footer", "script", "style", "button", "aside"]):
                tag.decompose()
            
            # Get paragraphs
            paragraphs = content.find_all("p")
            text_parts = []
            for p in paragraphs:
                text = p.get_text(separator=" ", strip=True)
                if text and len(text) > 20:  # Skip very short/empty paragraphs
                    text_parts.append(text)
            
            if text_parts:
                results[key] = "\n\n".join(text_parts)
                print(f"  -> Got {len(text_parts)} paragraphs, {len(results[key])} chars")
            else:
                # Fallback: get all text
                text = content.get_text(separator="\n", strip=True)
                results[key] = text
                print(f"  -> Fallback: {len(text)} chars")
        else:
            print(f"  -> No content found!")
            results[key] = ""
            
    except Exception as e:
        print(f"  -> ERROR: {e}")
        results[key] = ""
    
    time.sleep(1)  # Be polite

# Save results
output_path = "/home/ubuntu/acim_flashcards/data/whatis_workbook_text.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nSaved to {output_path}")
for key, text in results.items():
    print(f"  {key}: {len(text)} chars")
