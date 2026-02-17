import requests
    from bs4 import BeautifulSoup
    import time
    import random
    from config import CENTER_ZIP
    
    class SocialScraper:
        def __init__(self):
            self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            self.sites = ['site:facebook.com', 'site:nextdoor.com', 'site:instagram.com']
            self.queries = [f'"need a handyman" {CENTER_ZIP}', f'"looking for handyman" {CENTER_ZIP}']
    
        def scrape(self):
            found_leads = []
            print(f"   [SOCIALS] Searching public posts via DuckDuckGo...")
            for site in self.sites:
                for query in self.queries:
                    try:
                        full_query = f"{site} {query}"
                        url = f"https://html.duckduckgo.com/html/?q={full_query}"
                        time.sleep(random.uniform(2, 5))
                        response = requests.get(url, headers=self.headers, timeout=15)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, 'html.parser')
                            for res in soup.select('.result')[:5]:
                                title_tag = res.select_one('.result__title a')
                                if title_tag:
                                    link = title_tag['href']
                                    found_leads.append({
                                        'source': 'Social Search',
                                        'source_id': link,
                                        'title': title_tag.text.strip(),
                                        'url': link,
                                        'location': 'Online',
                                        'date_posted': 'Recent',
                                        'score': 'COLD',
                                        'score_val': 30,
                                        'status': 'NEW'
                                    })
                    except Exception as e:
                        print(f"Error {site}: {e}")
            return found_leads
    
