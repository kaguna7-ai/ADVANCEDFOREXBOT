# Trading Bot - Complete Setup & Build Guide

## 🚀 What You Have

A **production-ready Python trading bot** fully extracted from your Word document and ready to deploy!

## 📁 Project Files

```
Trading Bot Project
├── 🤖 Core Bot
│   ├── bot.py                          - Main trading bot
│   ├── app/healthcheck.py              - Health endpoint
│   └── config.yaml                     - Strategy config
│
├── 📦 Deployment  
│   ├── Dockerfile                      - Docker image
│   ├── docker-compose.yml              - Docker Compose
│   ├── requirements.txt                - Python dependencies
│   └── .env.example                    - API credentials template
│
├── 🔧 Scripts
│   ├── setup.sh                        - First-time setup
│   ├── build.sh                        - Build for local/Docker
│   └── run.sh                          - Run bot (multiple modes)
│
└── 📚 Documentation
    ├── README.md                       - Complete documentation
    ├── SETUP.md                        - This guide
    ├── QUICKSTART.md                   - 5-minute start
    ├── SECURITY_NOTES.md               - Security checklist
    └── .gitignore                      - Git ignore rules
```

## ⚡ 3-Step Quick Start

### 1. Initialize (1 minute)
```bash
cd /workspaces/ADVANCEDFOREXBOT
./setup.sh
```

### 2. Configure (2 minutes)
```bash
# Add your exchange API keys
nano .env

# (Optional) Adjust trading parameters
nano config.yaml
```

### 3. Run (30 seconds)
```bash
# Choose ONE method below:

# Method A - Local Python (fastest for development)
./run.sh local

# Method B - Docker (self-contained, reproducible)
./build.sh docker
./run.sh docker

# Method C - Docker Compose (production-ready)
./build.sh docker-compose
./run.sh docker-compose-daemon
```

## 📖 Documentation

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **QUICKSTART.md** | Get running in 5 minutes | 2 min |
| **README.md** | Full feature documentation | 10 min |
| **SECURITY_NOTES.md** | Security best practices | 5 min |
| **SETUP.md** | This setup guide | 5 min |

## 🛠️ Build Options

### Option 1: Local Python (Development)
```bash
./build.sh local
./run.sh local
```
✅ Fastest  
✅ Easy to modify  
⚠️ Requires Python 3.9+

### Option 2: Docker (Production Single)
```bash
./build.sh docker
./run.sh docker              # Foreground
./run.sh docker-daemon       # Background
```
✅ Self-contained  
✅ Consistent environment  
✅ Easy deployment  
⚠️ Requires Docker

### Option 3: Docker Compose (Production Multi)
```bash
./build.sh docker-compose
./run.sh docker-compose-daemon
```
✅ Production-grade  
✅ Resource limits  
✅ Health checks  
⚠️ Requires Docker & Docker Compose

## 🎯 Common Tasks

### First Time Setup
```bash
chmod +x *.sh              # Make scripts executable
./setup.sh                 # Initialize environment
nano .env                  # Add API credentials
```

### Run the Bot
```bash
./run.sh local             # Local Python
./run.sh docker            # Docker foreground
./run.sh docker-daemon     # Docker background
```

### Monitor the Bot
```bash
./run.sh logs local        # View logs (local)
./run.sh logs docker       # View Docker logs
docker-compose logs -f     # Docker Compose logs
tail -f logs/*.log         # Live log tail
```

### Stop the Bot
```bash
./run.sh stop              # Stop all instances
Ctrl+C                     # Stop foreground process
```

### Deploy to Production
```bash
# Option 1: VPS with Docker Compose
scp -r . user@server:/home/trading-bot
ssh user@server "cd /home/trading-bot && ./setup.sh && ./run.sh docker-compose-daemon"

# Option 2: As Systemd Service
sudo cp trading-bot.service /etc/systemd/system/
sudo systemctl enable trading-bot
sudo systemctl start trading-bot
```

## 🔐 Security Setup

1. **Never commit .env with real keys** ✅ Already in .gitignore
2. **Test in sandbox first** ✅ Set ENV=sandbox in .env
3. **Use small amounts initially** ✅ Start with low ACCOUNT_EQUITY_USD
4. **Monitor actively** ✅ Check logs frequently

See `SECURITY_NOTES.md` for complete security checklist.

## ⚙️ Configuration

