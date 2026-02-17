#!/usr/bin/env python
    import argparse
    import pandas as pd
    import os
    from datetime import datetime
    
    # Import configurations and models
    try:
        from config import *
        from database.models import init_db, Lead
        from scrapers.craigslist import CraigslistScraper
        from scrapers.reddit import RedditScraper
        from scrapers.socials import SocialScraper
    except ImportError as e:
        print(f"Startup Warning: {e}")
        init_db = lambda: None
        Lead = None
    
    # Initialize Database
    db_session = init_db() if init_db else None
    
    class LeadFinder:
        def __init__(self):
            self.session = db_session
    
        def scrape_leads(self):
            if not self.session:
                print("Error: Database not initialized.")
                return
    
            print("\n" + "="*60)
            print("HANDYMAN LEAD FINDER - Live Scrape Mode")
            print("="*60)
    
            all_leads = []
    
            # 1. Craigslist
            try:
                print("1. Running Craigslist Scraper...")
                cl = CraigslistScraper()
                all_leads.extend(cl.scrape())
            except Exception as e:
                print(f"   [!] Craigslist failed: {e}")
    
            # 2. Reddit
            try:
                print("2. Running Reddit Scraper...")
                rd = RedditScraper()
                all_leads.extend(rd.scrape())
            except Exception as e:
                print(f"   [!] Reddit failed: {e}")
    
            # 3. Socials
            try:
                print("3. Running Social Scraper...")
                soc = SocialScraper()
                all_leads.extend(soc.scrape())
            except Exception as e:
                print(f"   [!] Socials failed: {e}")
    
            print(f"\n[PROCESSING] Saving {len(all_leads)} leads to database...")
    
            added_count = 0
            for data in all_leads:
                try:
                    exists = self.session.query(Lead).filter_by(source_id=str(data['source_id'])).first()
                    if not exists:
                        new_lead = Lead(**data)
                        self.session.add(new_lead)
                        added_count += 1
                except Exception as e:
                    print(f"   Error saving lead: {e}")
    
            self.session.commit()
            print(f"✓ Done! {added_count} new leads added.")
    
        def export_csv(self):
            if not self.session: return
            leads = self.session.query(Lead).all()
            if not leads:
                print("No leads found.")
                return
    
            df = pd.DataFrame([l.__dict__ for l in leads])
            if '_sa_instance_state' in df.columns:
                del df['_sa_instance_state']
    
            filename = f"exports/leads_{datetime.now().strftime('%Y%m%d')}.csv"
            os.makedirs('exports', exist_ok=True)
            df.to_csv(filename, index=False)
            print(f"✓ Exported {len(leads)} leads to {filename}")
    
    if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('--scrape', action='store_true', help='Scrape new leads')
        parser.add_argument('--export', action='store_true', help='Export to CSV')
    
        args = parser.parse_args()
        finder = LeadFinder()
    
        if args.scrape:
            finder.scrape_leads()
        if args.export:
            finder.export_csv()
