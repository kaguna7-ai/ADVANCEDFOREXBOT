# Advanced Forex Bot - Build & Deployment Instructions

## Project Summary

This is a **production-ready Python trading bot** for cryptocurrency and forex trading built with:
- **CCXT** - Multi-exchange connectivity
- **FastAPI** - Health check endpoint
- **Pandas/NumPy** - Data analysis
- **TA-Lib** - Technical indicators (EMA, RSI)
- **Docker** - Containerization for easy deployment

## What's Been Set Up

Your workspace now has a complete, ready-to-run trading bot with:

✅ **Core Bot Code**
- `bot.py` - Main trading bot with EMA crossover + RSI strategy
- `app/healthcheck.py` - FastAPI health endpoint

✅ **Configuration Files**
- `config.yaml` - Strategy and risk parameters
- `.env.example` - API credentials template (copy to .env and fill in)
- `requirements.txt` - All Python dependencies

✅ **Containerization**
- `Dockerfile` - Docker image for production deployment
- `docker-compose.yml` - Pre-configured Docker Compose setup

✅ **Build & Run Scripts**
- `build.sh` - Smart build script for local/Docker builds
- `run.sh` - Run bot locally or in Docker with multiple modes
- `setup.sh` - First-time environment setup

✅ **Documentation**
- `README.md` - Complete documentation
- `SECURITY_NOTES.md` - Security best practices
- `QUICKSTART.md` - 5-minute quick start guide
- `.gitignore` - Git configuration (never commits API keys)

## Quick Start (2 Minutes)

### Step 1: Initialize
```bash
cd /workspaces/ADVANCEDFOREXBOT
chmod +x setup.sh build.sh run.sh
./setup.sh
```

### Step 2: Configure (IMPORTANT!)
```bash
# Edit .env with your exchange API keys
nano .env

# Verify config (optional - edit trading parameters)
nano config.yaml
```

### Step 3: Run
Choose your preferred method:

**Option A - Local Python (fastest):**
```bash
./run.sh local
```

**Option B - Docker (self-contained):**
```bash
./build.sh docker
./run.sh docker
```

**Option C - Docker Compose (production):**
```bash
./build.sh docker-compose
./run.sh docker-compose-daemon
./run.sh logs docker-compose
```

## Build Methods Explained

### Local Python Build
**Best for:** Development, testing, quick iteration
```bash
./build.sh local
# Installs: pip install -r requirements.txt
# Runs: python bot.py
```

### Docker Build
**Best for:** Single deployment, consistent environment
```bash
./build.sh docker
./run.sh docker              # Run foreground
./run.sh docker-daemon       # Run background
./run.sh stop                # Stop bot
./run.sh logs docker         # View logs
```

### Docker Compose Build
**Best for:** Production, multiple services, advanced configs
```bash
./build.sh docker-compose
./run.sh docker-compose-daemon       # Run background
./run.sh logs docker-compose         # View logs
docker-compose down                  # Stop
```

## File Structure

```
/workspaces/ADVANCEDFOREXBOT/
├── bot.py                    # Main trading bot entry point
├── app/
│   └── healthcheck.py        # FastAPI health check
├── config.yaml               # Strategy configuration
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── Dockerfile                # Docker image definition
├── docker-compose.yml        # Docker Compose configuration
├── build.sh                  # Build script
├── run.sh                    # Run script
├── setup.sh                  # Setup script
├── .gitignore                # Git ignore patterns
├── README.md                 # Full documentation
├── QUICKSTART.md             # 5-minute guide
└── SECURITY_NOTES.md         # Security best practices
```

## Configuration Guide

### .env File (API Credentials)
```bash
EXCHANGE=binance              # Your exchange (binance, bybit, kraken, etc.)
API_KEY=your_key_here         # Your exchange API key
API_SECRET=your_secret_here   # Your exchange API secret
ACCOUNT_EQUITY_USD=1000       # Your starting capital
ENV=production                # production or sandbox
```

