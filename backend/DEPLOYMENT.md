# Backend Deployment Guide

This guide covers deploying the Flask backend to various platforms.

## Quick Start

```bash
# Build and test Docker image locally
./deploy.sh docker

# Deploy to Docker Hub
DOCKER_USERNAME=yourusername DOCKER_PASSWORD=yourpassword ./deploy.sh dockerhub

# Deploy to Railway
./deploy.sh railway

# Deploy to Render
./deploy.sh render

# Deploy to Heroku
./deploy.sh heroku
```

## Prerequisites

1. **Docker** installed (for Docker deployments)
2. **Environment variables** configured
3. **Database** set up (PostgreSQL recommended for production)

## Environment Variables

Create a `.env` file or set these in your deployment platform:

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Database (use PostgreSQL in production)
DATABASE_URL=postgresql://user:password@host:port/database

# Email Configuration (optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## Deployment Options

### 1. Docker (Local/Server)

**Build and run locally:**
```bash
./deploy.sh docker

# Or manually:
docker build -t ecommerce-backend:latest .
docker run -d -p 5001:5001 \
  -e FLASK_ENV=production \
  -e DATABASE_URL=postgresql://... \
  --name backend \
  ecommerce-backend:latest
```

**Verify deployment:**
```bash
curl http://localhost:5001/api/health
```

### 2. Docker Hub

**Push to Docker Hub:**
```bash
export DOCKER_USERNAME=yourusername
export DOCKER_PASSWORD=yourpassword
./deploy.sh dockerhub
```

**Pull and run:**
```bash
docker pull yourusername/ecommerce-backend:latest
docker run -d -p 5001:5001 \
  -e DATABASE_URL=postgresql://... \
  yourusername/ecommerce-backend:latest
```

### 3. Railway

**Install Railway CLI:**
```bash
npm install -g @railway/cli
```

**Deploy:**
```bash
railway login
railway init
railway up
```

**Set environment variables:**
```bash
railway variables set DATABASE_URL=postgresql://...
railway variables set SECRET_KEY=your-secret-key
```

**Get deployment URL:**
```bash
railway domain
```

### 4. Render

**Via Dashboard:**
1. Go to https://render.com
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `docker build -t backend .`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 4 app:app`
   - **Environment**: `Python 3`
5. Add environment variables
6. Deploy

**Via CLI:**
```bash
render deploy
```

### 5. Heroku

**Install Heroku CLI:**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Or download from: https://devcenter.heroku.com/articles/heroku-cli
```

**Deploy:**
```bash
heroku login
heroku create ecommerce-backend
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY=$(openssl rand -base64 32)
git push heroku main
```

**View logs:**
```bash
heroku logs --tail
```

**Open app:**
```bash
heroku open
```

### 6. AWS (EC2/ECS/Elastic Beanstalk)

**EC2:**
```bash
# SSH into EC2 instance
ssh ubuntu@your-ec2-ip

# Install Docker
sudo apt update
sudo apt install docker.io -y

# Clone repository
git clone your-repo-url
cd backend

# Build and run
docker build -t backend .
docker run -d -p 80:5001 \
  -e DATABASE_URL=postgresql://... \
  backend
```

**ECS:**
1. Push image to ECR
2. Create ECS task definition
3. Create ECS service
4. Configure load balancer

**Elastic Beanstalk:**
```bash
eb init -p python-3.11
eb create ecommerce-backend-env
eb deploy
```

### 7. Google Cloud Platform (Cloud Run)

**Build and deploy:**
```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Build image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/backend

# Deploy to Cloud Run
gcloud run deploy backend \
  --image gcr.io/YOUR_PROJECT_ID/backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=postgresql://...
```

### 8. Azure (App Service)

**Deploy via Azure CLI:**
```bash
az login
az group create --name ecommerce-rg --location eastus
az appservice plan create --name backend-plan --resource-group ecommerce-rg --sku B1
az webapp create --resource-group ecommerce-rg --plan backend-plan --name ecommerce-backend --runtime "PYTHON|3.11"
az webapp config appsettings set --resource-group ecommerce-rg --name ecommerce-backend --settings DATABASE_URL=postgresql://...
az webapp deployment source config-local-git --name ecommerce-backend --resource-group ecommerce-rg
git remote add azure https://ecommerce-backend.scm.azurewebsites.net/ecommerce-backend.git
git push azure main
```

## Database Setup

### PostgreSQL (Recommended for Production)

**Local PostgreSQL:**
```bash
# Install PostgreSQL
brew install postgresql  # macOS
sudo apt install postgresql  # Linux

# Create database
createdb ecommerce_db

# Update DATABASE_URL
export DATABASE_URL=postgresql://localhost/ecommerce_db
```

**Cloud PostgreSQL Options:**
- **Railway**: Automatically provisions PostgreSQL
- **Render**: Add PostgreSQL addon
- **Heroku**: `heroku addons:create heroku-postgresql:hobby-dev`
- **AWS RDS**: Create PostgreSQL instance
- **Google Cloud SQL**: Create PostgreSQL instance
- **Azure Database**: Create PostgreSQL server

### SQLite (Development Only)

For development, SQLite is fine. For production, use PostgreSQL.

## Health Checks

After deployment, verify:

```bash
# Health check endpoint
curl https://your-backend-url/api/health

# Expected response:
{
  "status": "healthy",
  "database": "connected",
  "products": 4,
  "timestamp": "...",
  "version": "1.0.0"
}
```

## Monitoring

### Application Logs

**Docker:**
```bash
docker logs backend
docker logs -f backend  # Follow logs
```

**Railway:**
```bash
railway logs
```

**Heroku:**
```bash
heroku logs --tail
```

**Render:**
- View logs in dashboard

### Performance Monitoring

Consider adding:
- **Sentry** for error tracking
- **New Relic** or **Datadog** for APM
- **Prometheus** + **Grafana** for metrics

## Troubleshooting

### Common Issues

**Port binding error:**
```bash
# Check if port is in use
lsof -i :5001

# Kill process
kill -9 <PID>
```

**Database connection error:**
- Verify DATABASE_URL is set correctly
- Check database is accessible
- Verify credentials

**Memory issues:**
- Reduce gunicorn workers: `--workers 2`
- Increase container memory limit

**Timeout errors:**
- Increase timeout: `--timeout 300`
- Check database query performance

## Security Checklist

- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS (most platforms do this automatically)
- [ ] Set CORS origins appropriately
- [ ] Use environment variables for secrets
- [ ] Enable database SSL
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity

## Scaling

### Horizontal Scaling

**Docker Swarm:**
```bash
docker swarm init
docker stack deploy -c docker-compose.yml backend
```

**Kubernetes:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: yourusername/ecommerce-backend:latest
        ports:
        - containerPort: 5001
```

### Vertical Scaling

Increase container resources:
- More CPU
- More memory
- More gunicorn workers

## Cost Estimates

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| Railway | $5/month credit | $0.000463/GB-hour |
| Render | Free tier available | $7/month+ |
| Heroku | Free tier discontinued | $7/month+ |
| AWS EC2 | t2.micro free | ~$10/month+ |
| Google Cloud Run | 2M requests/month | $0.40/million requests |

## Support

For deployment issues:
1. Check logs: `docker logs backend` or platform logs
2. Verify environment variables
3. Test health endpoint
4. Check database connectivity
5. Review platform documentation

---

**Ready to deploy!** Choose your platform and run `./deploy.sh [platform]`
