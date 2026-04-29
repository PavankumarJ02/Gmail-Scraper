# Quick Start Guide - Gmail Scraper Web Application

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.8+
- Gmail account
- Google Cloud project with Gmail API enabled

### Step 1: Get Credentials (2 min)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable "Gmail API" from the library
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID" (Desktop)
5. Download the JSON file and save as `credentials.json` in project folder

### Step 2: Install & Run (3 min)

```bash
# Navigate to project
cd d:\scraper

# Install dependencies
uv sync
# OR: pip install -r requirements.txt

# Run the app
python app.py
```

### Step 3: Use the Web App

- Browser opens: **http://localhost:5000**
- Click "Authenticate with Gmail"
- Google login appears → Allow access
- Start searching!

## 🎯 Common Use Cases

### Find Invoices
- Keywords: `invoice, receipt, payment`
- Filter: Has Attachment = ON
- Export as JSON

### Search from Specific Sender
- Filter: From = `boss@company.com`
- Search all their emails

### Recent Important Emails
- Keywords: `urgent, important`
- Filter: After = `2024-01-01`
- Has Attachment = ON

### Project Emails
- Filter: Label = `Work`
- Keywords: `project, update`

## 📊 Features at a Glance

| Feature | How to Use |
|---------|-----------|
| **Keyword Search** | Type comma-separated keywords |
| **Date Range** | Set "After" and "Before" dates |
| **Sender/Recipient** | Enter email in From/To fields |
| **Subject Filter** | Type subject text |
| **Attachments** | Check "Has Attachment" box |
| **View Email** | Click "View Full Email" link |
| **Export Results** | Click "Export to JSON" button |

## 🆘 Troubleshooting

**"credentials.json not found"**
→ Download from Google Cloud Console → Save in project folder

**"Port 5000 already in use"**
→ Change port in `app.py` line (last line): `port=8000`

**"Access denied"**
→ Delete `token.pickle` and restart app

**"No emails found"**
→ Check your filters are correct
→ Try broader search terms

## 📂 Project Structure

```
d:\scraper\
├── app.py                      # Start here!
├── gmail_scraper.py            # Core logic
├── templates/index.html        # Web interface
├── static/styles.css           # Styling
├── static/script.js            # Frontend logic
├── credentials.json            # Download from Google
└── README.md                   # Full documentation
```

## 💡 Pro Tips

✓ More specific keywords = faster results
✓ Use date filters to narrow search scope
✓ Start with `max_results=10` then increase
✓ Check "Has Attachment" if you know email has files
✓ Use Gmail labels for organized searches

## 🎓 For Faculty Presentation

**What to Show:**
1. Web interface - clean, professional UI
2. Authentication flow - OAuth2 implementation
3. Search functionality with filters
4. Results display in card format
5. Modal view for full email content
6. JSON export capability

**Demo Workflow:**
1. Run `python app.py`
2. Open http://localhost:5000
3. Click "Authenticate with Gmail"
4. Search for emails (e.g., keywords: "meeting")
5. Click on email card to view details
6. Export results to JSON
7. Show exported file structure

**Code Quality Points:**
- RESTful API design
- Error handling
- Security (XSS prevention)
- Responsive design
- Well-documented code
- Separation of concerns

## 📝 Need Help?

See full documentation in [README.md](README.md)

Good luck with your presentation! 🎉
