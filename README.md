# Trading Bot

## Overview
This is a production-minded trading bot written in Python. It is modular: data ingest, indicators, risk sizing, and order placement are separated so you can replace any part.

**Important:** Trading is risky. Test thoroughly in sandbox/testnet and with small amounts before using real capital.

## Features
- Uses CCXT for exchange connectivity (many exchanges supported)
- Indicator-based strategy (EMA crossover + RSI)
- Risk-based position sizing
- Environment-based secret management (.env)
- Dockerized for deployment
- FastAPI health check endpoint

## Security & Best Practices
- Never commit `.env` to git. Use a secrets manager (AWS Secrets Manager, HashiCorp Vault, Google Secret Manager) in production.
- Use exchange testnets / paper trading first.
- Protect the host and limit API key permissions (withdrawal disabled, IP restrictions if supported).

## Prerequisites
- Python 3.11+
- Docker (optional, for containerized deployment)
- pip (Python package manager)

## Local Setup & Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and fill in your exchange API keys
```

### 3. Configure Strategy
Edit `config.yaml` to adjust:
- Exchange and symbol (e.g., BTC/USDT)
- Timeframe (1m, 5m, 15m, etc.)
- EMA and RSI parameters
- Risk settings (position size %, stop loss %, take profit %)

### 4. Run the Bot
```bash
python bot.py
```

## Docker Setup & Run

### 1. Build Docker Image
```bash
docker build -t trading-bot .
```

### 2. Run Container
```bash
docker run --env-file .env -v $(pwd)/config.yaml:/app/config.yaml trading-bot
```

Or with docker-compose (create `docker-compose.yml`):
```yaml
version: '3.8'
services:
  trading-bot:
    build: .
    env_file: .env
    volumes:
      - ./config.yaml:/app/config.yaml
    restart: unless-stopped
```

Then run:
```bash
docker-compose up -d
```

## Project Structure
```
.
├── bot.py                 # Main trading bot entry point
├── app/
│   └── healthcheck.py     # FastAPI health check endpoint
├── config.yaml            # Strategy and risk configuration
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── Dockerfile             # Docker container definition
└── README.md              # This file
```

## Extending the Bot

### Replace Strategy
Implement your own strategy by modifying the signal logic in `run_loop()`:
- Use backtesting frameworks (vectorbt or backtrader) for research
- Add websocket connectors for lower latency
- Implement additional indicators

### Add Persistence
- Add persistent database (PostgreSQL) for trade logs and analytics
- Implement trade history tracking and performance metrics

### Improve Monitoring
- Add Prometheus metrics for monitoring
- Integrate with Grafana for dashboards
- Set up alerting (Telegram, Slack, email)

## Testing

### Paper Trading (Sandbox)
Before running on real capital, test with your exchange's testnet:
1. Create a testnet/sandbox account on your exchange
2. Update `API_KEY` and `API_SECRET` in `.env` with testnet credentials
3. Adjust `ACCOUNT_EQUITY_USD` to a small test amount
4. Run the bot and monitor for correct signals and order placement

### Backtesting
Use vectorbt or backtrader to backtest the strategy with historical data before going live.

## Performance Considerations
- For low capital accounts (<$50), profit targets must account for fees and slippage
- Consider maker-first order placement to capture rebates
- Use adaptive volatility filters (ATR) to avoid unfavorable trading conditions
- Implement micro-position sizing to diversify risk

## Security Checklist
- [ ] Never commit `.env` file with real API keys
- [ ] Use short-lived API keys and rotate them regularly
- [ ] Enable IP whitelisting on exchange API keys
- [ ] Disable withdrawal permissions on API keys
- [ ] Test thoroughly in sandbox before going live
- [ ] Use TLS for all network traffic
- [ ] Monitor logs for unusual fills or execution failures
- [ ] Set up alerts for abnormal trading activity

## Troubleshooting

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Exchange Connection Issues
- Verify API keys are correct and enabled
- Check exchange status page
- Ensure API key permissions include trading on your symbol
- Verify network connectivity

### Order Placement Failures
- Check account has sufficient balance
- Verify symbol is correct and active on exchange
- Review order size relative to account equity and maximum position size
- Check if leverage is enabled if required

### Configuration Issues
- Validate `config.yaml` YAML syntax
- Ensure all required keys are present in configuration
- Check that strategy parameters are reasonable

## Support & Contributing
For issues or improvements, please refer to the project documentation or contact support.

## License
Refer to the LICENSE file for licensing information.

## Disclaimer
Trading cryptocurrencies or forex carries risk. This bot is provided as-is without warranty. Past performance does not guarantee future results. Use at your own risk and start with small amounts only.
