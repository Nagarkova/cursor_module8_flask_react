# How to Find Your Railway App URL

## Quick Steps to Find Your Railway URL

### Method 1: From Service Dashboard (Easiest)

1. **Go to your Railway project**: https://railway.com/project/2c82f87e-9b64-4e88-8676-3d17d894db60
2. **Click on your service** (backend or frontend)
3. **Look at the top of the page** - you'll see:
   - **"Settings"** tab
   - **"Deployments"** tab
   - **"Metrics"** tab
   - **"Variables"** tab
4. **Click on "Settings"** tab
5. **Scroll down to "Networking"** section
6. **You'll see "Public Domain"** - this is your app URL!
   - Example: `https://your-app-name.up.railway.app`

### Method 2: From Service Overview

1. **In your Railway project dashboard**
2. **Click on your service** (the card showing your backend/frontend)
3. **Look for a section showing "Domains"** or **"Public URL"**
4. **The URL will be displayed there**

### Method 3: Generate a Public Domain

If you don't see a public domain:

1. **Click on your service**
2. **Go to "Settings"** tab
3. **Scroll to "Networking"** section
4. **Click "Generate Domain"** button
5. **Railway will create a public URL** like: `https://your-service-name.up.railway.app`

### Method 4: Using Railway CLI

```bash
# Install Railway CLI (if not already installed)
npm install -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Get the domain
railway domain
```

## For Your Specific Project

Based on your Railway project link, here's what to do:

1. **Open**: https://railway.com/project/2c82f87e-9b64-4e88-8676-3d17d894db60
2. **You'll see your services** (likely "backend" and possibly "frontend")
3. **Click on the "backend" service**
4. **Go to Settings → Networking**
5. **Copy the Public Domain URL**

## Setting Up Custom Domain (Optional)

1. **In Settings → Networking**
2. **Click "Custom Domain"**
3. **Enter your domain** (e.g., `api.yourdomain.com`)
4. **Follow DNS instructions** to point your domain to Railway

## Important Notes

- **Backend URL**: Usually looks like `https://your-backend-name.up.railway.app`
- **Frontend URL**: If deployed separately, will have a different URL
- **Port**: Railway automatically handles port mapping (your app runs on PORT env var)
- **HTTPS**: Railway provides free SSL certificates automatically

## Using the URL

Once you have your Railway backend URL:

1. **Test it**: Visit `https://your-backend.up.railway.app/api/health`
2. **Use in Netlify**: Set `REACT_APP_API_URL` environment variable to this URL
3. **Update CORS**: Make sure backend allows your frontend domain

## Example URLs

- **Backend**: `https://ecommerce-backend-production.up.railway.app`
- **Health Check**: `https://ecommerce-backend-production.up.railway.app/api/health`
- **API Endpoint**: `https://ecommerce-backend-production.up.railway.app/api/products`
