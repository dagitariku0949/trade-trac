# 🎛️ Website Management Guide

## Overview

This guide shows you how to manage your trading dashboard website - adding features, removing components, updating content, and deploying changes.

## 🚀 Quick Management Commands

### Development Workflow
```bash
# 1. Start development server
cd backend
python app.py

# 2. Make changes to files
# 3. Test locally at http://localhost:5000

# 4. Commit and deploy
git add .
git commit -m "Your update description"
git push origin main
```

### Database Management
```bash
# Initialize new database
python setup_database.py

# Create migration for schema changes
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Reset database (development only)
rm database.db
python setup_database.py
```

## 🎨 Adding New Features

### 1. Frontend Components

**Add a new page/component:**
```bash
# Create new component file
touch frontend/js/components/newFeature.js

# Add to main app
# Edit frontend/js/app.js to include your component
```

**Example - Adding a new dashboard widget:**
```javascript
// frontend/js/components/portfolioWidget.js
export function renderPortfolioWidget(data) {
    const container = document.getElementById('portfolio-widget');
    container.innerHTML = `
        <div class="widget-card">
            <h3>Portfolio Overview</h3>
            <div class="portfolio-stats">
                <!-- Your widget content -->
            </div>
        </div>
    `;
}
```

### 2. Backend API Endpoints

**Add new API route:**
```python
# In backend/api_routes.py or backend/app.py
@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    # Your logic here
    return jsonify({'data': 'your_data'})
```

### 3. Database Models

**Add new database table:**
```python
# In backend/models.py
class Portfolio(Base):
    __tablename__ = 'portfolios'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    # Add your fields
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
```

**Create migration:**
```bash
alembic revision --autogenerate -m "Add portfolio table"
alembic upgrade head
```

## 🗑️ Removing Features

### 1. Remove Frontend Components
```bash
# Remove component file
rm frontend/js/components/unwantedFeature.js

# Remove from main app
# Edit frontend/js/app.js to remove references

# Remove CSS styles
# Edit frontend/css/styles.css to remove related styles
```

### 2. Remove Backend Routes
```python
# Comment out or delete routes in backend/app.py
# @app.route('/api/unwanted', methods=['GET'])
# def unwanted_endpoint():
#     pass
```

### 3. Remove Database Tables
```python
# Create migration to drop table
alembic revision -m "Remove unwanted table"

# In the migration file:
def upgrade():
    op.drop_table('unwanted_table')

def downgrade():
    # Recreate table if needed
    pass
```

## 🔄 Updating Existing Features

### 1. Update Frontend Styling
```css
/* In frontend/css/styles.css */
.existing-component {
    /* Update styles */
    background: new-color;
    border-radius: 12px;
}
```

### 2. Update API Responses
```python
# In backend/app.py or api_routes.py
@app.route('/api/trades', methods=['GET'])
def get_trades():
    # Add new fields to response
    return jsonify([{
        **trade.to_dict(),
        'new_field': 'new_value'
    } for trade in trades])
```

### 3. Update Database Schema
```bash
# Add new column to existing table
alembic revision --autogenerate -m "Add new column to trades"
alembic upgrade head
```

## 🌐 Deployment Management

### GitHub Pages (Frontend Only)
```bash
# Update docs folder for GitHub Pages
cp -r frontend/* docs/
git add docs/
git commit -m "Update GitHub Pages"
git push origin main
```

### Full Stack Deployment

#### Render.com
```bash
# Push to main branch triggers auto-deploy
git push origin main

# Manual deploy via Render dashboard
# https://dashboard.render.com
```

#### Heroku
```bash
# Deploy to Heroku
git push heroku main

# Run migrations on Heroku
heroku run alembic upgrade head

# View logs
heroku logs --tail
```

#### Railway
```bash
# Deploy to Railway
railway up

# Run migrations
railway run alembic upgrade head
```

## 🛠️ Admin Panel

Let me create an admin panel for easy website management: