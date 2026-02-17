#!/usr/bin/env python
    import argparse
    import pandas as pd
    import os
    from datetime import datetime
    # Note: Requires config.py and database/models.py to be present
    try:
        from config import *
        from database.models import init_db, Lead
        from scrapers.craigslist import CraigslistScraper
    except ImportError:
        print("Warning: Missing dependencies (config, database, scrapers). Upload them to run.")
        # Dummy mocks for syntax check if run without files
        init_db = lambda: None
        Lead = None
        CraigslistScraper = None
    
    # Initialize DB if available
    db_session = init_db() if init_db else None
    
    class LeadFinder:
        def __init__(self):
            self.session = db_session
    
        def scrape_leads(self):
            if not self.session: return
            print("\n" + "="*60)
            print("HANDYMAN LEAD FINDER - Live Scrape Mode")
            print("="*60)
            
            # 1. Run Craigslist Scraper
            cl = CraigslistScraper()
            new_leads_data = cl.scrape()
            
            print(f"\n[PROCESSING] Processing {len(new_leads_data)} raw leads...")
            
            added_count = 0
            for data in new_leads_data:
                # Check for duplicates
                exists = self.session.query(Lead).filter_by(source_id=data['source_id']).first()
                if not exists:
                    new_lead = Lead(**data)
                    self.session.add(new_lead)
                    added_count += 1
            
            self.session.commit()
            print(f"✓ Database updated: {added_count} new leads added.")
    
        def export_csv(self):
            if not self.session: return
            leads = self.session.query(Lead).all()
            if not leads:
                print("No leads in database.")
                return
    
            # Convert to Pandas DataFrame for easy export
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
    
