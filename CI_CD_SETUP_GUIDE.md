# CI/CD Setup Guide

This guide will help you configure all necessary secrets and settings for the optimized CI/CD pipeline.

## GitHub Repository Secrets Setup

### Navigate to Secrets
1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

### Required Secrets

#### 1. Security Scanning

**SNYK_TOKEN** (Required for Snyk security scanning)
```
Value: your_snyk_api_token
```

**How to get:**
1. Sign up at https://snyk.io (free for open source)
2. Go to Account Settings → General
3. Copy your Auth Token
4. Paste into GitHub secret

#### 2. Slack Notifications

**SLACK_WEBHOOK_URL** (Required for notifications)
```
Value: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

**How to get:**
1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name it "CI/CD Bot" and select your workspace
4. Go to "Incoming Webhooks" → Toggle "On"
5. Click "Add New Webhook to Workspace"
6. Select channel (e.g., #deployments)
7. Copy the Webhook URL
8. Paste into GitHub secret

#### 3. Deployment Keys (Optional - if deploying)

**STAGING_DEPLOY_KEY**
```
Value: your_staging_ssh_key_or_token
```

**PRODUCTION_DEPLOY_KEY**
```
Value: your_production_ssh_key_or_token
```

**STAGING_DATABASE_URL**
```
Value: postgresql://user:password@host:port/database
```

**PRODUCTION_DATABASE_URL**
```
Value: postgresql://user:password@host:port/database
```

**REACT_APP_API_URL** (Optional - defaults to http://localhost:5000)
```
Value: https://api.example.com
```

### Optional Secrets

**CODECOV_TOKEN** (If using Codecov)
```
Value: your_codecov_token
```

## Verify Setup

### 1. Test Health Check Endpoint

```bash
# Start your backend locally
cd backend
source venv/bin/activate
python app.py

# In another terminal, test the health check
curl http://localhost:5001/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-30T12:00:00",
  "database": "connected",
  "products": 4,
  "version": "1.0.0"
}
```

### 2. Test Slack Notifications

```bash
# Test webhook manually
curl -X POST \
  -H 'Content-type: application/json' \
  --data '{"text":"Test message from CI/CD setup"}' \
  YOUR_SLACK_WEBHOOK_URL
