#!/bin/bash

# Build script for the Trading Bot
# This script handles all build tasks

set -e

PROJECT_NAME="trading-bot"
DOCKER_IMAGE="$PROJECT_NAME:latest"

echo "=================================="
echo "Trading Bot Build Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if .env exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found!"
    print_status "Creating .env from .env.example..."
    cp .env.example .env
    print_warning "Please edit .env with your API keys before running the bot"
fi

# Check if config.yaml exists
if [ ! -f "config.yaml" ]; then
    print_error "config.yaml not found!"
    exit 1
fi

# Parse arguments
BUILD_TYPE=${1:-local}

case $BUILD_TYPE in
    local)
        print_status "Building for local execution..."
        print_status "Installing Python dependencies..."
        pip install -r requirements.txt
        print_status "Build complete!"
        print_status "To run: python bot.py"
        ;;
    docker)
        print_status "Building Docker image: $DOCKER_IMAGE..."
        docker build -t "$DOCKER_IMAGE" .
        print_status "Docker image built successfully!"
        print_status "To run: docker run --env-file .env $DOCKER_IMAGE"
        ;;
    docker-compose)
        print_status "Setting up Docker Compose..."
        if [ ! -f "docker-compose.yml" ]; then
            print_status "Creating docker-compose.yml..."
            cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  trading-bot:
    build: .
    container_name: trading-bot
    env_file: .env
    volumes:
      - ./config.yaml:/app/config.yaml
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
EOF
        fi
        print_status "Building with Docker Compose..."
        docker-compose build
        print_status "Docker Compose setup complete!"
        print_status "To run: docker-compose up -d"
        ;;
    clean)
        print_status "Cleaning build artifacts..."
        rm -rf __pycache__ .pytest_cache .coverage htmlcov
        find . -type f -name '*.pyc' -delete
        find . -type d -name '__pycache__' -delete
        print_status "Clean complete!"
        ;;
    help)
        echo "Usage: ./build.sh [option]"
        echo ""
        echo "Options:"
        echo "  local          Build for local Python execution (default)"
        echo "  docker         Build Docker image"
        echo "  docker-compose Setup Docker Compose configuration"
        echo "  clean          Remove build artifacts"
        echo "  help           Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./build.sh local          # Install Python dependencies locally"
        echo "  ./build.sh docker         # Build Docker image"
        echo "  ./build.sh docker-compose # Create and build docker-compose"
        ;;
    *)
        print_error "Unknown build type: $BUILD_TYPE"
        echo "Use './build.sh help' for usage information"
        exit 1
        ;;
esac

echo ""
print_status "Build process completed successfully!"
