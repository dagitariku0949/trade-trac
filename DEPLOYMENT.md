# Deployment Guide

## Deploy Backend to Render.com (Free)

### Step 1: Sign Up
1. Go to https://render.com
2. Sign up with your GitHub account

### Step 2: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `dagitariku0949/trade-trac`
3. Configure the service:
   - **Name**: `trading-dashboard-api` (or any name you like)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn app:app`
   - **Instance Type**: `Free`

### Step 3: Environment Variables (Optional)
Add these if needed:
- `PYTHON_VERSION`: `3.11.0`
- `PORT`: `10000` (Render uses this by default)

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. You'll get a URL like: `https://trading-dashboard-api.onrender.com`

### Step 5: Update Frontend
1. Copy your Render URL
2. Open `frontend/js/api.js`
3. Replace `'https://your-app-name.onrender.com/api'` with your actual URL
4. Example: `'https://trading-dashboard-api.onrender.com/api'`

### Step 6: Update GitHub Pages
```bash
cd trading-dashboard-python
xcopy frontend docs\ /E /I /Y
git add .
git commit -m "Update API URL for production"
git push
```

Wait 2-3 minutes and your site will be fully functional!

---

## Alternative: PythonAnywhere (Free)

### Step 1: Sign Up
1. Go to https://www.pythonanywhere.com
2. Create a free "Beginner" account

### Step 2: Upload Code
1. Go to "Files" tab
2. Upload your `backend` folder
3. Or use Git: `git clone https://github.com/dagitariku0949/trade-trac.git`

### Step 3: Create Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask"
4. Python version: 3.10
5. Set path to your `app.py`

### Step 4: Configure
1. Set working directory to your backend folder
2. Install requirements in Bash console:
   ```bash
   pip install -r requirements.txt
   ```

### Step 5: Reload
1. Click "Reload" button
2. Your API will be at: `https://yourusername.pythonanywhere.com`

---

## Alternative: Railway.app (Free)

### Step 1: Sign Up
1. Go to https://railway.app
2. Sign up with GitHub

### Step 2: Deploy
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose `dagitariku0949/trade-trac`
4. Railway auto-detects Python
5. Add start command: `cd backend && python app.py`

### Step 3: Get URL
1. Go to Settings → Domains
2. Generate domain
3. Copy the URL

---

## Testing Your Deployment

Once deployed, test your API:

```bash
# Replace with your actual URL
curl https://your-app.onrender.com/api/trades/stats/account
```

You should see JSON response with account stats.

---

## Important Notes

⚠️ **Free Tier Limitations:**
- Render: App sleeps after 15 min of inactivity (takes 30s to wake up)
- PythonAnywhere: Limited CPU time per day
- Railway: 500 hours/month free

💡 **Database:**
- Currently uses SQLite (file-based)
- Data persists on Render but may be lost on redeploys
- For production, consider upgrading to PostgreSQL

🔒 **Security:**
- Add authentication for production use
- Use environment variables for sensitive data
- Enable HTTPS (automatic on Render/Railway)

---

## Troubleshooting

**Backend not responding:**
- Check logs in Render dashboard
- Verify build command succeeded
- Check if service is running

**CORS errors:**
- Make sure Flask-CORS is installed
- Check CORS configuration in app.py

**Database errors:**
- SQLite file may not persist
- Consider using PostgreSQL for production
