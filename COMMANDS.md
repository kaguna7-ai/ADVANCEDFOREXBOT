# 🚀 Quick Command Reference

## First Time Only
```bash
chmod +x *.sh              # Make scripts executable
./setup.sh                 # Initialize and install dependencies
nano .env                  # Configure with your API keys
```

## Running the Bot

### Local Python (Fastest)
```bash
./run.sh local
```

### Docker (Self-contained)
```bash
./build.sh docker          # One-time build
./run.sh docker            # Run in foreground
./run.sh docker-daemon     # Run in background
```

### Docker Compose (Production)
```bash
./build.sh docker-compose  # One-time setup
./run.sh docker-compose-daemon  # Run in background
docker-compose logs -f     # View logs
docker-compose down        # Stop
```

## Monitoring

```bash
tail -f logs/*.log                 # Watch logs live
./run.sh logs docker               # Docker logs
docker-compose logs -f             # Docker Compose logs
./run.sh health                    # Check status
```

## Stopping

```bash
./run.sh stop              # Stop all instances
Ctrl+C                     # Stop foreground process
docker-compose down        # Stop Docker Compose
```

## Configuration

```bash
nano .env                  # Edit API credentials
nano config.yaml           # Edit strategy parameters
```

## Building

```bash
./build.sh local           # Local Python build
./build.sh docker          # Docker image build
./build.sh docker-compose  # Docker Compose setup
./build.sh clean           # Clean artifacts
```

## Documentation

```bash
cat INDEX.md               # Start here
cat QUICKSTART.md          # 5-minute guide
cat README.md              # Full documentation
cat SECURITY_NOTES.md      # Security best practices
```

## Useful One-Liners

```bash
# Test configuration
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Check dependencies
pip list | grep -E "ccxt|pandas|numpy"

# Verify Python version
python3 --version

# Build and run in one command
./build.sh local && ./run.sh local

# View last 50 lines of logs
tail -50 logs/*.log

# Clean and rebuild Docker
docker system prune -a --volumes && ./build.sh docker
```

## Environment Variables

```bash
# Copy template
cp .env.example .env

# Required variables
EXCHANGE=binance
API_KEY=your_key_here
API_SECRET=your_secret_here
ACCOUNT_EQUITY_USD=1000
ENV=production  # or "sandbox" for testing
```

## Troubleshooting Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Verify config
python3 -c "import yaml; print(yaml.safe_load(open('config.yaml')))"

# Check logs for errors
grep -i error logs/*.log

# Rebuild Docker image
docker build --no-cache -t trading-bot .

# List running containers
docker ps

# View container logs
docker logs -f trading-bot

# Remove container
docker rm trading-bot
```

## File Shortcuts

```bash
# Edit files
nano bot.py                # Main bot code
nano config.yaml           # Trading strategy config
nano .env                  # API credentials
nano app/healthcheck.py    # Health endpoint

# View documentation
cat README.md              # Full docs
cat QUICKSTART.md          # Quick start
cat SECURITY_NOTES.md      # Security checklist
```

## Docker Compose Commands

```bash
docker-compose up                    # Run foreground
docker-compose up -d                 # Run background
docker-compose down                  # Stop
docker-compose logs -f               # View logs
docker-compose ps                    # List services
docker-compose restart               # Restart services
docker-compose build --no-cache      # Rebuild
```

## Production Deployment

```bash
# Deploy to VPS
scp -r . user@server:/opt/trading-bot
ssh user@server "cd /opt/trading-bot && ./setup.sh"

# Enable auto-start (Systemd)
sudo systemctl enable trading-bot
sudo systemctl start trading-bot
sudo systemctl status trading-bot
```

## Health Checks

```bash
# Check Python
python3 --version

# Check dependencies
pip list

# Check config
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Check Docker
docker --version
docker ps

# Test local server
curl -X GET http://localhost:8000/health
```

---

**Start with**: `./setup.sh` then `./run.sh local`

**Questions?**: Read `INDEX.md` or `README.md`

**Security?**: Review `SECURITY_NOTES.md` before going live
