# 🚀 Database Upgrade Guide

## Overview

Your trading dashboard has been upgraded with a powerful SQL database system supporting multiple database types and advanced features.

## 🆕 New Features

### Enhanced Database Support
- **SQLite** (Development) - Default, no setup required
- **PostgreSQL** (Production Recommended) - Best performance and features
- **MySQL** (Alternative) - Widely supported option

### New Models & Features
- **Multi-Account Support** - Track multiple trading accounts
- **Trading Strategies** - Organize trades by strategy
- **Trade Tags** - Categorize trades with custom tags
- **Trade Images** - Attach screenshots and charts
- **Advanced Analytics** - Performance metrics and risk analysis
- **Enhanced Trade Fields** - Stop loss, take profit, sessions, quality ratings

## 🛠️ Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Choose Your Database

#### Option A: SQLite (Development - Default)
No additional setup required. Uses local `database.db` file.

#### Option B: PostgreSQL (Production Recommended)

**Install PostgreSQL:**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

**Create Database:**
```sql
CREATE DATABASE trading_dashboard;
CREATE USER trader WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE trading_dashboard TO trader;
```

**Configure Environment:**
```bash
cp .env.example .env
# Edit .env file:
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=trading_dashboard
DB_USER=trader
DB_PASSWORD=your_password
```

#### Option C: MySQL

**Install MySQL:**
```bash
# Ubuntu/Debian
sudo apt-get install mysql-server

# macOS
brew install mysql

# Windows
# Download from https://dev.mysql.com/downloads/mysql/
```

**Create Database:**
```sql
CREATE DATABASE trading_dashboard;
CREATE USER 'trader'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON trading_dashboard.* TO 'trader'@'localhost';
```

**Configure Environment:**
```bash
cp .env.example .env
# Edit .env file:
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=trading_dashboard
DB_USER=trader
DB_PASSWORD=your_password
```

### 3. Initialize Database

```bash
python setup_database.py
```

This will:
- Create all database tables
- Add default trading account
- Create sample strategies
- Add default trade tags

### 4. Run Migrations (Optional)

For production environments, use Alembic for database migrations:

```bash
# Initialize migrations (first time only)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## 🔧 Environment Variables

Create a `.env` file in the backend directory:

```env
# Database Configuration
DB_TYPE=postgresql  # or mysql, sqlite
DB_HOST=localhost
DB_PORT=5432
DB_NAME=trading_dashboard
DB_USER=your_username
DB_PASSWORD=your_password

# Or use a full database URL
# DATABASE_URL=postgresql://user:password@localhost:5432/trading_dashboard

# Application Settings
FLASK_ENV=development
SQL_DEBUG=False
SECRET_KEY=your-secret-key-here
```

## 📊 New API Endpoints

### Trading Accounts
- `GET /api/accounts` - List all accounts
- `POST /api/accounts` - Create new account
- `PUT /api/accounts/{id}` - Update account

### Trading Strategies
- `GET /api/strategies` - List all strategies
- `POST /api/strategies` - Create new strategy
- `GET /api/strategies/{id}/performance` - Strategy performance

### Trade Tags
- `GET /api/tags` - List all tags
- `POST /api/tags` - Create new tag

### Enhanced Analytics
- `GET /api/analytics/performance` - Advanced performance metrics
- `GET /api/analytics/risk` - Risk management analytics

## 🔄 Migration from Old System

If you have existing trades in the old system, they will be automatically migrated to the new enhanced structure with default values.

## 🚀 Production Deployment

### Render.com (PostgreSQL)
```yaml
# render.yaml
services:
  - type: web
    name: trading-dashboard
    env: python
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "cd backend && python app.py"
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: trading-dashboard-db
          property: connectionString

databases:
  - name: trading-dashboard-db
    databaseName: trading_dashboard
    user: trader
```

### Heroku (PostgreSQL)
```bash
# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SQL_DEBUG=False
```

### Railway (PostgreSQL)
```bash
# Add PostgreSQL service
railway add postgresql

# Deploy
railway up
```

## 🔍 Troubleshooting

### Connection Issues
1. Check database is running
2. Verify credentials in `.env`
3. Ensure database exists
4. Check firewall settings

### Migration Issues
```bash
# Reset migrations (development only)
rm -rf migrations/versions/*
alembic revision --autogenerate -m "Fresh start"
alembic upgrade head
```

### Performance Issues
- Add database indexes for frequently queried fields
- Use connection pooling for high traffic
- Consider read replicas for analytics

## 📈 Performance Benefits

- **Faster Queries** - Proper indexing and relationships
- **Data Integrity** - Foreign key constraints and validation
- **Scalability** - Support for thousands of trades
- **Advanced Analytics** - Complex queries and aggregations
- **Concurrent Access** - Multiple users and sessions

## 🛡️ Security Features

- **SQL Injection Protection** - SQLAlchemy ORM
- **Connection Pooling** - Efficient resource usage
- **Environment Variables** - Secure credential storage
- **Database Migrations** - Version controlled schema changes

Your trading dashboard is now enterprise-ready with professional database capabilities! 🎉