```

### 3. Activate Optimized Workflow

**Option A: Replace existing workflow**
```bash
cd .github/workflows
mv ci-cd.yml ci-cd-old.yml.backup
mv ci-cd-optimized.yml ci-cd.yml
git add .
git commit -m "Enable optimized CI/CD pipeline"
git push
```

**Option B: Run both temporarily**
```bash
# Keep both workflows active to compare
git add .github/workflows/ci-cd-optimized.yml
git commit -m "Add optimized CI/CD pipeline"
git push
# Delete old one after verification
```

## Verification Checklist

After pushing the changes:

- [ ] Go to Actions tab in GitHub
- [ ] Verify new workflow appears
- [ ] Wait for workflow to complete
- [ ] Check that Slack notification was received
- [ ] Verify all jobs completed successfully
- [ ] Compare runtime with previous workflow
- [ ] Check cache hit rates in logs

## Snyk Integration Details

### Free Tier Limits
- Unlimited tests for open source projects
- 200 tests/month for private projects
- Unlimited CLI scans

### Configuration File (Optional)

Create `.snyk` file in repository root:

```yaml
# .snyk
version: v1.29.0
exclude:
  # Exclude test files from scanning
  code:
    - test/**
    - __tests__/**
ignore:
  # Ignore specific vulnerabilities (use with caution)
  'SNYK-JS-AXIOS-1234567':
    - '*':
        reason: 'Fix not available yet, risk accepted'
        expires: '2026-03-01'
```

## Slack Notification Customization

### Custom Channels

Send different notifications to different channels:

```yaml
# Success notifications to #deployments
SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_DEPLOYMENTS }}

# Failure notifications to #alerts
SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_ALERTS }}
```

### Mention Users on Failure

```json
{
  "text": "<!here> ❌ Pipeline Failed",
  "blocks": [...]
}
```

Use:
- `<!here>` - mention active users
- `<!channel>` - mention all
- `<@USER_ID>` - mention specific user

## Cache Management

### View Cache Usage

```bash
# Using GitHub CLI
gh cache list

# View cache size
gh api /repos/OWNER/REPO/actions/caches
```

### Clear All Caches

```bash
# Clear all caches (use with caution)
gh cache delete --all
```

### Manual Cache Invalidation

Update `CACHE_VERSION` in workflow:

```yaml
env:
  CACHE_VERSION: 'v2'  # Increment this
```

## Troubleshooting

### Issue: Snyk scan failing

**Error**: `Missing SNYK_TOKEN`
**Solution**: Ensure secret is added and spelled correctly

**Error**: `Authentication failed`
**Solution**: Regenerate token on Snyk.io

### Issue: Slack notifications not received

**Check:**
1. Webhook URL is correct
2. App has permission to post
3. Channel still exists
4. Webhook not revoked

**Test webhook:**
```bash
curl -X POST YOUR_WEBHOOK_URL \
  -H 'Content-type: application/json' \
  -d '{"text":"Test"}'
```

### Issue: Health check failing

**Check:**
1. Endpoint returns 200 status
2. Database is accessible
3. URL is correct in workflow
4. No authentication required

### Issue: Docker build slow

**Solutions:**
1. Check .dockerignore is complete
2. Verify BuildKit cache is working
3. Optimize Dockerfile layer order
4. Use multi-stage builds

## Monitoring & Alerts

### GitHub Actions Insights

View performance metrics:
1. Repository → Insights → Actions
2. Check workflow run duration
3. Monitor success/failure rates
4. Review billable minutes

### Recommended Monitoring

1. **Set up GitHub Status Checks**
   - Settings → Branches → Branch protection rules
   - Require status checks before merging

2. **Enable Notifications**
   - Personal settings → Notifications
   - Watch repository for Actions workflow runs

3. **Weekly Reviews**
   - Check security alerts
   - Review failed runs
   - Optimize slow jobs

## Advanced Configuration

### Matrix Testing (Future)

Test multiple Python/Node versions:

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12']
    node-version: ['18', '20']
```

### Environment Variables

Global environment variables:

```yaml
env:
  PYTHON_VERSION: '3.11'
  NODE_VERSION: '18'
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### Conditional Steps

Run steps based on conditions:

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main' && success()
  run: ./deploy.sh
```

## Support

### Common Commands

```bash
# Trigger workflow manually
gh workflow run ci-cd.yml

# View workflow runs
gh run list

# View specific run logs
gh run view RUN_ID

# Cancel running workflow
gh run cancel RUN_ID

# Re-run failed jobs
gh run rerun RUN_ID
```

### Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Snyk Documentation](https://docs.snyk.io)
- [Slack API Documentation](https://api.slack.com)
- [Docker BuildKit](https://docs.docker.com/build/buildkit/)

## Rollback Plan

If issues occur:

```bash
# Revert to old workflow
cd .github/workflows
mv ci-cd.yml ci-cd-optimized.yml.backup
mv ci-cd-old.yml.backup ci-cd.yml
git add .
git commit -m "Revert to previous CI/CD workflow"
git push
```

## Next Steps

After successful setup:

1. ✅ Monitor first few workflow runs
2. ✅ Verify Slack notifications work
3. ✅ Check cache hit rates
4. ✅ Measure time savings
5. ✅ Review security scan results
6. ✅ Delete old workflow after 1 week
7. ✅ Document any custom changes
8. ✅ Train team on new features

## Questions?

Check the CI_CD_OPTIMIZATION_REPORT.md for detailed information about:
- Performance improvements
- Cost savings
- Technical details
- Best practices
