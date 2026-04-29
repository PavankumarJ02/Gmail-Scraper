"""
Gmail Scraper with keyword filtering and email fetching capabilities
"""

import os
import pickle
import base64
import json
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import discovery
from config import SCOPES, CREDENTIALS_FILE, TOKEN_FILE, DEFAULT_QUERY, MAX_RESULTS


class GmailScraper:
    def __init__(self):
        self.service = None
        self.keywords = []
        self.filters = {}
        self.authenticate()

    def authenticate(self):
        """Authenticate with Gmail API using OAuth2"""
        creds = None

        # Load token.pickle if exists
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, create new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(CREDENTIALS_FILE):
                    raise FileNotFoundError(
                        f"{CREDENTIALS_FILE} not found. Please download it from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save token for future use
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        self.service = discovery.build('gmail', 'v1', credentials=creds)
        print("✓ Successfully authenticated with Gmail API")

    def add_keywords(self, keywords):
        """Add keywords to filter emails"""
        if isinstance(keywords, str):
            keywords = [keywords]
        self.keywords = keywords
        print(f"✓ Keywords added: {', '.join(keywords)}")

    def add_filters(self, filters_dict):
        """
        Add email filters
        Example: {'from': 'sender@example.com', 'subject': 'keyword', 'before': '2024-01-01'}
        """
        self.filters = filters_dict
        print(f"✓ Filters added: {json.dumps(filters_dict, indent=2)}")

    def build_query(self):
        """Build Gmail query based on keywords and filters"""
        query_parts = []

        # Add keyword searches
        if self.keywords:
            keyword_query = ' OR '.join([f'"{kw}"' for kw in self.keywords])
            query_parts.append(f"({keyword_query})")

        # Add filters
        if self.filters:
            for key, value in self.filters.items():
                if key == 'from':
                    query_parts.append(f'from:{value}')
                elif key == 'to':
                    query_parts.append(f'to:{value}')
                elif key == 'subject':
                    query_parts.append(f'subject:"{value}"')
                elif key == 'before':
                    query_parts.append(f'before:{value}')
                elif key == 'after':
                    query_parts.append(f'after:{value}')
                elif key == 'has_attachment':
                    if value:
                        query_parts.append('has:attachment')
                elif key == 'label':
                    query_parts.append(f'label:{value}')

        query = ' '.join(query_parts) if query_parts else DEFAULT_QUERY
        return query

    def fetch_emails(self, max_results=MAX_RESULTS):
        """
        Fetch emails based on keywords and filters
        
        Args:
            max_results: Maximum number of emails to fetch
            
        Returns:
            List of email messages
        """
        try:
            query = self.build_query()
            print(f"\n🔍 Searching with query: {query}")

            # Get email IDs
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            print(f"✓ Found {len(messages)} emails")

            if not messages:
                print("No emails found matching your criteria.")
                return []

            # Get full email details
            emails = []
            for msg in messages:
                email_data = self.get_email_details(msg['id'])
                emails.append(email_data)

            return emails

        except Exception as e:
            print(f"✗ Error fetching emails: {str(e)}")
            return []

    def get_email_details(self, msg_id):
        """Get detailed information about a specific email"""
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()

            headers = message['payload'].get('headers', [])
            body = self.get_email_body(message['payload'])

            email_data = {
                'id': msg_id,
                'subject': self.get_header_value(headers, 'Subject'),
                'from': self.get_header_value(headers, 'From'),
                'to': self.get_header_value(headers, 'To'),
                'date': self.get_header_value(headers, 'Date'),
                'body': body[:500],  # First 500 chars
                'snippet': message.get('snippet', ''),
                'full_body': body
            }
            return email_data

        except Exception as e:
            print(f"✗ Error getting email details: {str(e)}")
            return None

    def get_header_value(self, headers, name):
        """Extract header value by name"""
        for header in headers:
            if header['name'] == name:
                return header['value']
        return ''

    def get_email_body(self, payload):
        """Extract email body from payload"""
        try:
            if 'parts' in payload:
                parts = payload['parts']
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        data = part['body'].get('data', '')
                        if data:
                            return base64.urlsafe_b64decode(data).decode('utf-8')
            else:
                data = payload.get('body', {}).get('data', '')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8')
        except Exception as e:
            print(f"✗ Error extracting body: {str(e)}")

        return ''

    def display_emails(self, emails):
        """Display fetched emails in formatted manner"""
        if not emails:
            print("No emails to display.")
            return

        print("\n" + "="*80)
        print(f"{'TOTAL EMAILS FOUND:'} {len(emails)}")
        print("="*80)

        for idx, email in enumerate(emails, 1):
            if not email:
                continue

            print(f"\n📧 Email #{idx}")
            print(f"From: {email.get('from', 'N/A')}")
            print(f"To: {email.get('to', 'N/A')}")
            print(f"Subject: {email.get('subject', 'N/A')}")
            print(f"Date: {email.get('date', 'N/A')}")
            print(f"Preview: {email.get('snippet', 'N/A')[:100]}...")
            print("-"*80)

    def save_results(self, emails, filename='scraped_emails.json'):
        """Save scraped emails to JSON file"""
        try:
            # Convert datetime objects to strings if needed
            data = {
                'total': len(emails),
                'timestamp': datetime.now().isoformat(),
                'filters': self.filters,
                'keywords': self.keywords,
                'emails': emails
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"\n✓ Results saved to {filename}")
        except Exception as e:
            print(f"✗ Error saving results: {str(e)}")


def main():
    """Main function demonstrating Gmail Scraper usage"""
    print("=" * 80)
    print("GMAIL SCRAPER - KEYWORD SEARCH & FILTER")
    print("=" * 80)

    try:
        # Initialize scraper
        scraper = GmailScraper()

        # Example 1: Search by keywords
        print("\n--- EXAMPLE 1: Search by Keywords ---")
        scraper.add_keywords(['invoice', 'payment'])
        emails = scraper.fetch_emails(max_results=10)
        scraper.display_emails(emails)
        scraper.save_results(emails, 'emails_by_keywords.json')

        # Example 2: Search with filters
        print("\n\n--- EXAMPLE 2: Search with Filters ---")
        scraper_2 = GmailScraper()
        scraper_2.add_keywords(['confirm'])
        scraper_2.add_filters({
            'has_attachment': True,
            'after': '2024-01-01'
        })
        emails_2 = scraper_2.fetch_emails(max_results=10)
        scraper_2.display_emails(emails_2)
        scraper_2.save_results(emails_2, 'emails_with_filters.json')

        # Example 3: Search from specific sender
        print("\n\n--- EXAMPLE 3: Search from Specific Sender ---")
        scraper_3 = GmailScraper()
        scraper_3.add_filters({
            'from': 'example@gmail.com'
        })
        emails_3 = scraper_3.fetch_emails(max_results=5)
        scraper_3.display_emails(emails_3)

    except Exception as e:
        print(f"✗ Error: {str(e)}")


if __name__ == '__main__':
    main()
