# Complete Deployment Guide - Backend & Frontend

This guide covers deploying both the Flask backend and React frontend to production.

## 🚀 Quick Deploy Options

### Option 1: Railway (Recommended - Easiest)
**Best for**: Quick deployment, automatic HTTPS, free tier available

### Option 2: Render
**Best for**: Simple setup, GitHub integration, free tier

### Option 3: Vercel (Frontend) + Railway (Backend)
**Best for**: Optimized frontend hosting, separate scaling

---

## 📦 Option 1: Railway Deployment (Full Stack)

Railway is the easiest option - it auto-detects Dockerfiles and deploys automatically.

### Prerequisites
1. GitHub account
2. Railway account: https://railway.app

### Step 1: Deploy Backend

1. **Go to Railway**: https://railway.app
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Choose your repository**: `Nagarkova/cursor_module8_flask_react`
5. **Select "backend" as root directory**:
   - Click on the service
   - Go to Settings → Root Directory
   - Set to: `backend`
6. **Railway will auto-detect Dockerfile** and start building
7. **Set Environment Variables**:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key-here
   PORT=5001
   ```
8. **Get Backend URL**: Railway will provide a URL like `https://your-backend.up.railway.app`

### Step 2: Deploy Frontend

1. **Add New Service** in Railway project
2. **Select "Deploy from GitHub repo"** (same repo)
3. **Set Root Directory** to: `frontend`
4. **Set Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-backend.up.railway.app
   ```
5. **Set Build Command**:
   ```
   npm ci && npm run build
   ```
6. **Set Start Command**:
   ```
   npx serve -s build -l 80
   ```
   OR use Dockerfile (already configured)

### Step 3: Configure CORS

Update backend `app.py` to allow frontend domain:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://your-frontend.up.railway.app",
            "http://localhost:3000"  # Keep for local dev
        ]
    }
})
```

### Step 4: Verify Deployment

- Backend: `https://your-backend.up.railway.app/api/health`
- Frontend: `https://your-frontend.up.railway.app`

---

## 🌐 Option 2: Render Deployment

### Backend Deployment

1. **Go to Render**: https://render.com
2. **Click "New" → "Web Service"**
3. **Connect GitHub repository**
4. **Configure**:
   - **Name**: `ecommerce-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 4 app:app`
5. **Set Environment Variables**:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key
   PORT=5001
   ```
6. **Deploy** and copy the URL (e.g., `https://ecommerce-backend.onrender.com`)

### Frontend Deployment

1. **Click "New" → "Static Site"**
2. **Connect GitHub repository**
3. **Configure**:
   - **Name**: `ecommerce-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm ci && npm run build`
   - **Publish Directory**: `build`
4. **Set Environment Variables**:
   ```
   REACT_APP_API_URL=https://ecommerce-backend.onrender.com
   ```
5. **Deploy**

---

## ⚡ Option 3: Vercel (Frontend) + Railway (Backend)

### Deploy Backend to Railway
Follow **Option 1: Step 1** above.

### Deploy Frontend to Vercel

1. **Go to Vercel**: https://vercel.com
2. **Import Git Repository**
3. **Configure**:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
4. **Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-backend.up.railway.app
   ```
5. **Deploy**

**Benefits**: 
- Vercel optimizes React apps automatically
- Global CDN
- Free SSL
- Fast deployments

---

## 🐳 Option 4: Docker Compose (Self-Hosted)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key
      - DATABASE_URL=sqlite:///ecommerce.db
    volumes:
      - ./backend/instance:/app/instance

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - REACT_APP_API_URL=http://localhost:5001
    depends_on:
      - backend
```

**Deploy**:
```bash
docker-compose up -d
```

---

## 🔧 Environment Variables Reference

### Backend Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `SECRET_KEY` | Flask secret key | `your-secret-key-here` |
| `DATABASE_URL` | Database connection (optional) | `sqlite:///ecommerce.db` |
| `PORT` | Port to run on | `5001` |
| `MAIL_SERVER` | Email server (optional) | `smtp.gmail.com` |
| `MAIL_USERNAME` | Email username (optional) | `your-email@gmail.com` |
| `MAIL_PASSWORD` | Email password (optional) | `your-app-password` |

