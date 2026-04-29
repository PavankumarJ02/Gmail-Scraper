"""
Example usage of Gmail Scraper with different scenarios
"""

from gmail_scraper import GmailScraper


def example_1_simple_keyword_search():
    """Example 1: Simple keyword search"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Simple Keyword Search")
    print("="*80)

    scraper = GmailScraper()
    scraper.add_keywords(['project', 'update'])
    emails = scraper.fetch_emails(max_results=5)
    scraper.display_emails(emails)


def example_2_search_from_sender():
    """Example 2: Search emails from specific sender"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Search from Specific Sender")
    print("="*80)

    scraper = GmailScraper()
    scraper.add_filters({
        'from': 'boss@company.com'
    })
    emails = scraper.fetch_emails(max_results=10)
    scraper.display_emails(emails)
    scraper.save_results(emails, 'emails_from_boss.json')


def example_3_recent_important_emails():
    """Example 3: Find recent important emails with attachments"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Recent Important Emails with Attachments")
    print("="*80)

    scraper = GmailScraper()
    scraper.add_keywords(['important', 'urgent'])
    scraper.add_filters({
        'has_attachment': True,
        'after': '2024-01-01'
    })
    emails = scraper.fetch_emails(max_results=15)
    scraper.display_emails(emails)
    scraper.save_results(emails, 'important_emails_with_attachments.json')


def example_4_subject_based_search():
    """Example 4: Search by specific subject"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Subject-Based Search")
    print("="*80)

    scraper = GmailScraper()
    scraper.add_filters({
        'subject': 'Meeting',
        'after': '2024-01-01'
    })
    emails = scraper.fetch_emails(max_results=8)
    scraper.display_emails(emails)


def example_5_complex_filters():
    """Example 5: Complex filtering with multiple criteria"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Complex Filtering")
    print("="*80)

    scraper = GmailScraper()
    scraper.add_keywords(['invoice', 'receipt', 'payment'])
    scraper.add_filters({
        'from': 'finance@company.com',
        'has_attachment': True,
        'after': '2024-01-01',
        'before': '2024-12-31'
    })
    emails = scraper.fetch_emails(max_results=20)
    scraper.display_emails(emails)
    scraper.save_results(emails, 'finance_emails.json')


def example_6_label_based_search():
    """Example 6: Search emails by label"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Label-Based Search")
    print("="*80)

    scraper = GmailScraper()
    scraper.add_filters({
        'label': 'Work'
    })
    emails = scraper.fetch_emails(max_results=12)
    scraper.display_emails(emails)


if __name__ == '__main__':
    # Run examples
    # Uncomment the example you want to run
    
    # example_1_simple_keyword_search()
    # example_2_search_from_sender()
    # example_3_recent_important_emails()
    # example_4_subject_based_search()
    example_5_complex_filters()
    # example_6_label_based_search()
