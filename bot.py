import os
import time
import asyncio
import logging
from loguru import logger
import pandas as pd
import numpy as np
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
import yaml
from dotenv import load_dotenv

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    logger.warning("MetaTrader5 not installed. Install with: pip install MetaTrader5")

load_dotenv()

# Load config
with open('config.yaml', 'r') as f:
    cfg = yaml.safe_load(f)

# MT5 Configuration
BROKER = os.getenv('MT5_BROKER', 'your_broker')
LOGIN = int(os.getenv('MT5_LOGIN', '0'))
PASSWORD = os.getenv('MT5_PASSWORD', '')
SERVER = os.getenv('MT5_SERVER', '')
SYMBOL = cfg.get('symbol', 'EURUSD')
TIMEFRAME = cfg.get('timeframe', '1m')
ENV_MODE = os.getenv('ENV', 'production')

# Convert timeframe string to MT5 constant
TIMEFRAME_MAP = {
    '1m': mt5.TIMEFRAME_M1,
    '5m': mt5.TIMEFRAME_M5,
    '15m': mt5.TIMEFRAME_M15,
    '30m': mt5.TIMEFRAME_M30,
    '1h': mt5.TIMEFRAME_H1,
    '4h': mt5.TIMEFRAME_H4,
    '1d': mt5.TIMEFRAME_D1,
}

mt5_timeframe = TIMEFRAME_MAP.get(TIMEFRAME, mt5.TIMEFRAME_M1)

logger.info(f"Bot Configuration:")
logger.info(f"  Broker: {BROKER}")
logger.info(f"  Login: {LOGIN}")
logger.info(f"  Symbol: {SYMBOL}")
logger.info(f"  Timeframe: {TIMEFRAME}")
logger.info(f"  Environment: {ENV_MODE}")

# Initialize MT5 connection
def init_mt5():
    """Initialize MetaTrader5 connection"""
    if not MT5_AVAILABLE:
        logger.error("MetaTrader5 module not available. Install with: pip install MetaTrader5")
        return False
    
    try:
        # Initialize MT5
        if not mt5.initialize(login=LOGIN, server=SERVER, password=PASSWORD):
            logger.error(f"MT5 initialization failed: {mt5.last_error()}")
            return False
        
        logger.info("MT5 initialized successfully")
        
        # Get account info
        account_info = mt5.account_info()
        if account_info:
            logger.info(f"Account Balance: ${account_info.balance}")
            logger.info(f"Account Equity: ${account_info.equity}")
            logger.info(f"Free Margin: ${account_info.margin_free}")
        else:
            logger.warning("Could not retrieve account info")
        
        return True
    except Exception as e:
        logger.error(f"MT5 initialization error: {e}")
        return False


def fetch_ohlcv(symbol, timeframe, limit=200):
    """Fetch OHLCV data from MT5"""
    try:
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, limit)
        if rates is None:
            logger.error(f"Failed to fetch rates: {mt5.last_error()}")
            return None
        
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df = df.rename(columns={
            'time': 'timestamp',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'tick_volume': 'volume'
        })
        
        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    except Exception as e:
        logger.error(f"Error fetching OHLCV: {e}")
        return None


def compute_indicators(df):
    """Calculate EMA and RSI indicators"""
    try:
        df = df.copy()
        df['ema_short'] = EMAIndicator(df['close'], window=cfg['strategy']['ema_short']).ema_indicator()
        df['ema_long'] = EMAIndicator(df['close'], window=cfg['strategy']['ema_long']).ema_indicator()
        df['rsi'] = RSIIndicator(df['close'], window=cfg['strategy']['rsi_period']).rsi()
        return df
    except Exception as e:
        logger.error(f"Error computing indicators: {e}")
        return None


def get_position_size(symbol, price, equity):
    """Calculate position size based on risk parameters"""
    try:
        pct = cfg['risk']['max_position_size_pct']
        size_usd = equity * pct
        
        # Get symbol info (pip size, etc.)
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            logger.error(f"Symbol {symbol} not found")
            return 0
        
        # Calculate lot size
        lot_size = size_usd / (price * symbol_info.trade_contract_size)
        
        # Get minimum and maximum lot sizes
        min_lot = symbol_info.volume_min
        max_lot = symbol_info.volume_max
        
        # Ensure lot size is within limits
        lot_size = max(min_lot, min(lot_size, max_lot))
        
        logger.info(f"Position size: {lot_size} lots (min: {min_lot}, max: {max_lot})")
        return lot_size
    except Exception as e:
        logger.error(f"Error calculating position size: {e}")
        return 0


