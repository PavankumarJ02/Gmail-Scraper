"""
Flask Web Application for Gmail Scraper
Main application entry point
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from gmail_scraper import GmailScraper

app = Flask(__name__)
CORS(app)

# Store scraper instance
scraper_instance = None


@app.route('/')
def index():
    """Render main dashboard"""
    return render_template('index.html')


@app.route('/api/auth', methods=['POST'])
def authenticate():
    """Initialize Gmail Scraper authentication"""
    global scraper_instance
    try:
        scraper_instance = GmailScraper()
        return jsonify({
            'success': True,
            'message': 'Successfully authenticated with Gmail API'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/search', methods=['POST'])
def search_emails():
    """Search emails based on keywords and filters"""
    if scraper_instance is None:
        return jsonify({
            'success': False,
            'error': 'Not authenticated. Please authenticate first.'
        }), 400

    try:
        data = request.json
        keywords = data.get('keywords', [])
        filters = data.get('filters', {})
        max_results = data.get('max_results', 10)

        # Convert max_results to int
        max_results = min(int(max_results), 100)  # Cap at 100

        # Clean filters (remove empty values)
        filters = {k: v for k, v in filters.items() if v}

        # Add keywords and filters
        if keywords:
            scraper_instance.add_keywords(keywords)
        if filters:
            scraper_instance.add_filters(filters)

        # Fetch emails
        emails = scraper_instance.fetch_emails(max_results=max_results)

        return jsonify({
            'success': True,
            'total': len(emails),
            'emails': emails,
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/export', methods=['POST'])
def export_results():
    """Export search results to JSON"""
    try:
        data = request.json
        emails = data.get('emails', [])
        filename = f"gmail_scraper_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        export_data = {
            'total': len(emails),
            'timestamp': datetime.now().isoformat(),
            'emails': emails
        }

        # Save to file
        filepath = os.path.join('exports', filename)
        os.makedirs('exports', exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        return jsonify({
            'success': True,
            'message': f'Results exported to {filename}',
            'filename': filename
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'authenticated': scraper_instance is not None
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('exports', exist_ok=True)
    
    print("=" * 80)
    print("🚀 GMAIL SCRAPER WEB APPLICATION")
    print("=" * 80)
    print("\n✨ Starting Flask server...")
    print("🌐 Open your browser: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='localhost', port=5000)
