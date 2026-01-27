# GitHub Actions Workflows

This directory contains GitHub Actions workflows for CI/CD of the full-stack application.

## Workflows

### 1. `ci-cd.yml` - Main CI/CD Pipeline

Comprehensive workflow that includes:

#### Jobs:
- **backend-test**: Runs backend tests with PostgreSQL service
- **frontend-test**: Runs frontend tests with coverage
- **backend-build**: Builds backend application
- **frontend-build**: Builds frontend React application
- **lint**: Code linting for both Python and JavaScript
- **security-scan**: Security scanning with Bandit and npm audit
- **deploy-staging**: Deploys to staging environment (develop branch)
- **deploy-production**: Deploys to production environment (main branch)
- **notify**: Sends notifications on completion

#### Triggers:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

### 2. `docker-build.yml` - Docker Image Build and Push

Builds and pushes Docker images to GitHub Container Registry:

- **build-and-push-backend**: Builds backend Docker image
- **build-and-push-frontend**: Builds frontend Docker image

#### Triggers:
- Push to `main` branch
- Version tags (v*)
- Manual workflow dispatch

## Setup Instructions

### 1. Required Secrets

Add these secrets to your GitHub repository settings:

#### Backend Secrets:
- `STAGING_DATABASE_URL`: Staging database connection string
- `PRODUCTION_DATABASE_URL`: Production database connection string
- `STAGING_DEPLOY_KEY`: SSH key for staging deployment
- `PRODUCTION_DEPLOY_KEY`: SSH key for production deployment

#### Frontend Secrets:
- `REACT_APP_API_URL`: API URL for React app (optional, defaults to localhost:5000)

#### Optional:
- `SLACK_WEBHOOK_URL`: Slack webhook for notifications
- `GITHUB_TOKEN`: Automatically provided by GitHub Actions

### 2. Environment Setup

#### Backend:
- Python 3.11
- PostgreSQL 15 (for tests)
- Dependencies from `backend/requirements.txt`

#### Frontend:
- Node.js 18
- Dependencies from `frontend/package.json`

### 3. Environment Configuration

Configure environments in GitHub repository settings:
- Go to Settings → Environments
- Create `staging` and `production` environments
- Add environment-specific secrets and variables

## Workflow Features

### Testing
- ✅ Backend unit tests with pytest
- ✅ Frontend tests with Jest
- ✅ Code coverage reporting
- ✅ Coverage upload to Codecov

### Building
- ✅ Backend build verification
- ✅ Frontend production build
- ✅ Artifact storage

### Code Quality
- ✅ Python linting with flake8
- ✅ JavaScript linting with ESLint
- ✅ Security scanning with Bandit and npm audit

### Deployment
- ✅ Staging deployment (develop branch)
- ✅ Production deployment (main branch)
- ✅ Environment-specific configurations

## Customization

### Update Python/Node Versions

Edit the `env` section in `ci-cd.yml`:

```yaml
env:
  NODE_VERSION: '18'      # Change Node.js version
  PYTHON_VERSION: '3.11'  # Change Python version
```

### Add Deployment Steps

Edit the deploy jobs in `ci-cd.yml`:

```yaml
- name: Deploy backend to production
  run: |
    # Add your deployment commands here
    # Examples:
    # - Docker: docker push backend:${{ github.sha }}
    # - Kubernetes: kubectl apply -f k8s/
    # - AWS: aws deploy create-deployment ...
    # - Heroku: heroku container:push web
```

### Add Notification Channels

Edit the `notify` job:

```yaml
- name: Send Slack notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

## Monitoring

### View Workflow Runs
- Go to Actions tab in GitHub repository
- View workflow run history
- Check logs for each job

### Coverage Reports
- Coverage reports uploaded to Codecov
- View at: https://codecov.io/gh/YOUR_USERNAME/YOUR_REPO

## Troubleshooting

### Tests Failing
1. Check test logs in Actions tab
2. Run tests locally: `pytest` or `npm test`
3. Verify dependencies are installed

### Build Failing
1. Check build logs
2. Verify Node.js/Python versions
3. Check for dependency conflicts

### Deployment Failing
1. Verify secrets are set correctly
2. Check deployment permissions
3. Verify environment configurations

## Best Practices

1. **Always test locally** before pushing
2. **Use feature branches** for development
3. **Review PRs** before merging to main
4. **Monitor deployments** after merging
5. **Keep secrets secure** - never commit secrets
6. **Update dependencies** regularly
7. **Monitor workflow performance** and optimize

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Buildx](https://docs.docker.com/buildx/)
- [Codecov Documentation](https://docs.codecov.com/)
