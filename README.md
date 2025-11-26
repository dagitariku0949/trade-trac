# 🚀 Professional Trading Dashboard

A comprehensive trading journal and analytics platform with advanced SQL database, interactive calendar, and professional management tools.

## ✨ Key Features

- **Interactive Monthly Calendar** - Visual trading performance heatmap with clickable days
- **Multi-Database Support** - SQLite, PostgreSQL, MySQL with automatic migrations
- **Advanced Analytics** - Performance metrics, risk analysis, drawdown tracking
- **Multi-Account Management** - Track demo and live accounts separately
- **Strategy Performance** - Analyze and compare trading strategies
- **Professional Admin Panel** - Easy website management interface
- **One-Click Deployment** - GitHub Pages, Render, Heroku support
- **Enhanced Trade Tracking** - Stop loss, take profit, sessions, quality ratings

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone and setup
git clone <your-repo>
cd trading-dashboard-python

# Setup management tools
python setup_management.py

# Initialize database
python setup_database.py
```

### 2. Start Development
```bash
# Start backend
cd backend
python app.py

# Open in browser
# Frontend: http://localhost:5000
# Admin Panel: http://localhost:5000/admin.html
```

### 3. Deploy
```bash
# Deploy frontend to GitHub Pages
python deploy.py frontend

# Deploy full stack to Render
python deploy.py render
```

## 🎛️ Website Management

### Easy Management Commands
```bash
# Add new component
python manage.py add-component portfolio widget

# Add new API endpoint  
python manage.py add-endpoint user-stats GET

# Add database model
python manage.py add-model UserProfile name:string,age:integer

# Deploy changes
python deploy.py frontend

# Check status
python deploy.py status
```

### NPM Scripts (Optional)
```bash
npm run setup          # Setup database
npm run dev            # Start development server
npm run deploy         # Deploy to GitHub Pages
npm run add:component  # Add new component
npm run status         # Check deployment status
```

## 🗄️ Database Management

### Supported Databases
- **SQLite** (Development) - Default, no setup required
- **PostgreSQL** (Production) - Recommended for production
- **MySQL** - Alternative production option

### Configuration
```bash
# Copy environment template
cp .env.example backend/.env

# Edit database settings
# For PostgreSQL:
DB_TYPE=postgresql
DB_HOST=localhost
DB_NAME=trading_dashboard
DB_USER=your_user
DB_PASSWORD=your_password
```

### Migrations
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Or use management tool
python manage.py migrate
```

## 🎨 Adding Features

### 1. Frontend Components
```bash
# Create new widget
python manage.py add-component risk-meter widget

# Create new page
python manage.py add-component settings page
```

### 2. API Endpoints
```bash
# Add GET endpoint
python manage.py add-endpoint portfolio-summary GET

# Add POST endpoint  
python manage.py add-endpoint update-settings POST
```

### 3. Database Models
```bash
# Add new model
python manage.py add-model Portfolio name:string,balance:float,active:boolean

# Run migrations
python manage.py migrate
```

## 🚀 Deployment Options

### GitHub Pages (Frontend Only)
```bash
python deploy.py frontend
```
- Automatically syncs frontend to `docs/` folder
- Deploys to GitHub Pages
- Perfect for demo/portfolio sites

### Render.com (Full Stack)
```bash
python deploy.py render
```
- Deploys both frontend and backend
- Automatic PostgreSQL database
- Free tier available

### Heroku (Full Stack)
```bash
python deploy.py heroku
```
- Full stack deployment
- Add-on PostgreSQL database
- Automatic scaling

## 🛠️ Admin Panel Features

Access at `http://localhost:5000/admin.html`

- **System Overview** - Statistics and health checks
- **Account Management** - Add/edit trading accounts
- **Strategy Management** - Create and analyze strategies
- **Tag Management** - Organize trades with tags
- **Database Tools** - Backup, restore, migrations
- **Deployment Control** - One-click deployments

## 📊 Advanced Analytics

### Performance Metrics
- Profit factor and win rate
- Sharpe ratio calculation
- Maximum drawdown analysis
- Consecutive loss tracking

### Risk Management
- Position sizing analysis
- Risk percentage tracking
- Drawdown monitoring
- Loss streak analysis

### Strategy Analysis
- Performance by strategy
- Win rate by setup quality
- Session-based performance
- Symbol-specific metrics

## 🔧 Development Workflow

### 1. Make Changes
```bash
# Edit files in frontend/ or backend/
# Test locally at http://localhost:5000
```

### 2. Commit & Deploy
```bash
git add .
git commit -m "Your changes"
python deploy.py frontend  # or render/heroku
```

### 3. Manage Features
```bash
# Add new features
python manage.py add-component new-feature

# Remove features  
python manage.py remove-component old-feature

# Update database
python manage.py migrate
```

## 📁 Project Structure

```
trading-dashboard-python/
├── frontend/           # Frontend files
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript
│   ├── admin.html     # Admin panel
│   └── index.html     # Main app
├── backend/           # Python backend
│   ├── app.py         # Main Flask app
│   ├── models.py      # Database models
│   ├── api_routes.py  # API endpoints
│   └── database.py    # Database config
├── docs/              # GitHub Pages files
├── migrations/        # Database migrations
├── manage.py          # Management CLI
├── deploy.py          # Deployment tool
└── setup_database.py # Database setup
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test locally
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature-name`
6. Create Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Documentation**: Check `DATABASE_UPGRADE.md` and `WEBSITE_MANAGEMENT.md`
- **Issues**: Create GitHub issue with details
- **Admin Panel**: Use built-in tools for management

---

**Built with ❤️ for serious traders who value discipline and data-driven insights**