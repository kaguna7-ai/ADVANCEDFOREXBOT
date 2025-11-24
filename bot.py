import os
import time
import asyncio
import logging
from loguru import logger
import ccxt
import pandas as pd
import numpy as np
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
import yaml
from dotenv import load_dotenv

load_dotenv()

# Load config
with open('config.yaml', 'r') as f:
    cfg = yaml.safe_load(f)

EXCHANGE_ID = os.getenv('EXCHANGE', cfg.get('exchange', 'binance'))
API_KEY = os.getenv('API_KEY', '')
API_SECRET = os.getenv('API_SECRET', '')
SYMBOL = cfg.get('symbol', 'BTC/USDT')
TIMEFRAME = cfg.get('timeframe', '1m')
ENV_MODE = os.getenv('ENV', 'production')

# Secure exchange init (use CCXT)
exchange_class = getattr(ccxt, EXCHANGE_ID)
exchange_config = {
    'enableRateLimit': True,
    # optional: set the sandbox/testnet URLs via env
}

# Add API keys if provided
if API_KEY and API_SECRET:
    exchange_config['apiKey'] = API_KEY
    exchange_config['secret'] = API_SECRET

# Use testnet for sandbox mode
if ENV_MODE == 'sandbox':
    exchange_config['sandbox'] = True
    logger.info(f'Using {EXCHANGE_ID} testnet (sandbox mode)')

exchange = exchange_class(exchange_config)

# Utilities
async def sleep(seconds):
    await asyncio.sleep(seconds)


def fetch_ohlcv(limit=200):
    # fetch recent OHLCV
    ohlcv = exchange.fetch_ohlcv(SYMBOL, timeframe=TIMEFRAME, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df


def compute_indicators(df):
    df = df.copy()
    df['ema_short'] = EMAIndicator(df['close'], window=cfg['strategy']['ema_short']).ema_indicator()
    df['ema_long'] = EMAIndicator(df['close'], window=cfg['strategy']['ema_long']).ema_indicator()
    df['rsi'] = RSIIndicator(df['close'], window=cfg['strategy']['rsi_period']).rsi()
    return df


def risk_position_size(equity_usd, price):
    pct = cfg['risk']['max_position_size_pct']
    size_usd = equity_usd * pct
    amount = size_usd / price
    return amount


def place_order(side, amount):
    # Basic market order; in production add retries, optimistic locking, and order verification
    logger.info(f"Placing {side} order for {amount} {SYMBOL}")
    try:
        order = exchange.create_market_order(SYMBOL, side, amount)
        logger.info(f"Order placed: {order}")
        return order
    except Exception as e:
        logger.error("Order failed: %s", e)
        return None


async def run_loop():
    # very simple event loop
    while True:
        try:
            df = fetch_ohlcv(limit=cfg.get('backtest_limit', 200))
            df = compute_indicators(df)
            last = df.iloc[-1]
            prev = df.iloc[-2]

            # simple crossover strategy
            if prev['ema_short'] < prev['ema_long'] and last['ema_short'] > last['ema_long'] and last['rsi'] < 70:
                # buy signal
                price = last['close']
                equity = float(os.getenv('ACCOUNT_EQUITY_USD', '1000'))
                amount = risk_position_size(equity, price)
                place_order('buy', amount)

            if prev['ema_short'] > prev['ema_long'] and last['ema_short'] < last['ema_long'] and last['rsi'] > 30:
                # sell signal / close
                price = last['close']
                equity = float(os.getenv('ACCOUNT_EQUITY_USD', '1000'))
                amount = risk_position_size(equity, price)
                place_order('sell', amount)

        except Exception as e:
            logger.exception("Main loop exception: %s", e)
        await sleep(30)  # wait 30s between checks; adjust to timeframe


if __name__ == '__main__':
    logger.info('Starting trading bot')
    try:
        asyncio.run(run_loop())
    except KeyboardInterrupt:
        logger.info('Shutting down')
