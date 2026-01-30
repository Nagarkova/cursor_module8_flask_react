# Netlify Deployment Guide

Quick guide for deploying the frontend to Netlify.

## 🚀 Quick Start

### Prerequisites
1. Backend deployed (Railway or Render)
2. Backend URL ready (e.g., `https://your-backend.up.railway.app`)
3. Netlify account: https://netlify.com

## Step-by-Step Deployment

### 1. Deploy Backend First

**Important**: Deploy your backend to Railway or Render first, then get the backend URL.

**Railway**:
- Deploy backend service
- Get URL: `https://your-backend.up.railway.app`

**Render**:
- Deploy backend web service
- Get URL: `https://your-backend.onrender.com`

### 2. Deploy Frontend to Netlify

#### Option A: Via Netlify Dashboard (Easiest)

1. **Go to Netlify**: https://app.netlify.com
2. **Sign up/Login** (can use GitHub account)
3. **Click "Add new site"** → **"Import an existing project"**
4. **Connect to GitHub**:
   - Authorize Netlify to access your repositories
   - Select: `Nagarkova/cursor_module8_flask_react`
5. **Configure Build Settings**:
   - **Base directory**: `frontend`
   - **Build command**: `npm ci && npm run build`
   - **Publish directory**: `frontend/build`
6. **Set Environment Variable**:
   - Click **"Show advanced"** or **"Environment variables"**
   - Click **"Add variable"**
   - **Key**: `REACT_APP_API_URL`
   - **Value**: Your backend URL (e.g., `https://your-backend.up.railway.app`)
   - Click **"Add"**
7. **Click "Deploy site"**
8. **Wait for build** (usually 2-3 minutes)
9. **Get your site URL**: `https://random-name-12345.netlify.app`

#### Option B: Via Netlify CLI

```bash
# 1. Install Netlify CLI globally
npm install -g netlify-cli

# 2. Login to Netlify
netlify login

# 3. Navigate to frontend directory
cd frontend

# 4. Initialize Netlify site
netlify init

# Follow prompts:
# - Create & configure a new site
# - Team: Select your team
# - Site name: (optional, or use default)
# - Build command: npm ci && npm run build
# - Directory to deploy: build
# - Netlify functions folder: (leave empty)

# 5. Set environment variable
netlify env:set REACT_APP_API_URL https://your-backend.up.railway.app

# 6. Deploy to production
netlify deploy --prod

# Or deploy to preview (for testing)
netlify deploy
```

### 3. Update Backend CORS

After Netlify deployment, update your backend to allow the Netlify domain:

**If using Railway**:
```bash
railway variables set FRONTEND_URL=https://your-app.netlify.app
```

**If using Render**:
1. Go to your backend service dashboard
2. Go to **Environment** tab
3. Add variable:
   - **Key**: `FRONTEND_URL`
   - **Value**: `https://your-app.netlify.app`
4. **Save** and **Redeploy**

### 4. Verify Deployment

1. **Visit your Netlify site**: `https://your-app.netlify.app`
2. **Open browser console** (F12)
3. **Check for errors**:
   - Should see products loading
   - No CORS errors
   - API calls should work
4. **Test functionality**:
   - Add product to cart
   - View cart
   - Complete checkout

## 🔧 Configuration Files

The project includes these Netlify configuration files:

### `frontend/netlify.toml`
- Build settings
- Redirect rules for React Router
- Security headers
- Cache headers for static assets

### `frontend/public/_redirects`
- Ensures React Router works correctly
- All routes redirect to `index.html`

These files are already configured and will be used automatically.

## 🌐 Custom Domain (Optional)

1. Go to **Site settings** → **Domain management**
2. Click **Add custom domain**
3. Enter your domain (e.g., `myapp.com`)
4. Follow DNS configuration:
   - Add CNAME record: `www` → `your-app.netlify.app`
   - Or A record: `@` → Netlify IPs
5. Netlify will automatically provision SSL certificate

