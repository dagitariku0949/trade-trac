# Trading Dashboard - Python Backend

A comprehensive trading dashboard with HTML/CSS/JavaScript frontend and Python Flask backend.

## Features

- Real-time trading metrics (Profit Factor, Win Rate, etc.)
- Confluence tracking across 5 timeframes
- Account management and P&L tracking
- Interactive charts and visualizations
- Trade management (Add, Edit, Close, Delete)
- Daily performance analytics

## Tech Stack

**Frontend:**
- HTML5
- CSS3 (with modern styling)
- Vanilla JavaScript
- Chart.js for visualizations

**Backend:**
- Python 3.8+
- Flask web framework
- SQLite database
- RESTful API

## Quick Start

1. **Backend Setup:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

2. **Frontend:**
```bash
cd frontend
# Open index.html in browser or use live server
```

## Project Structure

```
trading-dashboard-python/
├── backend/
│   ├── app.py              # Flask application
│   ├── models.py           # Database models
│   ├── routes/             # API routes
│   ├── database.db         # SQLite database
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html          # Main HTML file
│   ├── css/
│   │   └── styles.css      # Styling
│   ├── js/
│   │   ├── app.js          # Main application logic
│   │   ├── api.js          # API client
│   │   └── components/     # UI components
│   └── assets/             # Images, icons
└── README.md
```