def place_order(symbol, order_type, volume, price):
    """Place a market order on MT5"""
    try:
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "deviation": 20,
            "magic": 234000,
            "comment": "EMA Crossover Bot",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Order failed: {result.comment}")
            return None
        
        logger.info(f"Order placed: {order_type} {volume} {symbol} @ {price}")
        logger.info(f"Order #{result.order}")
        return result
    except Exception as e:
        logger.error(f"Error placing order: {e}")
        return None


def close_all_positions(symbol):
    """Close all open positions for a symbol"""
    try:
        positions = mt5.positions_get(symbol=symbol)
        
        if positions is None or len(positions) == 0:
            logger.info(f"No open positions for {symbol}")
            return True
        
        for pos in positions:
            order_type = mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
            close_price = mt5.symbol_info(symbol).bid if order_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info(symbol).ask
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": pos.volume,
                "type": order_type,
                "price": close_price,
                "deviation": 20,
                "magic": 234000,
                "comment": f"Close position #{pos.ticket}",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                logger.info(f"Closed position #{pos.ticket}")
            else:
                logger.error(f"Failed to close position: {result.comment}")
        
        return True
    except Exception as e:
        logger.error(f"Error closing positions: {e}")
        return False


async def run_loop():
    """Main trading loop"""
    while True:
        try:
            # Fetch OHLCV data
            df = fetch_ohlcv(SYMBOL, mt5_timeframe, limit=cfg.get('backtest_limit', 200))
            if df is None or len(df) < 2:
                logger.warning("Insufficient data, waiting...")
                await asyncio.sleep(30)
                continue
            
            # Compute indicators
            df = compute_indicators(df)
            if df is None:
                await asyncio.sleep(30)
                continue
            
            last = df.iloc[-1]
            prev = df.iloc[-2]
            
            # Get account info for position sizing
            account_info = mt5.account_info()
            if account_info is None:
                logger.error("Cannot get account info")
                await asyncio.sleep(30)
                continue
            
            equity = account_info.equity
            current_price = last['close']
            
            # EMA Crossover Strategy
            # BUY: Short EMA crosses above Long EMA AND RSI < 70
            if (prev['ema_short'] < prev['ema_long'] and 
                last['ema_short'] > last['ema_long'] and 
                last['rsi'] < 70):
                
                logger.info(f"BUY Signal! EMA({cfg['strategy']['ema_short']}) crossed above EMA({cfg['strategy']['ema_long']}), RSI={last['rsi']:.2f}")
                
                # Close any existing positions first
                close_all_positions(SYMBOL)
                
                # Calculate position size and place buy order
                volume = get_position_size(SYMBOL, current_price, equity)
                if volume > 0:
                    place_order(SYMBOL, mt5.ORDER_TYPE_BUY, volume, current_price)
            
            # SELL: Short EMA crosses below Long EMA AND RSI > 30
            elif (prev['ema_short'] > prev['ema_long'] and 
                  last['ema_short'] < last['ema_long'] and 
                  last['rsi'] > 30):
                
                logger.info(f"SELL Signal! EMA({cfg['strategy']['ema_short']}) crossed below EMA({cfg['strategy']['ema_long']}), RSI={last['rsi']:.2f}")
                
                # Close all positions
                close_all_positions(SYMBOL)
            
            # Log current state
            logger.info(f"{SYMBOL} | Close: {current_price:.5f} | EMA(S): {last['ema_short']:.5f} | EMA(L): {last['ema_long']:.5f} | RSI: {last['rsi']:.2f}")
        
        except Exception as e:
            logger.exception(f"Main loop error: {e}")
        
        # Wait before next iteration
        await asyncio.sleep(60)


def shutdown_mt5():
    """Shutdown MT5 connection"""
    try:
        mt5.shutdown()
        logger.info("MT5 connection closed")
    except Exception as e:
        logger.error(f"Error closing MT5: {e}")


if __name__ == '__main__':
    logger.info('Starting MT5 Trading Bot')
    
    if not init_mt5():
        logger.error("Failed to initialize MT5. Exiting.")
        exit(1)
    
    try:
        asyncio.run(run_loop())
    except KeyboardInterrupt:
        logger.info('Shutting down bot...')
        shutdown_mt5()
        logger.info('Bot stopped')
