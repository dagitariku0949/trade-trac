# 🔧 Troubleshooting Guide

## Admin Panel Not Accessible

### Quick Solutions

#### Option 1: Simple Server (Recommended for Testing)
```bash
# Run simple HTTP server (no dependencies needed)
python simple_server.py
```
Then open: `http://localhost:8000/admin-standalone.html`

#### Option 2: Direct File Access
Open the file directly in your browser:
```
file:///C:/Users/YourName/Downloads/trading-dashboard/trading-dashboard-python/frontend/admin-standalone.html
```

#### Option 3: Full Backend Server
```bash
# Run the batch file (Windows)
start_server.bat

# Or manually:
cd backend
python app.py
```
Then open: `http://localhost:5000/admin.html`

## Common Issues & Solutions

### 1. "Site Can't Be Reached" Error

**Cause**: Backend server not running

**Solutions**:
- **Quick Fix**: Use `python simple_server.py` for frontend-only mode
- **Full Fix**: Install dependencies and start backend

### 2. Python Not Found

**Error**: `Python was not found`

**Solutions**:
1. **Install Python**: Download from [python.org](https://python.org)
2. **Add to PATH**: During installation, check "Add Python to PATH"
3. **Verify**: Open Command Prompt and type `python --version`

### 3. Package Installation Fails

**Error**: `Fatal error in launcher` or `pip not found`

**Solutions**:
```bash
# Try these alternatives:
python -m pip install flask flask-cors sqlalchemy
# or
py -m pip install flask flask-cors sqlalchemy
# or use the simple server (no packages needed)
python simple_server.py
```

### 4. Port Already in Use

**Error**: `Address already in use`

**Solutions**:
1. **Find what's using the port**:
   ```bash
   netstat -ano | findstr :5000
   ```
2. **Kill the process** or **use different port**
3. **Use simple server** (uses port 8000):
   ```bash
   python simple_server.py
   ```

### 5. Database Errors

**Error**: Database connection issues

**Solutions**:
1. **Use SQLite** (default, no setup needed)
2. **Reset database**:
   ```bash
   del database.db
   python setup_database.py
   ```
3. **Use frontend-only mode** for testing

## Server Options Comparison

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| **Simple Server** | No dependencies, quick start | Frontend only, no API | Testing UI, demos |
| **Flask Backend** | Full functionality, API access | Requires Python packages | Development, production |
| **Direct File** | Instant access | Limited functionality | Quick preview |

## Step-by-Step Setup

### For Complete Beginners

1. **Download Python**:
   - Go to [python.org](https://python.org)
   - Download Python 3.8 or newer
   - **Important**: Check "Add Python to PATH" during installation

2. **Test Python**:
   ```bash
   python --version
   ```
   Should show: `Python 3.x.x`

3. **Start Simple Server**:
   ```bash
   cd trading-dashboard-python
   python simple_server.py
   ```

4. **Open Admin Panel**:
   - Browser opens automatically
   - Or go to: `http://localhost:8000/admin-standalone.html`

### For Full Development Setup

1. **Install Dependencies**:
   ```bash
   cd trading-dashboard-python/backend
   pip install -r requirements.txt
   ```

2. **Setup Database**:
   ```bash
   cd ..
   python setup_database.py
   ```

3. **Start Backend**:
   ```bash
   cd backend
   python app.py
   ```

4. **Access Admin Panel**:
   `http://localhost:5000/admin.html`

## Alternative Access Methods

### 1. GitHub Pages (Live Demo)
Visit: `https://yourusername.github.io/trade-trac/admin-standalone.html`

### 2. Local File System
Navigate to your project folder and double-click:
`frontend/admin-standalone.html`

### 3. VS Code Live Server
If you have VS Code:
1. Install "Live Server" extension
2. Right-click `admin-standalone.html`
3. Select "Open with Live Server"

## Environment-Specific Issues

### Windows
- Use `python` command
- Run `start_server.bat` for automated setup
- Check Windows Defender/Firewall settings

### macOS/Linux
- May need `python3` instead of `python`
- Use `chmod +x *.py` to make scripts executable
- Check firewall settings

## Getting Help

### Check Status
```bash
python deploy.py status
```

### View Logs
```bash
# Simple server shows logs in terminal
# Flask backend shows logs in terminal
```

### Reset Everything
```bash
# Delete database and start fresh
del database.db  # Windows
rm database.db   # macOS/Linux

python setup_database.py
```

## Success Indicators

✅ **Simple Server Working**:
- Terminal shows "Server started successfully!"
- Browser opens automatically
- Can access admin panel at localhost:8000

✅ **Full Backend Working**:
- No error messages in terminal
- Can access http://localhost:5000
- Admin panel shows live data

✅ **Admin Panel Working**:
- Navigation buttons work
- Statistics show numbers
- No JavaScript errors in browser console

## Still Having Issues?

1. **Try Simple Server First**: `python simple_server.py`
2. **Check Browser Console**: F12 → Console tab for errors
3. **Verify File Paths**: Ensure you're in the right directory
4. **Use Direct File Access**: Open HTML files directly
5. **Check Antivirus**: May block local servers

The simple server option should work in 99% of cases and gives you full access to the admin panel interface! 🚀