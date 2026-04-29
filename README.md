# Gmail Scraper - Professional Web Application

A professional-grade Gmail scraper web application with an intuitive user interface, keyword searching, email fetching, and advanced filtering capabilities.

## Features

✨ **Keyword Search** - Search emails by keywords with intuitive web interface
🔍 **Advanced Filters** - Filter by sender, subject, date range, attachments, and labels
📧 **Email Extraction** - View full email details with formatted preview
💾 **Export Results** - Export search results to JSON format
🔐 **OAuth2 Authentication** - Secure authentication with Gmail API
🌐 **Beautiful Web Dashboard** - Professional responsive UI for easy email management
📱 **Mobile Friendly** - Works seamlessly on desktop and mobile devices

## Prerequisites

- Python 3.7+
- Gmail account with 2FA enabled (recommended)
- Google Cloud project with Gmail API enabled

## Setup Instructions

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API"
   - Click on it and press "Enable"

### Step 2: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client ID"
3. Select "Desktop application"
4. Download the credentials JSON file
5. Save it as `credentials.json` in the project directory

### Step 3: Install Dependencies

Using pip:
```bash
pip install -r requirements.txt
```

Or using uv (faster):
```bash
uv sync
```

### Step 4: Run the Web Application

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

You should see the Gmail Scraper dashboard!

## Usage

### Web Dashboard (Recommended)

1. **Run the application:**
   ```bash
   python app.py
   ```

2. **Open your browser:**
   Navigate to http://localhost:5000

3. **Authenticate:**
   - Click "Authenticate with Gmail" button
   - You'll be redirected to Google login
   - Grant permissions to access your Gmail

4. **Search & Filter:**
   - Enter keywords in the search box
   - Use advanced filters for precise searches:
     - From/To email addresses
     - Subject text
     - Date range
     - Attachment status
     - Gmail labels
   - Click "Search Emails"

5. **View Results:**
   - Browse email cards in the results grid
   - Click "View Full Email" to see complete message
   - Click "Export to JSON" to save results

### Command-Line Interface (Alternative)

For programmatic usage, see [example_usage.py](d:\scraper\example_usage.py)

## Filter Options

| Filter | Description | Example |
|--------|-------------|---------|
| `from` | Email sender | `'from': 'user@example.com'` |
| `to` | Email recipient | `'to': 'user@example.com'` |
| `subject` | Email subject | `'subject': 'Meeting'` |
| `before` | Before date (YYYY-MM-DD) | `'before': '2024-12-31'` |
| `after` | After date (YYYY-MM-DD) | `'after': '2024-01-01'` |
| `has_attachment` | Has attachments | `'has_attachment': True` |
| `label` | Gmail label | `'label': 'IMPORTANT'` |

## File Structure

```
scraper/
├── requirements.txt       # Python dependencies
├── config.py             # Configuration settings
├── gmail_scraper.py      # Main scraper class
├── credentials.json      # OAuth credentials (download from Google Cloud)
├── token.pickle         # OAuth token (auto-generated on first run)
└── README.md            # This file
```

## Output

### Web Dashboard Display
- Email cards with sender, subject, and preview
- Click any email to view full content in modal
- Export all results as JSON file

### JSON Export Format

```json
{
  "total": 5,
  "timestamp": "2024-01-15T10:30:00.123456"           # OAuth credentials (from Google Cloud)
├── token.pickle                    # OAuth token (auto-generated)
├── templates/
│   └── index.html                  # Web dashboard HTML
├── static/
│   ├── styles.css                  # Dashboard styling
│   └── script.js                   # Dashboard JavaScript
└── exports/                        # Exported results folder
    "from": "example@gmail.com"
  },
  "keywords": ["invoice"],
  "emails": [
    {
      "id": "msg123",
      "subject": "Invoice #001",
      "from": "sender@example.com",
      "to": "recipient@example.com",
      "date": "Mon, 15 Jan 2024 10:00:00 +0000",
      "body": "Preview of email body...",
      "snippet": "Email snippet...",
      "full_body": "Complete email body..."
    }
  ]
}
```
Troubleshooting

### "credentials.json not found"
- Make sure you've downloaded the OAuth credentials from Google Cloud Console
- Save it as `credentials.json` in the project directory

### "Gmail API not enabled"
- Go to Google Cloud Console > APIs & Services > Library
- Search for "Gmail API" and enable it

### "Access denied" or "Invalid grant"
- Delete `token.pickle` and run `python app.py` again
- YAcademic Project Features

This project demonstrates:

✅ **Web Application Development** - Flask-based full-stack application
✅ **OAuth 2.0 Authentication** - Secure API authentication
✅ **RESTful API Design** - Clean API endpoints for frontend communication
✅ **Frontend Development** - HTML5, CSS3, JavaScript ES6+
✅ **Responsive Design** - Mobile-friendly UI
✅ **Error Handling** - Comprehensive error management
✅ **Data Management** - JSON export and handling
✅ **Security** - XSS protection, secure credential handling
✅ **Professional Code** - Well-documented, modular architecture

## Technologies Used

- **Backend:** Python, Flask, Google Gmail API
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Authentication:** OAuth 2.0
- **Package Manager:** uv (optional, pip also works)
- **APIs:** RESTful design patterns

## Project Stats

- **Lines of Code:** ~2000+
- **Modules:** 5 core files
- **Frontend Components:** Dynamic email cards, modal views
- **API Endpoints:** 4 RESTful endpoints
- **Supported Filters:** 7+ filter types
4. **Check attachments** - Has_attachment filter is quick
5. **Use labels** - Label-based searches are optimized by Gmail
Delete `token.pickle` and run the script again to re-authenticate.

## Security Notes

- Keep `credentials.json` and `token.pickle` private
- Never commit them to version control
- Add them to `.gitignore`

## Limitations

- Only reads emails (doesn't send or modify)
- Limited to 500 emails per request by default
- Rate limited by Google's API quotas

## License

MIT License

## Support

For issues with the Gmail API, visit: https://developers.google.com/gmail/api
