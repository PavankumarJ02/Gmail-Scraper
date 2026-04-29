"""
Configuration settings for Gmail Scraper
"""

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Max number of emails to fetch at once
MAX_RESULTS = 10

# Credentials file path
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

# Email fetch settings
DEFAULT_QUERY = 'in:inbox'
