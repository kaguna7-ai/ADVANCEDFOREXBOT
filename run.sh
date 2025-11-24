#!/bin/bash

# Run script for the Trading Bot
# This script handles running the bot locally or in Docker

set -e

PROJECT_NAME="trading-bot"
DOCKER_IMAGE="$PROJECT_NAME:latest"

echo "=================================="
echo "Trading Bot Runner"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check dependencies
check_env() {
    if [ ! -f ".env" ]; then
        print_error ".env file not found!"
        print_status "Creating .env from .env.example..."
        cp .env.example .env
        print_error "Please edit .env with your API keys and run again"
        exit 1
    fi
}

# Parse arguments
RUN_MODE=${1:-local}

case $RUN_MODE in
    local)
        print_status "Running bot locally..."
        check_env
        
        # Check if dependencies are installed
        if ! python3 -c "import ccxt" 2>/dev/null; then
            print_warning "Dependencies not installed. Installing..."
            pip install -r requirements.txt
        fi
        
        print_status "Starting bot..."
        python3 bot.py
        ;;
    
    docker)
        print_status "Running bot in Docker..."
        check_env
        
        # Build if image doesn't exist
        if ! docker image inspect "$DOCKER_IMAGE" &>/dev/null; then
            print_status "Building Docker image..."
            docker build -t "$DOCKER_IMAGE" .
        fi
        
        print_status "Starting Docker container..."
        docker run --rm \
            --env-file .env \
            -v "$(pwd)/config.yaml:/app/config.yaml" \
            -v "$(pwd)/logs:/app/logs" \
            "$DOCKER_IMAGE"
        ;;
    
    docker-daemon)
        print_status "Running bot in Docker (daemon mode)..."
        check_env
        
        # Build if image doesn't exist
        if ! docker image inspect "$DOCKER_IMAGE" &>/dev/null; then
            print_status "Building Docker image..."
            docker build -t "$DOCKER_IMAGE" .
        fi
        
        # Stop existing container if running
        if docker ps | grep -q "$PROJECT_NAME"; then
            print_status "Stopping existing container..."
            docker stop "$PROJECT_NAME" || true
        fi
        
        print_status "Starting Docker container (background)..."
        docker run -d \
            --name "$PROJECT_NAME" \
            --restart unless-stopped \
            --env-file .env \
            -v "$(pwd)/config.yaml:/app/config.yaml" \
            -v "$(pwd)/logs:/app/logs" \
            "$DOCKER_IMAGE"
        
        print_status "Container started! Use 'docker logs $PROJECT_NAME' to view logs"
        ;;
    
    docker-compose)
        print_status "Running with Docker Compose..."
        check_env
        
        if [ ! -f "docker-compose.yml" ]; then
            print_error "docker-compose.yml not found!"
            print_status "Run './build.sh docker-compose' first"
            exit 1
        fi
        
        docker-compose up
        ;;
    
    docker-compose-daemon)
        print_status "Running with Docker Compose (daemon mode)..."
        check_env
        
        if [ ! -f "docker-compose.yml" ]; then
            print_error "docker-compose.yml not found!"
            print_status "Run './build.sh docker-compose' first"
            exit 1
        fi
        
        docker-compose up -d
        print_status "Service started in background!"
        print_status "View logs with: docker-compose logs -f"
        ;;
    
    stop)
        print_status "Stopping bot..."
        if docker ps | grep -q "$PROJECT_NAME"; then
            docker stop "$PROJECT_NAME"
            print_status "Container stopped"
        fi
        
        if command -v docker-compose &> /dev/null; then
            docker-compose down 2>/dev/null || true
        fi
        ;;
    
    logs)
        MODE=${2:-local}
        case $MODE in
            docker)
                docker logs -f "$PROJECT_NAME"
                ;;
            docker-compose)
                docker-compose logs -f
                ;;
            *)
                print_error "Unknown logs mode: $MODE"
                ;;
        esac
        ;;
    
    health)
        print_status "Checking bot health..."
        if docker ps | grep -q "$PROJECT_NAME"; then
            STATUS=$(docker inspect -f '{{.State.Status}}' "$PROJECT_NAME")
            print_status "Container status: $STATUS"
        else
            print_warning "Container not running"
        fi
        ;;
    
    help)
        echo "Usage: ./run.sh [mode] [options]"
        echo ""
        echo "Modes:"
        echo "  local                    Run bot locally (default)"
        echo "  docker                   Run bot in Docker container (foreground)"
        echo "  docker-daemon            Run bot in Docker (background)"
        echo "  docker-compose           Run with Docker Compose (foreground)"
        echo "  docker-compose-daemon    Run with Docker Compose (background)"
        echo "  stop                     Stop running bot/container"
        echo "  logs [mode]              View logs (docker or docker-compose)"
        echo "  health                   Check bot health"
        echo "  help                     Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./run.sh local                   # Run locally"
        echo "  ./run.sh docker                  # Run in Docker foreground"
        echo "  ./run.sh docker-daemon           # Run in Docker background"
        echo "  ./run.sh docker-daemon logs      # View Docker logs"
        echo "  ./run.sh docker-compose-daemon   # Run with Docker Compose background"
        echo "  ./run.sh stop                    # Stop running bot"
        ;;
    
    *)
        print_error "Unknown mode: $RUN_MODE"
        echo "Use './run.sh help' for usage information"
        exit 1
        ;;
esac