### config.yaml (Strategy Parameters)
```yaml
exchange: binance
symbol: BTC/USDT              # Trading pair
timeframe: 1m                 # Candle interval
strategy:
  ema_short: 9                # Short EMA period
  ema_long: 21                # Long EMA period
  rsi_period: 14              # RSI period
risk:
  max_position_size_pct: 0.02 # Risk 2% per trade
  stop_loss_pct: 0.01         # 1% stop loss
  take_profit_pct: 0.02       # 2% take profit
```

## Strategy Explained

The bot implements a **EMA Crossover Strategy**:

1. **Buy Signal**: When short EMA crosses above long EMA AND RSI < 70
2. **Sell Signal**: When short EMA crosses below long EMA AND RSI > 30
3. **Position Sizing**: Based on account equity and max risk per trade
4. **Execution**: Market orders via exchange API

## Deployment Options

### Option 1: Local Server
```bash
ssh your-server.com
cd /path/to/bot
./run.sh local
```

### Option 2: Docker (VPS/Cloud)
```bash
docker build -t trading-bot .
docker run --env-file .env --restart=always trading-bot
```

### Option 3: Docker Compose (Production)
```bash
docker-compose up -d
docker-compose logs -f
```

### Option 4: Systemd Service (Linux)
```bash
sudo nano /etc/systemd/system/trading-bot.service
sudo systemctl enable trading-bot
sudo systemctl start trading-bot
```

## Safety Checklist

Before running with real money:

- [ ] Test in **sandbox/testnet** first
- [ ] Use **small amounts** initially (< $100)
- [ ] Review logs: `tail -f logs/*.log`
- [ ] Verify strategy in backtesting
- [ ] Set `max_position_size_pct: 0.01` (1% per trade)
- [ ] Never commit `.env` file with real keys
- [ ] Use API key IP whitelist on exchange
- [ ] Disable withdrawal permissions
- [ ] Monitor actively for first week
- [ ] Have a kill switch ready: `./run.sh stop`

## Advanced Usage

### Modify Trading Strategy
Edit `bot.py` in the `run_loop()` function to:
- Add custom indicators
- Change signal logic
- Implement stop-loss/take-profit
- Add multiple symbols

### Add Database Logging
Extend `place_order()` to log trades to PostgreSQL/MongoDB

### Integrate Monitoring
Add alerts via Telegram, Slack, or Discord

### Backtest Strategy
Use vectorbt or backtrader with historical data

## Troubleshooting

### Bot won't start
```bash
python3 --version              # Check Python 3.9+
pip list | grep ccxt           # Verify dependencies
python3 -c "import yaml; yaml.safe_load(open('config.yaml'))"
```

### API connection fails
```bash
# Check API keys in .env
# Verify exchange status
# Try testnet first
```

### Docker issues
```bash
docker logs trading-bot        # View logs
docker build --no-cache .      # Rebuild
docker rm trading-bot          # Clean up
```

## Support & Documentation

- **Quick Start**: `QUICKSTART.md` (5 minutes)
- **Full Docs**: `README.md` (comprehensive)
- **Security**: `SECURITY_NOTES.md` (important!)
- **Logs**: `logs/` directory

## Next Steps

1. **Run setup**: `./setup.sh`
2. **Edit .env**: Add your API credentials
3. **Test in sandbox**: Set `ENV=sandbox` in .env
4. **Run bot**: `./run.sh local` or `./run.sh docker`
5. **Monitor**: `tail -f logs/*.log`
6. **Go live** (after successful sandbox testing)

## Important Notes

- ⚠️ **Trading is risky** - Start small!
- ⚠️ **Never commit .env** with real API keys
- ⚠️ **Always test in sandbox** before going live
- ⚠️ **Monitor actively** the first week
- ✅ **Backup your config** regularly
- ✅ **Keep dependencies updated**: `pip install -r requirements.txt --upgrade`

---

**Your bot is ready to use. Read QUICKSTART.md for 5-minute startup guide!**
