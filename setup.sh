#!/bin/bash

# Setup script - One-time initialization
# This script prepares the environment for the first time

set -e

echo "=================================="
echo "Trading Bot Setup Script"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check Python version
print_status "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
    print_status "Python $PYTHON_VERSION found (required: $REQUIRED_VERSION+)"
else
    print_error "Python 3.9+ required, found $PYTHON_VERSION"
    exit 1
fi

# Create .env if not exists
print_status "Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_warning "Created .env - Please edit with your API credentials:"
    echo "  - EXCHANGE: Set to 'binance', 'bybit', etc."
    echo "  - API_KEY: Your exchange API key"
    echo "  - API_SECRET: Your exchange API secret"
    echo "  - ACCOUNT_EQUITY_USD: Starting capital"
    echo "  - ENV: 'sandbox' for testing, 'production' for live"
else
    print_status ".env already exists"
fi

# Create config.yaml if not exists
if [ ! -f "config.yaml" ]; then
    print_warning "config.yaml not found. Creating default..."
    cp -n config.yaml.default config.yaml 2>/dev/null || true
fi

# Create logs directory
if [ ! -d "logs" ]; then
    mkdir -p logs
    print_status "Created logs directory"
else
    print_status "logs directory exists"
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip setuptools wheel --quiet
pip install -r requirements.txt --quiet

print_status "Installation complete!"
echo ""
echo "=================================="
echo "Next steps:"
echo "=================================="
echo "1. Edit .env with your exchange credentials:"
echo "   nano .env"
echo ""
echo "2. Edit config.yaml to adjust strategy parameters"
echo ""
echo "3. Test in sandbox mode first:"
echo "   - Set ENV=sandbox in .env"
echo "   - Use sandbox API keys"
echo ""
echo "4. Run the bot:"
echo "   ./run.sh local        # Run locally"
echo "   ./run.sh docker       # Run in Docker"
echo ""
echo "5. View documentation:"
echo "   cat README.md"
echo ""
echo "=================================="
echo ""
print_warning "IMPORTANT: Never commit .env with real API keys!"
print_warning "Always test in sandbox/paper trading first!"
