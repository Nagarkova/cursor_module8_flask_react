# Fix Netlify Frontend Deployment

## Step-by-Step Fix for Your Netlify Site

Your Netlify site: `shop-ui-react-flask`

### Step 1: Check Repository Connection

1. Go to: https://app.netlify.com/projects/shop-ui-react-flask/configuration/deploys
2. Click on **"Build & deploy"** in the left sidebar
3. Under **"Continuous Deployment"**, check which repository is connected
4. **It should be**: `Nagarkova/cursor_module8_flask_react`
5. **If it's wrong** (like `cursor_module_6_posts_flask`), continue to Step 2

### Step 2: Fix Repository Connection

#### Option A: Change Repository (Keep Site)

1. In **Build & deploy** settings
2. Under **"Continuous Deployment"**, click **"Change site source"** or **"Edit settings"**
3. Click **"Disconnect repository"** or **"Change site source"**
4. Click **"Add new provider"** → Select **GitHub**
5. Search for: `cursor_module8_flask_react`
6. Select: `Nagarkova/cursor_module8_flask_react`
7. Select branch: `main` (or `master` if that's your default branch)
8. Click **"Save"**

#### Option B: Configure Build Settings Manually

If the repository is correct but build is failing:

1. Go to **Build & deploy** → **Build settings**
2. Configure:
   - **Base directory**: `frontend`
   - **Build command**: `npm ci && npm run build`
   - **Publish directory**: `frontend/build`
3. Click **"Save"**

**OR** leave these empty if you want to use the `netlify.toml` file (recommended)

### Step 3: Set Environment Variables

1. Go to **Build & deploy** → **Environment**
2. Click **"Add variable"**
3. Add:
   - **Key**: `REACT_APP_API_URL`
   - **Value**: Your backend URL (e.g., `https://your-backend.up.railway.app`)
   - **Scopes**: Select **"Production"** and **"Deploy previews"**
4. Click **"Save"**

### Step 4: Trigger New Deployment

1. Go to **Deploys** tab
2. Click **"Trigger deploy"** → **"Deploy site"**
3. Or push a commit to your `main` branch (if auto-deploy is enabled)

### Step 5: Check Build Logs

1. Click on the latest deploy
2. Check the build logs for errors
3. Common issues:
   - **Wrong repository**: Will show `cursor_module_6_posts_flask` in logs
   - **Base directory error**: Will show "Base directory does not exist"
   - **Build errors**: Check npm/node version issues

## Expected Build Log Output

When working correctly, you should see:
```
5:XX:XX PM: Cloning repository...
5:XX:XX PM: git clone https://github.com/Nagarkova/cursor_module8_flask_react
5:XX:XX PM: Preparing Git Reference refs/heads/main
5:XX:XX PM: Installing dependencies
5:XX:XX PM: npm ci
5:XX:XX PM: Building site
5:XX:XX PM: npm run build
5:XX:XX PM: Post processing
5:XX:XX PM: Site is live ✨
```

## Quick Configuration Checklist

In Netlify Dashboard → Build & deploy:

- [ ] **Repository**: `Nagarkova/cursor_module8_flask_react`
- [ ] **Branch**: `main` (or `master`)
- [ ] **Base directory**: `frontend` (or leave empty for netlify.toml)
- [ ] **Build command**: `npm ci && npm run build` (or leave empty)
- [ ] **Publish directory**: `frontend/build` (or leave empty)
- [ ] **Node version**: `18` (set in Environment or netlify.toml)
- [ ] **Environment variable**: `REACT_APP_API_URL` = your backend URL

## Troubleshooting

### Error: "Base directory does not exist"
- **Fix**: Make sure repository is `cursor_module8_flask_react`
- **Fix**: Set Base directory to `frontend` in build settings
- **Fix**: Ensure `netlify.toml` exists at repository root

### Error: Wrong repository cloned
- **Fix**: Disconnect and reconnect to correct repository
- **Fix**: Verify repository name in Continuous Deployment settings

### Error: Build fails with npm errors
- **Fix**: Check Node version is set to 18
- **Fix**: Verify `package.json` exists in `frontend` directory
- **Fix**: Check build logs for specific npm errors

### Error: Environment variable not working
- **Fix**: Variable must start with `REACT_APP_`
- **Fix**: Redeploy after adding environment variable
- **Fix**: Check variable is set for Production scope

## Verify Deployment

After successful deployment:

1. Visit your Netlify site URL
2. Open browser console (F12)
3. Check for errors
4. Test functionality:
   - Products should load
   - Can add to cart
   - Can checkout

## Need More Help?

Check the build logs in Netlify dashboard for specific error messages and share them for further assistance.
