/* Gmail Scraper Web Application - JavaScript */

let authenticatedUser = false;
let currentEmails = [];

// DOM Elements
const authBtn = document.getElementById('authBtn');
const authStatus = document.getElementById('authStatus');
const searchSection = document.getElementById('searchSection');
const searchBtn = document.getElementById('searchBtn');
const clearBtn = document.getElementById('clearBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const noResults = document.getElementById('noResults');
const errorMessage = document.getElementById('errorMessage');
const emailsList = document.getElementById('emailsList');
const resultCount = document.getElementById('resultCount');
const exportBtn = document.getElementById('exportBtn');
const emailModal = document.getElementById('emailModal');
const modalClose = document.querySelector('.modal-close');

// Event Listeners
authBtn.addEventListener('click', authenticate);
searchBtn.addEventListener('click', searchEmails);
clearBtn.addEventListener('click', clearForm);
exportBtn.addEventListener('click', exportResults);
modalClose.addEventListener('click', closeModal);

// Authenticate with Gmail
async function authenticate() {
    showSpinner(true);
    authBtn.disabled = true;

    try {
        const response = await fetch('/api/auth', {
            method: 'POST'
        });

        const data = await response.json();

        if (data.success) {
            authenticatedUser = true;
            showStatus(data.message, 'success');
            searchSection.style.display = 'block';
            authBtn.style.display = 'none';
            showSpinner(false);
        } else {
            showStatus(data.error || 'Authentication failed', 'error');
            authBtn.disabled = false;
            showSpinner(false);
        }
    } catch (error) {
        showStatus('Error: ' + error.message, 'error');
        authBtn.disabled = false;
        showSpinner(false);
    }
}

// Search Emails
async function searchEmails() {
    if (!authenticatedUser) {
        showError('Please authenticate first');
        return;
    }

    const keywords = document.getElementById('keywords').value
        .split(',')
        .map(k => k.trim())
        .filter(k => k);

    const filters = {
        'from': document.getElementById('fromFilter').value,
        'to': document.getElementById('toFilter').value,
        'subject': document.getElementById('subjectFilter').value,
        'label': document.getElementById('labelFilter').value,
        'after': document.getElementById('afterFilter').value,
        'before': document.getElementById('beforeFilter').value,
        'has_attachment': document.getElementById('hasAttachment').checked
    };

    const maxResults = document.getElementById('maxResults').value;

    if (!keywords.length && Object.values(filters).every(v => !v)) {
        showError('Please enter keywords or filters');
        return;
    }

    showSpinner(true);
    errorMessage.style.display = 'none';
    resultsSection.style.display = 'none';
    noResults.style.display = 'none';

    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                keywords,
                filters,
                max_results: maxResults
            })
        });

        const data = await response.json();

        showSpinner(false);

        if (data.success) {
            currentEmails = data.emails;
            displayResults(data);
        } else {
            showError(data.error || 'Search failed');
        }
    } catch (error) {
        showSpinner(false);
        showError('Error: ' + error.message);
    }
}

// Display Results
function displayResults(data) {
    if (data.emails.length === 0) {
        noResults.style.display = 'block';
        resultsSection.style.display = 'none';
        return;
    }

    resultsSection.style.display = 'block';
    resultCount.textContent = `Found ${data.total} email${data.total !== 1 ? 's' : ''}`;

    emailsList.innerHTML = '';

    data.emails.forEach((email, index) => {
        if (!email) return;

        const emailCard = document.createElement('div');
        emailCard.className = 'email-card';
        emailCard.innerHTML = `
            <h3>${escapeHtml(email.subject || 'No Subject')}</h3>
            <p><strong>From:</strong> ${escapeHtml(email.from || 'Unknown')}</p>
            <p><strong>To:</strong> ${escapeHtml(email.to || 'Unknown')}</p>
            <p>${escapeHtml(email.snippet || 'No preview available')}</p>
            <div class="email-meta">
                <div class="email-meta-item">${escapeHtml(email.date || 'Unknown Date')}</div>
                <div class="email-meta-item"><a href="#" onclick="openModal(${index}); return false;">View Full Email</a></div>
            </div>
        `;
        emailsList.appendChild(emailCard);
    });

    exportBtn.style.display = 'block';
}

// Open Email Modal
function openModal(index) {
    const email = currentEmails[index];
    if (!email) return;

    document.getElementById('modalSubject').textContent = email.subject || 'No Subject';
    document.getElementById('modalFrom').textContent = email.from || 'Unknown';
    document.getElementById('modalTo').textContent = email.to || 'Unknown';
    document.getElementById('modalDate').textContent = email.date || 'Unknown';
    document.getElementById('modalFullBody').textContent = email.full_body || 'No body content available';

    emailModal.style.display = 'flex';
}

// Close Modal
function closeModal() {
    emailModal.style.display = 'none';
}

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    if (event.target === emailModal) {
        closeModal();
    }
});

// Export Results
async function exportResults() {
    if (currentEmails.length === 0) {
        showError('No emails to export');
        return;
    }

    try {
        const response = await fetch('/api/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                emails: currentEmails
            })
        });

        const data = await response.json();

        if (data.success) {
            showSuccess(data.message);
        } else {
            showError(data.error || 'Export failed');
        }
    } catch (error) {
        showError('Error: ' + error.message);
    }
}

// Clear Form
function clearForm() {
    document.getElementById('keywords').value = '';
    document.getElementById('fromFilter').value = '';
    document.getElementById('toFilter').value = '';
    document.getElementById('subjectFilter').value = '';
    document.getElementById('labelFilter').value = '';
    document.getElementById('afterFilter').value = '';
    document.getElementById('beforeFilter').value = '';
    document.getElementById('hasAttachment').checked = false;
    document.getElementById('maxResults').value = '10';

    resultsSection.style.display = 'none';
    noResults.style.display = 'none';
    errorMessage.style.display = 'none';
}

// UI Helpers
function showSpinner(show) {
    loadingSpinner.style.display = show ? 'flex' : 'none';
}

function showStatus(message, type) {
    authStatus.textContent = message;
    authStatus.className = `status-message ${type}`;
}

function showError(message) {
    errorMessage.textContent = '❌ ' + message;
    errorMessage.style.display = 'block';
}

function showSuccess(message) {
    const msg = document.createElement('div');
    msg.className = 'error-message';
    msg.style.background = '#dcfce7';
    msg.style.color = '#166534';
    msg.textContent = '✓ ' + message;
    document.body.appendChild(msg);
    setTimeout(() => msg.remove(), 3000);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize
console.log('✓ Gmail Scraper Web Application loaded');
console.log('Waiting for authentication...');
