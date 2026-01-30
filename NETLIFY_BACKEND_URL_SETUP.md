# How to Add Backend URL to Netlify

## Your Backend URL
```
https://cursormodule8flaskreact-production.up.railway.app
```

## Step-by-Step Instructions

### Method 1: Via Netlify Dashboard (Recommended)

1. **Go to Netlify Dashboard**
   - Visit: https://app.netlify.com
   - Sign in to your account

2. **Select Your Site**
   - Click on your site: `shop-ui-react-flask` (or your site name)

3. **Go to Site Settings**
   - Click **"Site settings"** (gear icon) in the top menu
   - Or go to: **Site configuration** → **Environment variables**

4. **Add Environment Variable**
   - Click **"Add variable"** or **"Add environment variable"**
   - **Key**: `REACT_APP_API_URL`
   - **Value**: `https://cursormodule8flaskreact-production.up.railway.app`
   - **Scopes**: Select:
     - ✅ **Production**
     - ✅ **Deploy previews** (optional, for PR previews)
     - ✅ **Branch deploys** (optional)

5. **Save**
   - Click **"Save"** or **"Add variable"**

6. **Redeploy**
   - Go to **"Deploys"** tab
   - Click **"Trigger deploy"** → **"Deploy site"**
   - Or push a new commit to trigger automatic deployment

### Method 2: Via Netlify CLI

```bash
# Install Netlify CLI (if not already installed)
npm install -g netlify-cli

# Login to Netlify
netlify login

# Link to your site (if not already linked)
cd frontend
netlify link

# Set the environment variable
netlify env:set REACT_APP_API_URL https://cursormode8flaskreact-production.up.railway.app

# Deploy
netlify deploy --prod
```

## Verify It's Set Correctly

1. **Check Environment Variables**
   - Go to **Site settings** → **Environment variables**
   - You should see: `REACT_APP_API_URL = https://cursormodule8flaskreact-production.up.railway.app`

2. **Check Build Logs**
   - Go to **Deploys** tab
   - Click on the latest deploy
   - Look for environment variables in the build logs
   - Should show: `REACT_APP_API_URL`

3. **Test in Browser**
   - Visit your Netlify site
   - Open browser console (F12)
   - Check network requests - API calls should go to your Railway backend
   - No CORS errors should appear

## Update Backend CORS

After setting the Netlify URL, update your Railway backend to allow requests from Netlify:

### In Railway Dashboard:

1. Go to your Railway project
2. Click on your backend service
3. Go to **Variables** tab
4. Add/Update:
   - **Key**: `FRONTEND_URL`
   - **Value**: `https://your-netlify-site.netlify.app` (your actual Netlify URL)
5. **Save** and **Redeploy** backend

### Or via Railway CLI:

```bash
railway variables set FRONTEND_URL=https://your-netlify-site.netlify.app
```

## Quick Checklist

- [ ] Added `REACT_APP_API_URL` in Netlify dashboard
- [ ] Value set to: `https://cursormodule8flaskreact-production.up.railway.app`
- [ ] Scopes include Production
- [ ] Triggered new deployment
- [ ] Updated backend CORS with Netlify URL
- [ ] Tested API calls in browser console

## Troubleshooting

### Environment Variable Not Working

**Issue**: API calls still go to localhost
- **Solution**: 
  - Verify variable name is exactly `REACT_APP_API_URL` (case-sensitive)
  - Redeploy after adding variable
  - Check build logs to confirm variable is loaded

### CORS Errors

**Issue**: CORS errors in browser console
- **Solution**:
  - Update backend `FRONTEND_URL` environment variable
  - Redeploy backend
  - Verify CORS configuration in `backend/app.py`

### Build Fails

**Issue**: Build fails after adding variable
- **Solution**:
  - Check variable value is correct URL (with https://)
  - No trailing slash
  - Verify Railway backend is accessible: `curl https://cursormodule8flaskreact-production.up.railway.app/api/health`

## Example Configuration

**Netlify Environment Variables:**
```
REACT_APP_API_URL = https://cursormodule8flaskreact-production.up.railway.app
```

**Railway Environment Variables:**
```
FRONTEND_URL = https://your-netlify-site.netlify.app
FLASK_ENV = production
SECRET_KEY = your-secret-key
```

## Testing

After setup, test your API connection:

1. **Health Check**:
   ```bash
   curl https://cursormodule8flaskreact-production.up.railway.app/api/health
   ```

2. **From Browser**:
   - Open your Netlify site
   - Open DevTools → Network tab
   - Try adding a product to cart
   - Verify API calls go to Railway backend

3. **Check Console**:
   - No CORS errors
   - API calls successful
   - Products load correctly