## 🔄 Automatic Deployments

Netlify automatically deploys when you push to GitHub:

- **Production**: Deploys from `main` branch
- **Preview**: Creates preview URLs for pull requests
- **Branch**: Deploys other branches as previews

To disable auto-deploy:
- Go to **Site settings** → **Build & deploy**
- Under **Continuous Deployment**, click **Stop auto publishing**

## 🐛 Troubleshooting

### Build Fails

**Error**: `npm ci` fails
- **Solution**: Check Node version in `netlify.toml` (should be 18)
- Or set in Netlify dashboard: **Site settings** → **Build & deploy** → **Environment** → **Node version**: `18`

**Error**: Missing dependencies
- **Solution**: Ensure `package.json` has all dependencies
- Check `package-lock.json` is committed

**Error**: Build command fails
- **Solution**: Test locally: `cd frontend && npm ci && npm run build`
- Check build logs in Netlify dashboard

### API Calls Fail

**Error**: CORS errors in console
- **Solution**: Update backend `FRONTEND_URL` environment variable
- Redeploy backend after updating CORS

**Error**: 404 on API calls
- **Solution**: Verify `REACT_APP_API_URL` is set correctly
- Check backend URL is accessible: `curl https://your-backend.up.railway.app/api/health`

**Error**: Environment variable not working
- **Solution**: 
  - Variables must start with `REACT_APP_` prefix
  - Redeploy after changing environment variables
  - Check variable name matches exactly (case-sensitive)

### 404 Errors on Routes

**Error**: Page shows 404 when navigating
- **Solution**: Verify `_redirects` file exists in `frontend/public/`
- Check `netlify.toml` has redirect rules
- Redeploy site

### Site Shows Blank Page

**Error**: White screen, no content
- **Solution**: 
  - Check browser console for errors
  - Verify build completed successfully
  - Check if `index.html` exists in build folder
  - Test backend API is accessible

## 📊 Netlify Features

✅ **Automatic Deployments**: Deploys on every push  
✅ **Preview Deployments**: PR previews  
✅ **CDN**: Global content delivery  
✅ **HTTPS**: Free SSL certificates  
✅ **Form Handling**: Built-in form submissions  
✅ **Analytics**: Site analytics (paid)  
✅ **Split Testing**: A/B testing (paid)  
✅ **Serverless Functions**: Add API endpoints  

## 🔒 Security Headers

Netlify automatically adds security headers (configured in `netlify.toml`):
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: strict-origin-when-cross-origin`

## 💰 Pricing

**Free Tier**:
- 100 GB bandwidth/month
- 300 build minutes/month
- Unlimited sites
- HTTPS included
- Form submissions (100/month)

**Pro Tier** ($19/month):
- 1 TB bandwidth/month
- 1000 build minutes/month
- Advanced analytics
- Split testing
- More form submissions

## 📝 Environment Variables

Set in Netlify dashboard:
- **Site settings** → **Build & deploy** → **Environment**

Required:
- `REACT_APP_API_URL` - Your backend URL

Optional:
- `REACT_APP_ANALYTICS_ID` - Analytics tracking ID
- Any other `REACT_APP_*` variables

## ✅ Post-Deployment Checklist

- [ ] Frontend builds successfully
- [ ] Site loads without errors
- [ ] Products display correctly
- [ ] Can add items to cart
- [ ] Can complete checkout
- [ ] No CORS errors in console
- [ ] Backend CORS updated with Netlify URL
- [ ] HTTPS enabled (automatic)
- [ ] Custom domain configured (if applicable)

## 🎯 Next Steps

1. **Set up monitoring**: Use Netlify Analytics or external service
2. **Configure custom domain**: Add your own domain
3. **Set up CI/CD**: Already configured via GitHub integration
4. **Add form handling**: If you need contact forms
5. **Enable analytics**: Track site performance

---

**Your app is now live on Netlify!** 🎉

Visit your site and test all functionality. If you encounter any issues, check the troubleshooting section above.