### .env (API Credentials)
```bash
EXCHANGE=binance              # Exchange name
API_KEY=xxx                   # Your API key
API_SECRET=xxx                # Your API secret
ACCOUNT_EQUITY_USD=1000       # Starting capital
ENV=sandbox                   # sandbox or production
```

### config.yaml (Strategy)
```yaml
exchange: binance
symbol: BTC/USDT              # Trading pair
timeframe: 1m                 # Candle time
strategy:
  ema_short: 9                # Short moving average
  ema_long: 21                # Long moving average
  rsi_period: 14              # RSI indicator
risk:
  max_position_size_pct: 0.02 # Risk per trade (%)
```

## 🚦 Strategy Explained

The bot uses **EMA Crossover + RSI** strategy:

```
BUY when:
  - Short EMA crosses ABOVE Long EMA
  - AND RSI < 70 (not overbought)

SELL when:
  - Short EMA crosses BELOW Long EMA
  - AND RSI > 30 (not oversold)
```

## 📊 What Gets Logged

```
logs/
├── bot_YYYY-MM-DD.log       # Daily bot logs
├── trades_YYYY-MM-DD.log    # Daily trade logs
└── errors_YYYY-MM-DD.log    # Error logs
```

View logs:
```bash
tail -f logs/*.log
```

## 🔄 Workflow

### Development
```
1. ./setup.sh          (One-time)
2. nano .env           (Configure)
3. ./run.sh local      (Test locally)
4. tail -f logs/*.log  (Monitor)
```

### Production
```
1. ./setup.sh                    (One-time)
2. nano .env                     (Configure with real keys)
3. ./build.sh docker-compose     (Build once)
4. ./run.sh docker-compose-daemon (Run background)
5. ./run.sh logs docker-compose  (Monitor)
```

## ✅ Pre-Launch Checklist

- [ ] Python 3.9+ installed (check: `python3 --version`)
- [ ] .env configured with API keys
- [ ] Tested in sandbox mode (set ENV=sandbox)
- [ ] Strategy parameters reviewed in config.yaml
- [ ] Started with small position size (1-2%)
- [ ] Monitoring set up (checking logs)
- [ ] Kill switch ready (know how to stop bot)
- [ ] Read SECURITY_NOTES.md

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'ccxt'"
```bash
pip install -r requirements.txt
```

### "API connection failed"
```bash
# Check credentials in .env
# Verify exchange status
# Try testnet first
```

### "Docker image build failed"
```bash
docker build --no-cache -t trading-bot .
```

### "Permission denied" on scripts
```bash
chmod +x *.sh
```

## 📱 Supported Exchanges

The bot uses CCXT, which supports 100+ exchanges:
- **Major**: Binance, Bybit, Kraken, Coinbase
- **Emerging**: Bitget, OKX, Huobi, Kucoin
- **Testnet**: Most exchanges have sandbox/testnet

See bot.py EXCHANGE_ID configuration.

## 💡 Next Steps After Launch

1. **Monitor daily** - Check logs, verify orders placed
2. **Paper trade** - Use testnet for 2-4 weeks minimum
3. **Backtest** - Use vectorbt/backtrader with historical data
4. **Optimize** - Adjust parameters based on results
5. **Scale** - Increase position sizes gradually

## 📚 Resources

- **CCXT Docs**: https://docs.ccxt.com/
- **Exchange APIs**: Binance, Bybit, Kraken (official docs)
- **TA Indicators**: https://github.com/bukosabino/ta
- **Trading Tips**: See SECURITY_NOTES.md

## 🎓 Learning Path

1. **Read**: QUICKSTART.md (5 min)
2. **Setup**: ./setup.sh (1 min)
3. **Configure**: .env + config.yaml (2 min)
4. **Test**: ./run.sh local (5 min)
5. **Read**: README.md (10 min)
6. **Read**: SECURITY_NOTES.md (5 min)
7. **Deploy**: Choose your method (5 min)

**Total**: ~30 minutes to go from setup to deployment!

## 🚀 You're Ready!

Your trading bot is fully set up and ready to:
- ✅ Run locally for testing
- ✅ Run in Docker for production
- ✅ Deploy to cloud/VPS
- ✅ Monitor with logs
- ✅ Trade across 100+ exchanges

**Start with**: `./setup.sh`

Then choose: **QUICKSTART.md** or **README.md**

---

**Last Updated**: November 24, 2025  
**Bot Version**: Production-Ready  
**Status**: Ready to Deploy ✅
