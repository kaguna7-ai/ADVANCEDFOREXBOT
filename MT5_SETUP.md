# **IMPORTANT: MetaTrader5 Setup Instructions**

MetaTrader5 is a Windows-only application. To use this bot with MT5, follow these steps:

## Step 1: Install MetaTrader5 on Windows

1. Download MetaTrader5 from your broker (e.g., Pepperstone, Exness, FxPro, etc.)
2. Install on Windows
3. Create a trading account with your broker
4. Get your credentials:
   - Account Number (MT5_LOGIN)
   - Password
   - Server Name

## Step 2: Install Python MetaTrader5 Module

On Windows, open Command Prompt or PowerShell and run:

```bash
pip install MetaTrader5
```

Or with your virtualenv activated:

```bash
.\venv\Scripts\activate
pip install MetaTrader5
```

## Step 3: Configure Your Credentials

Edit `.env` file and fill in your MT5 credentials:

```env
MT5_BROKER=YourBroker
MT5_LOGIN=12345678
MT5_PASSWORD=your_password
MT5_SERVER=YourBroker-Demo
ENV=production
```

## Step 4: Configure Trading Settings

Edit `config.yaml` for your preferred:
- Symbol (EURUSD, GBPUSD, AUDUSD, etc.)
- Timeframe (1m, 5m, 15m, 1h, 4h, 1d)
- Strategy parameters (EMA periods, RSI period)
- Risk management (position size, stop loss, take profit)

Example for Forex (1-hour):
```yaml
symbol: EURUSD
timeframe: 1h
strategy:
  ema_short: 9
  ema_long: 21
  rsi_period: 14
```

## Step 5: Run the Bot

### On Windows (Local Python):

```bash
# Activate virtualenv
.\venv\Scripts\activate

# Run bot
python bot.py
```

### Using Docker (Windows with Docker Desktop):

```bash
# Build Docker image
.\build.sh docker

# Run in Docker
.\run.sh docker
```

## Important Security Notes

⚠️ **NEVER commit `.env` with real credentials to git!**

- Keep API credentials secure
- Use demo/sandbox accounts for testing first
- Start with small position sizes
- Monitor actively
- Have a kill switch ready (Ctrl+C)

## Supported Brokers

MetaTrader5 works with these and many more:
- Pepperstone
- Exness
- FxPro
- IC Markets
- Axiory
- eToro
- Many others

Visit your broker's website to download MT5 and create an account.

## Troubleshooting

### "ModuleNotFoundError: No module named 'MetaTrader5'"

You're not on Windows or pip install failed. Solutions:
1. Ensure you're on Windows (MetaTrader5 is Windows-only)
2. Run: `pip install MetaTrader5`
3. Check Python architecture matches your system (32-bit vs 64-bit)

### "MT5 initialization failed"

- Verify MT5 is installed and running
- Check credentials in `.env` are correct
- Check server name is exactly correct (case-sensitive)
- Verify account is not locked
- Try demo account credentials first

### "Invalid login or password"

- Check `.env` credentials match your MT5 account
- Password is case-sensitive
- Try login directly in MT5 to verify credentials

## Next Steps

1. Install MetaTrader5 on Windows
2. Create trading account with broker
3. Get credentials and update `.env`
4. Run: `python bot.py`
5. Monitor logs and trade history

**Ready to trade on MT5!** 🚀
