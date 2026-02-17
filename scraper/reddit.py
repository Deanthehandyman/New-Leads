import requests
    import time
    from datetime import datetime
    
    class RedditScraper:
        def __init__(self):
            self.subreddits = ['EastTexas', 'TylerTX', 'LongviewTX', 'Texas', 'HomeImprovement', 'realestateinvesting']
            self.keywords = ['handyman', 'repair', 'fix', 'help needed', 'contractor', 'plumber', 'electrician']
            self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HandymanLeadFinder/1.0'}
    
        def scrape(self):
            found_leads = []
            print(f"   [REDDIT] Scanning {len(self.subreddits)} subreddits...")
            
            for sub in self.subreddits:
                try:
                    url = f"https://www.reddit.com/r/{sub}/new.json?limit=10"
                    response = requests.get(url, headers=self.headers, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        posts = data.get('data', {}).get('children', [])
                        
                        for post in posts:
                            p_data = post['data']
                            title = p_data.get('title', '').lower()
                            text = p_data.get('selftext', '').lower()
                            
                            # Check keywords
                            if any(k in title or k in text for k in self.keywords):
                                lead = {
                                    'source': 'Reddit',
                                    'source_id': p_data['id'],
                                    'title': p_data['title'][:100],
                                    'url': f"https://reddit.com{p_data['permalink']}",
                                    'location': f"r/{sub}",
                                    'date_posted': datetime.fromtimestamp(p_data['created_utc']).strftime('%Y-%m-%d'),
                                    'score': 'WARM',
                                    'score_val': 60,
                                    'status': 'NEW'
                                }
                                found_leads.append(lead)
                    time.sleep(2)
                except Exception as e:
                    print(f"   Error scraping r/{sub}: {e}")
                    
            return found_leads
