# Trading Bot - Quick Start Guide

## 5-Minute Quick Start

### 1. Clone/Set Up
```bash
cd /path/to/ADVANCEDFOREXBOT
chmod +x setup.sh build.sh run.sh
./setup.sh
```

### 2. Configure
```bash
# Edit environment variables
nano .env

# Edit trading strategy
nano config.yaml
```

### 3. Run (Choose One)

**Local Python (fastest for development):**
```bash
./run.sh local
```

**Docker (reproducible, no Python install needed):**
```bash
# First time only
./build.sh docker

# Then run
./run.sh docker
```

**Docker Compose (with logging and resource limits):**
```bash
# First time only
./build.sh docker-compose

# Then run (background)
./run.sh docker-compose-daemon

# View logs
./run.sh logs docker-compose
```

## Production Deployment

### Option A: Systemd Service (Linux)

Create `/etc/systemd/system/trading-bot.service`:
```ini
[Unit]
Description=Trading Bot
After=network.target

[Service]
Type=simple
User=trading
WorkingDirectory=/path/to/bot
EnvironmentFile=/path/to/bot/.env
ExecStart=/path/to/bot/run.sh local
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

Start with:
```bash
sudo systemctl enable trading-bot
sudo systemctl start trading-bot
sudo systemctl status trading-bot
```

### Option B: Docker Compose on VPS

```bash
# Build and run
./run.sh docker-compose-daemon

# Stop
./run.sh stop

# View logs
docker-compose logs -f
```

### Option C: Kubernetes Deployment

See `k8s/` directory for deployment manifests (if available)

## File Structure

```
.
├── bot.py                 # Main bot code
├── config.yaml            # Strategy configuration
├── requirements.txt       # Python dependencies
├── .env.example           # Environment template
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose config
├── app/
│   └── healthcheck.py     # Health check endpoint
├── logs/                  # Bot logs (created)
├── build.sh              # Build script
├── run.sh                # Run script
├── setup.sh              # Setup script
└── README.md             # Full documentation
```

## Configuration Tips

### For Beginners
- Use **Binance testnet** with small amounts
- Set `max_position_size_pct: 0.01` (1% per trade)
- Use `ema_short: 9, ema_long: 21` (proven defaults)

### For Advanced Traders
- Modify indicator parameters in `config.yaml`
- Edit strategy logic in `bot.py` `run_loop()` function
- Add custom indicators from `ta` library
- Implement stop-loss and take-profit logic

## Monitoring

### View Logs
```bash
# Local
tail -f logs/*.log

# Docker
docker logs -f trading-bot

# Docker Compose
docker-compose logs -f
```

### Health Check
```bash
./run.sh health
```

## Troubleshooting

### Bot won't start
```bash
# Check Python
python3 --version

# Check dependencies
pip list | grep ccxt

# Verify config
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

### API connection issues
- Verify API keys in `.env`
- Check internet connection
- Verify exchange status
- Try testnet first

### Docker issues
```bash
# Rebuild image
docker build -t trading-bot .

# Check logs
docker logs trading-bot

# Remove old container
docker rm trading-bot
```

## Safety First!

1. **Always test in sandbox first**
   ```bash
   # In .env, set ENV=sandbox
   # Use testnet API keys
   ```

2. **Start with small amounts**
   ```bash
   # Set low ACCOUNT_EQUITY_USD
   # Keep position sizes tiny (1-2%)
   ```

3. **Monitor actively**
   ```bash
   tail -f logs/*.log
   # Watch for errors and unusual behavior
   ```

4. **Have a kill switch**
   ```bash
   ./run.sh stop    # Stop bot immediately
   ```

## Support

- Read full docs: `README.md`
- Security notes: `SECURITY_NOTES.md`
- Check logs: `logs/` directory
- Test strategy: Use backtesting first

---

**Remember:** Trading is risky. Start small, test thoroughly, and never risk capital you can't afford to lose!
