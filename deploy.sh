#!/bin/bash

# Quick Deployment Script for Backend & Frontend
# Supports Railway, Render, and Docker

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLATFORM="${1:-railway}"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Full Stack Deployment${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

case "$PLATFORM" in
    railway)
        echo -e "${GREEN}Deploying to Railway...${NC}"
        echo ""
        echo -e "${YELLOW}Backend Deployment:${NC}"
        echo "1. Go to https://railway.app"
        echo "2. New Project → Deploy from GitHub"
        echo "3. Select repository: Nagarkova/cursor_module8_flask_react"
        echo "4. Set Root Directory: backend"
        echo "5. Set Environment Variables:"
        echo "   - FLASK_ENV=production"
        echo "   - SECRET_KEY=$(openssl rand -base64 32)"
        echo ""
        echo -e "${YELLOW}Frontend Deployment:${NC}"
        echo "1. Add New Service in Railway project"
        echo "2. Set Root Directory: frontend"
        echo "3. Set Environment Variable:"
        echo "   - REACT_APP_API_URL=https://your-backend.up.railway.app"
        echo ""
        echo "See DEPLOYMENT_GUIDE.md for detailed instructions"
        ;;
    
    render)
        echo -e "${GREEN}Deploying to Render...${NC}"
        echo ""
        echo "1. Go to https://render.com"
        echo "2. Connect GitHub repository"
        echo "3. Deploy backend as Web Service"
        echo "4. Deploy frontend as Static Site"
        echo ""
        echo "See DEPLOYMENT_GUIDE.md for detailed instructions"
        ;;
    
    docker)
        echo -e "${GREEN}Building Docker images...${NC}"
        cd "$SCRIPT_DIR/backend"
        docker build -t ecommerce-backend:latest .
        echo -e "${GREEN}✓ Backend image built${NC}"
        
        cd "$SCRIPT_DIR/frontend"
        docker build -t ecommerce-frontend:latest .
        echo -e "${GREEN}✓ Frontend image built${NC}"
        
        echo ""
        echo -e "${GREEN}To run locally:${NC}"
        echo "  docker run -d -p 5001:5001 --name backend ecommerce-backend:latest"
        echo "  docker run -d -p 80:80 --name frontend ecommerce-frontend:latest"
        ;;
    
    netlify)
        echo -e "${GREEN}Deploying Frontend to Netlify...${NC}"
        echo ""
        echo -e "${YELLOW}Prerequisites:${NC}"
        echo "1. Backend must be deployed first (Railway or Render)"
        echo "2. Get your backend URL (e.g., https://your-backend.up.railway.app)"
        echo ""
        echo -e "${YELLOW}Steps:${NC}"
        echo "1. Go to https://app.netlify.com"
        echo "2. Add new site → Import from Git"
        echo "3. Select repository: Nagarkova/cursor_module8_flask_react"
        echo "4. Configure:"
        echo "   - Base directory: frontend"
        echo "   - Build command: npm ci && npm run build"
        echo "   - Publish directory: frontend/build"
        echo "5. Set environment variable:"
        echo "   - REACT_APP_API_URL=https://your-backend.up.railway.app"
        echo "6. Deploy!"
        echo ""
        echo -e "${YELLOW}Or use CLI:${NC}"
        echo "  cd frontend"
        echo "  npm install -g netlify-cli"
        echo "  netlify login"
        echo "  netlify init"
        echo "  netlify env:set REACT_APP_API_URL https://your-backend.up.railway.app"
        echo "  netlify deploy --prod"
        echo ""
        echo "See DEPLOYMENT_GUIDE.md for detailed instructions"
        ;;
    
    *)
        echo -e "${YELLOW}Usage: $0 [railway|render|docker|netlify]${NC}"
        echo ""
        echo "Platforms:"
        echo "  railway  - Deploy to Railway (recommended)"
        echo "  render   - Deploy to Render"
        echo "  docker   - Build Docker images locally"
        echo "  netlify  - Deploy frontend to Netlify"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Deployment Instructions Complete${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
