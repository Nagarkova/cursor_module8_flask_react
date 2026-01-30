# Fix Netlify Wrong Repository Issue

## Problem
Netlify is trying to clone `cursor_module_6_posts_flask` instead of `cursor_module8_flask_react`.

## Solution: Change Repository in Netlify

### Option 1: Change Repository (Keep Existing Site)

1. **Go to Netlify Dashboard**: https://app.netlify.com
2. **Click on your site**
3. **Go to Site settings** (gear icon or "Site settings" link)
4. **Click "Build & deploy"** in the left sidebar
5. **Under "Continuous Deployment"**, click **"Link to a different branch"** or **"Edit settings"**
6. **Click "Change site source"** or **"Disconnect repository"**
7. **Click "Add new provider"** or **"Connect to Git provider"**
8. **Select GitHub** and authorize if needed
9. **Search for**: `cursor_module8_flask_react`
10. **Select**: `Nagarkova/cursor_module8_flask_react`
11. **Select branch**: `main` (or `master`)
12. **Configure build settings**:
    - **Base directory**: `frontend`
    - **Build command**: `npm ci && npm run build`
    - **Publish directory**: `frontend/build`
    - OR leave empty (the root `netlify.toml` will handle it)
13. **Click "Save"** or **"Deploy site"**

### Option 2: Delete and Recreate (Recommended - Cleaner)

1. **Go to Netlify Dashboard**: https://app.netlify.com
2. **Click on your site**
3. **Go to Site settings** → **General**
4. **Scroll down** and click **"Delete this site"**
5. **Confirm deletion**
6. **Click "Add new site"** → **"Import an existing project"**
7. **Select GitHub**
8. **Search for**: `cursor_module8_flask_react`
9. **Select**: `Nagarkova/cursor_module8_flask_react`
10. **Configure**:
    - **Branch**: `main`
    - **Base directory**: `frontend` (or leave empty - netlify.toml handles it)
    - **Build command**: Leave empty (netlify.toml handles it)
    - **Publish directory**: Leave empty (netlify.toml handles it)
11. **Click "Show advanced"** → **Add environment variable**:
    - **Key**: `REACT_APP_API_URL`
    - **Value**: Your backend URL (e.g., `https://your-backend.up.railway.app`)
12. **Click "Deploy site"**

## Verify Correct Repository

After connecting, verify:
1. Go to **Site settings** → **Build & deploy** → **Continuous Deployment**
2. You should see: `Nagarkova/cursor_module8_flask_react`
3. NOT: `cursor_module_6_posts_flask`

## After Fixing

Once connected to the correct repository:
- Netlify will automatically detect the `netlify.toml` at the root
- The build should work correctly
- You'll see the correct repository in the build logs

## Quick Checklist

- [ ] Disconnected from wrong repository (`cursor_module_6_posts_flask`)
- [ ] Connected to correct repository (`cursor_module8_flask_react`)
- [ ] Branch set to `main` (or `master`)
- [ ] Environment variable `REACT_APP_API_URL` set
- [ ] Build settings configured (or using netlify.toml)
- [ ] Triggered new deployment
