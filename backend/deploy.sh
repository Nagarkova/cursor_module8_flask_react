#!/bin/bash

# Backend Deployment Script
# Supports multiple deployment targets

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Default values
DEPLOYMENT_TARGET="${1:-docker}"
IMAGE_NAME="${IMAGE_NAME:-ecommerce-backend}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
REGISTRY="${REGISTRY:-}"

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Backend Deployment${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Function to build Docker image
build_image() {
    echo -e "${BLUE}Building Docker image...${NC}"
    docker build -t "${IMAGE_NAME}:${IMAGE_TAG}" .
    echo -e "${GREEN}✓ Image built successfully${NC}"
}

# Function to test Docker image
test_image() {
    echo -e "${BLUE}Testing Docker image...${NC}"
    docker run --rm -d \
        --name test-backend \
        -p 5001:5001 \
        -e FLASK_ENV=production \
        "${IMAGE_NAME}:${IMAGE_TAG}" || true
    
    sleep 5
    
    if curl -f -s http://localhost:5001/api/health > /dev/null; then
        echo -e "${GREEN}✓ Image test passed${NC}"
        docker stop test-backend 2>/dev/null || true
        return 0
    else
        echo -e "${RED}✗ Image test failed${NC}"
        docker stop test-backend 2>/dev/null || true
        return 1
    fi
}

# Function to push to Docker Hub
push_to_dockerhub() {
    if [ -z "$DOCKER_USERNAME" ] || [ -z "$DOCKER_PASSWORD" ]; then
        echo -e "${YELLOW}⚠ Docker Hub credentials not set${NC}"
        echo -e "  Set DOCKER_USERNAME and DOCKER_PASSWORD environment variables"
        return 1
    fi
    
    echo -e "${BLUE}Logging into Docker Hub...${NC}"
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
    
    FULL_IMAGE_NAME="${DOCKER_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG}"
    docker tag "${IMAGE_NAME}:${IMAGE_TAG}" "$FULL_IMAGE_NAME"
    
    echo -e "${BLUE}Pushing to Docker Hub...${NC}"
    docker push "$FULL_IMAGE_NAME"
    echo -e "${GREEN}✓ Image pushed to Docker Hub${NC}"
    echo -e "${GREEN}  Image: ${FULL_IMAGE_NAME}${NC}"
}

# Function to deploy to Railway
deploy_railway() {
    if ! command -v railway &> /dev/null; then
        echo -e "${YELLOW}Installing Railway CLI...${NC}"
        npm install -g @railway/cli
    fi
    
    echo -e "${BLUE}Deploying to Railway...${NC}"
    railway up
    echo -e "${GREEN}✓ Deployed to Railway${NC}"
}

# Function to deploy to Render
deploy_render() {
    echo -e "${BLUE}Deploying to Render...${NC}"
    echo -e "${YELLOW}Note: Render deployment requires:${NC}"
    echo -e "  1. Connect your GitHub repository to Render"
    echo -e "  2. Create a new Web Service"
    echo -e "  3. Set build command: docker build -t backend ."
    echo -e "  4. Set start command: gunicorn --bind 0.0.0.0:\$PORT --workers 4 app:app"
    echo -e "  5. Set environment variables"
    echo ""
    echo -e "${GREEN}Or use Render CLI:${NC}"
    echo -e "  render deploy"
}

# Function to deploy to Heroku
deploy_heroku() {
    if ! command -v heroku &> /dev/null; then
        echo -e "${YELLOW}Installing Heroku CLI...${NC}"
        echo -e "  Visit: https://devcenter.heroku.com/articles/heroku-cli"
        return 1
    fi
    
    echo -e "${BLUE}Deploying to Heroku...${NC}"
    
    # Create Procfile if it doesn't exist
    if [ ! -f "Procfile" ]; then
        echo "web: gunicorn --bind 0.0.0.0:\$PORT --workers 4 app:app" > Procfile
    fi
    
    # Login and deploy
    heroku login
    heroku create "${HEROKU_APP_NAME:-ecommerce-backend-$(date +%s)}" || true
    git push heroku main || heroku git:remote -a "$(heroku apps:info | grep 'Name:' | awk '{print $2}')" && git push heroku main
    
    echo -e "${GREEN}✓ Deployed to Heroku${NC}"
}

# Main deployment logic
case "$DEPLOYMENT_TARGET" in
    docker)
        build_image
        test_image
        echo ""
        echo -e "${GREEN}✓ Docker image ready${NC}"
        echo -e "${BLUE}To run locally:${NC}"
        echo -e "  docker run -d -p 5001:5001 --name backend ${IMAGE_NAME}:${IMAGE_TAG}"
        ;;
    
    dockerhub)
        build_image
        test_image
        push_to_dockerhub
        ;;
    
    railway)
        build_image
        deploy_railway
        ;;
    
    render)
        build_image
        deploy_render
        ;;
    
    heroku)
        deploy_heroku
        ;;
    
    *)
        echo -e "${RED}Unknown deployment target: $DEPLOYMENT_TARGET${NC}"
        echo ""
        echo "Usage: $0 [docker|dockerhub|railway|render|heroku]"
        echo ""
        echo "Examples:"
        echo "  $0 docker          # Build and test Docker image locally"
        echo "  $0 dockerhub       # Build and push to Docker Hub"
        echo "  $0 railway         # Deploy to Railway"
        echo "  $0 render          # Deploy to Render"
        echo "  $0 heroku          # Deploy to Heroku"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Deployment Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
