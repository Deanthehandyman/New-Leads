import requests
from bs4 import BeautifulSoup
import time
import random
from config import CRAIGSLIST_REGIONS, CRAIGSLIST_SEARCH_KEYWORDS

class CraigslistScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape(self):
        found_leads = []
        print(f"   [CRAIGSLIST] Scanning {len(CRAIGSLIST_REGIONS)} regions...")
        
        for region_url in CRAIGSLIST_REGIONS:
            region_name = region_url.split('//')[1].split('.')[0]
            print(f"   --> Scanning {region_name}...")
            # Search 'services' and 'gigs'
            search_urls = [
                f"{region_url}/search/sss?query={{}}",
                f"{region_url}/search/hss?query={{}}"
            ]

            for keyword in CRAIGSLIST_SEARCH_KEYWORDS:
                time.sleep(random.uniform(1.0, 3.0)) 
                for base_search in search_urls:
                    url = base_search.format(keyword.replace(' ', '+'))
                    try:
                        response = requests.get(url, headers=self.headers, timeout=10)
                        if response.status_code != 200: continue

                        soup = BeautifulSoup(response.text, 'html.parser')
                        results = soup.select('.result-row')

                        for result in results:
                            try:
                                title_elem = result.select_one('.titlestring')
                                if not title_elem: continue
                                
                                title = title_elem.text.strip()
                                link = title_elem['href']
                                date = result.select_one('.time')['title'] if result.select_one('.time') else "Unknown"
                                location = result.select_one('.nearby').text.strip() if result.select_one('.nearby') else region_name
                                
                                score = "WARM"
                                if "asap" in title.lower() or "emergency" in title.lower():
                                    score = "HOT"

                                lead = {
                                    'source': 'Craigslist',
                                    'source_id': link,
                                    'title': title,
                                    'url': link,
                                    'location': location,
                                    'date_posted': date,
                                    'score': score,
                                    'score_val': 80 if score == "HOT" else 50,
                                    'status': 'NEW'
                                }
                                found_leads.append(lead)
                            except: continue
                    except: continue
        return found_leads