### Frontend Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_API_URL` | Backend API URL | `https://your-backend.up.railway.app` |

---

## 🔒 Security Checklist

Before deploying:

- [ ] Set strong `SECRET_KEY` (use random string)
- [ ] Enable HTTPS (most platforms do this automatically)
- [ ] Configure CORS to allow only your frontend domain
- [ ] Set `FLASK_ENV=production`
- [ ] Review environment variables (no secrets in code)
- [ ] Enable database backups (if using PostgreSQL)
- [ ] Set up monitoring/logging

---

## 📝 Step-by-Step: Railway Deployment

### Backend

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
cd backend
railway init

# 4. Set environment variables
railway variables set FLASK_ENV=production
railway variables set SECRET_KEY=$(openssl rand -base64 32)

# 5. Deploy
railway up

# 6. Get URL
railway domain
```

### Frontend

```bash
# 1. Add new service
cd ../frontend
railway init

# 2. Link to same project
railway link

# 3. Set environment variable
railway variables set REACT_APP_API_URL=https://your-backend.up.railway.app

# 4. Deploy
railway up

# 5. Get URL
railway domain
```

---

## 🧪 Testing Deployment

### Backend Health Check
```bash
curl https://your-backend.up.railway.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "products": 4,
  "timestamp": "...",
  "version": "1.0.0"
}
```

### Frontend Check
```bash
curl https://your-frontend.up.railway.app
```

Should return HTML with React app.

### Test API from Frontend
1. Open frontend URL in browser
2. Check browser console for errors
3. Try adding product to cart
4. Verify API calls work

---

## 🐛 Troubleshooting

### Backend Issues

**503 Service Unavailable**
- Check if backend is running
- Verify environment variables
- Check logs: `railway logs` or platform logs

**CORS Errors**
- Update CORS configuration in `app.py`
- Add frontend URL to allowed origins

**Database Errors**
- Verify database is initialized
- Check database file permissions
- Review logs for SQL errors

### Frontend Issues

**API Calls Failing**
- Verify `REACT_APP_API_URL` is set correctly
- Check CORS configuration on backend
- Test backend URL directly in browser

**Build Failures**
- Check Node version (should be 18+)
- Verify all dependencies install
- Review build logs

**Blank Page**
- Check browser console for errors
- Verify build completed successfully
- Check if API URL is accessible

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| **Railway** | $5/month credit | $0.000463/GB-hour |
| **Render** | Free tier available | $7/month+ |
| **Vercel** | Free tier generous | $20/month+ |
| **Heroku** | Discontinued | $7/month+ |

**Recommendation**: Start with Railway or Render free tiers.

---

## 📊 Monitoring

### Railway
- Built-in metrics dashboard
- View logs: `railway logs`
- Monitor usage in dashboard

### Render
- View logs in dashboard
- Set up alerts
- Monitor uptime

### Vercel
- Analytics dashboard
- Performance metrics
- Error tracking

---

## 🔄 Updating Deployment

### Railway
```bash
# Just push to GitHub
git push origin main

# Railway auto-deploys
```

### Render
- Auto-deploys on push to main branch
- Or manually trigger in dashboard

### Vercel
- Auto-deploys on push
- Preview deployments for PRs

---

## ✅ Post-Deployment Checklist

- [ ] Backend health check passes
- [ ] Frontend loads correctly
- [ ] Products display on frontend
- [ ] Can add items to cart
- [ ] Can complete checkout
- [ ] CORS working (no errors in console)
- [ ] HTTPS enabled
- [ ] Environment variables set correctly
- [ ] Logs accessible
- [ ] Monitoring set up

---

## 🎯 Recommended Setup

**For Quick Start**: Railway (both services)
- Easiest setup
- Auto-detects Dockerfiles
- Free tier available
- Automatic HTTPS

**For Production**: 
- Frontend: Vercel (optimized React hosting)
- Backend: Railway or Render (reliable Python hosting)

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Docker Documentation](https://docs.docker.com)

---

**Ready to deploy!** Choose your platform and follow the steps above. 🚀
