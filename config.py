"""Configuration for Handyman Lead Finder
Targets homeowners and businesses within 200 miles of Pittsburg, TX (75686)
that NEED handyman, repair, and maintenance services.
"""

import os
from datetime import datetime, timedelta

# Geographic Configuration
CENTER_ZIP = '75686'  # Pittsburg, TX
CENTER_COORDS = (32.97, -94.95)  # Latitude, Longitude
RADIUS_MILES = 200

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database/leads.db')
DATABASE_PATH = 'database/leads.db'

# Lead Search Keywords - PEOPLE/BUSINESSES NEEDING HANDYMAN SERVICES
# NOT other handyman companies
CRAIGSLIST_SEARCH_KEYWORDS = [
    'need handyman',
    'looking for handyman',
    'repair needed',
    'home repair',
    'fix broken',
    'leaky faucet',
    'roof repair',
    'drywall repair',
    'painting needed',
    'deck repair',
    'fence repair',
    'gutter repair',
    'door repair',
    'window repair',
    'appliance repair',
    'plumbing repair',
    'electrical repair',
    'tile work',
    'cabinet repair',
    'ASAP repair',
    'emergency repair',
    'handyman wanted',
    'reliable handyman',
    # Tech/Starlink additions
    'starlink',
    'satellite install',
    'internet setup',
    'tv mounting',
    'ethernet run'
]

# Lead Scoring Configuration
LEAD_SCORING = {
    'HOT': {
        'description': 'Priority: Clear need + Full contact info',
        'keywords_score': 25,
        'has_phone': True,
        'has_email_or_website': True,
        'distance_max_miles': 50,
        'posting_age_days': 7,
        'score_threshold': 80,
    },
    'WARM': {
        'description': 'Secondary: Likely customer + Partial contact',
        'keywords_score': 15,
        'has_phone': True,
        'has_email_or_website': False,
        'distance_max_miles': 100,
        'posting_age_days': 30,
        'score_threshold': 60,
    },
    'COLD': {
        'description': 'Lower priority: Generic or vague need',
        'keywords_score': 5,
        'has_phone': False,
        'has_email_or_website': False,
        'distance_max_miles': 200,
        'posting_age_days': 90,
        'score_threshold': 0,
    },
}

# Craigslist Configuration
CRAIGSLIST_REGIONS = [
    # East Texas regions
    'https://beaumont.craigslist.org',
    'https://tyler.craigslist.org',
    'https://longview.craigslist.org',
    'https://texarkana.craigslist.org',
    'https://centrallouisiana.craigslist.org',
    'https://northlouisiana.craigslist.org',
    'https://arklatex.craigslist.org',
    'https://houston.craigslist.org',  # Includes many surrounding areas
]

# Export Configuration
EXPORT_PATH = 'exports/'
EXPORT_FILENAME = f'handyman_leads_{datetime.now().strftime("%Y%m%d")}.csv'
