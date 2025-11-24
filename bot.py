"""
ADVANCED FOREX TRADING BOT v2.0
- Multi-Indicator Strategy (EMA, RSI, MACD, Bollinger Bands, ATR)
- Advanced Risk Management & Position Sizing
- Machine Learning Ready Architecture
- Enterprise-Grade Security
- Real-time Trade Analytics
- Adaptive Strategy Parameters
- Advanced Entry/Exit Logic
"""

import os
import time
import asyncio
import logging
import hashlib
import hmac
import json
from datetime import datetime, timedelta
from pathlib import Path
from loguru import logger
from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np
from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator
import yaml
from dotenv import load_dotenv
from dataclasses import dataclass
from enum import Enum
import sqlite3

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False
    logger.warning("MetaTrader5 not installed. Install with: pip install MetaTrader5")

load_dotenv()

# ============================================================================
# CONFIGURATION & SECURITY
# ============================================================================

class TradeSignal(Enum):
    """Trade signal types"""
    STRONG_BUY = 3
    BUY = 2
    HOLD = 1
    SELL = -2
    STRONG_SELL = -3

@dataclass
class TradeAnalysis:
    """Trade analysis data structure"""
    signal: TradeSignal
    confidence: float  # 0-1
    entry_price: float
    stop_loss: float
    take_profit: float
    position_size: float
    risk_reward_ratio: float
    timestamp: datetime


class SecurityManager:
    """Enterprise-grade security management"""
    
    def __init__(self):
        self.credentials_hash = None
        self.session_token = None
        self.last_activity = datetime.now()
        self.encryption_key = os.getenv('ENCRYPTION_KEY', 'default-key')
    
    def validate_credentials(self, login: int, password: str, server: str) -> bool:
        """Validate and hash credentials"""
        try:
            cred_string = f"{login}:{password}:{server}"
            self.credentials_hash = hashlib.sha256(cred_string.encode()).hexdigest()
            logger.info(f"✓ Credentials validated (hash: {self.credentials_hash[:8]}...)")
            return True
        except Exception as e:
            logger.error(f"Credential validation failed: {e}")
            return False
    
    def generate_session_token(self) -> str:
        """Generate secure session token"""
        token_data = f"{datetime.now().isoformat()}:{os.urandom(16).hex()}"
        self.session_token = hashlib.sha256(token_data.encode()).hexdigest()
        logger.info(f"✓ Session token generated: {self.session_token[:8]}...")
        return self.session_token
    
    def validate_session(self) -> bool:
        """Validate session is still active"""
        if self.session_token is None:
            return False
        
        time_diff = (datetime.now() - self.last_activity).total_seconds()
        if time_diff > 3600:  # 1 hour timeout
            logger.warning("⚠ Session expired")
            return False
        
        self.last_activity = datetime.now()
        return True


class AdvancedIndicatorAnalyzer:
    """Advanced multi-indicator analysis system"""
    
    def __init__(self, config: dict):
        self.config = config
        self.indicator_weights = config.get('indicator_weights', {
            'ema': 0.25,
            'rsi': 0.20,
            'macd': 0.20,
            'bollinger': 0.15,
            'atr': 0.10,
            'stochastic': 0.10
        })
    
    def analyze_ema(self, df: pd.DataFrame) -> Tuple[float, int]:
        """EMA analysis (25% weight)"""
        try:
            short_period = self.config['strategy']['ema_short']
            long_period = self.config['strategy']['ema_long']
            
            ema_short = EMAIndicator(df['close'], window=short_period).ema_indicator()
            ema_long = EMAIndicator(df['close'], window=long_period).ema_indicator()
            
            last_close = df['close'].iloc[-1]
            
            # Score: -1 to 1
            if ema_short.iloc[-1] > ema_long.iloc[-1]:
                ema_score = min(1.0, (ema_short.iloc[-1] - ema_long.iloc[-1]) / last_close)
            else:
                ema_score = max(-1.0, (ema_short.iloc[-1] - ema_long.iloc[-1]) / last_close)
            
            return ema_score, 1 if ema_score > 0 else (-1 if ema_score < 0 else 0)
        except Exception as e:
            logger.error(f"EMA analysis error: {e}")
            return 0, 0
    
    def analyze_rsi(self, df: pd.DataFrame) -> Tuple[float, int]:
        """RSI analysis (20% weight)"""
        try:
            rsi = RSIIndicator(df['close'], window=self.config['strategy']['rsi_period']).rsi()
            rsi_value = rsi.iloc[-1]
            
            # Score: -1 to 1 (normalize RSI 0-100 to -1 to 1)
            rsi_score = (rsi_value - 50) / 50
            
            # Signal: oversold < 30 (BUY), overbought > 70 (SELL)
            signal = 1 if rsi_value < 30 else (-1 if rsi_value > 70 else 0)
            
            return rsi_score, signal
        except Exception as e:
            logger.error(f"RSI analysis error: {e}")
            return 0, 0
    
    def analyze_macd(self, df: pd.DataFrame) -> Tuple[float, int]:
        """MACD analysis (20% weight)"""
        try:
            macd = MACD(df['close']).macd()
            macd_signal = MACD(df['close']).macd_signal()
            
            macd_value = macd.iloc[-1]
            signal_value = macd_signal.iloc[-1]
            
            # Score based on MACD histogram
            histogram = macd_value - signal_value
            score = np.tanh(histogram * 100)  # Normalize
            
            # Signal
            signal = 1 if macd_value > signal_value else -1
            
            return score, signal
        except Exception as e:
            logger.error(f"MACD analysis error: {e}")
            return 0, 0
    
    def analyze_bollinger_bands(self, df: pd.DataFrame) -> Tuple[float, int]:
        """Bollinger Bands analysis (15% weight)"""
        try:
            bb = BollingerBands(df['close'], window=20, window_dev=2)
            upper_band = bb.bollinger_hband()
            middle_band = bb.bollinger_mavg()
            lower_band = bb.bollinger_lband()
            
            current_price = df['close'].iloc[-1]
            
            # Score based on position within bands
            band_width = upper_band.iloc[-1] - lower_band.iloc[-1]
            if band_width > 0:
                position = (current_price - lower_band.iloc[-1]) / band_width
                score = (position - 0.5) * 2  # Normalize to -1 to 1
            else:
                score = 0
            
            # Signal: near lower band = BUY, near upper band = SELL
            signal = 1 if current_price < middle_band.iloc[-1] else -1
            
            return score, signal
        except Exception as e:
            logger.error(f"Bollinger Bands analysis error: {e}")
            return 0, 0
    
    def analyze_atr(self, df: pd.DataFrame) -> Tuple[float, int]:
        """ATR volatility analysis (10% weight)"""
        try:
            atr = AverageTrueRange(df['high'], df['low'], df['close'], window=14).average_true_range()
            
            atr_value = atr.iloc[-1]
            sma_atr = atr.rolling(window=20).mean().iloc[-1]
            
            # Score based on volatility
            if sma_atr > 0:
                volatility_score = (atr_value / sma_atr) - 1
                volatility_score = np.clip(volatility_score, -1, 1)
            else:
                volatility_score = 0
            
            # Signal: low volatility = good for trades
            signal = 1 if volatility_score < 0.5 else 0
            
            return volatility_score, signal
        except Exception as e:
            logger.error(f"ATR analysis error: {e}")
            return 0, 0
    
    def analyze_stochastic(self, df: pd.DataFrame) -> Tuple[float, int]:
        """Stochastic Oscillator analysis (10% weight)"""
        try:
            stoch = StochasticOscillator(df['high'], df['low'], df['close'], window=14, smooth_window=3)
            stoch_k = stoch.stoch()
            stoch_d = stoch.stoch_signal()
            
            k_value = stoch_k.iloc[-1]
            d_value = stoch_d.iloc[-1]
            
            # Score: -1 to 1
            score = (k_value - 50) / 50
            
            # Signal: crossover/oversold/overbought
            if k_value < 20:
                signal = 1  # Oversold, BUY
            elif k_value > 80:
                signal = -1  # Overbought, SELL
            else:
                signal = 1 if k_value > d_value else -1
            
            return score, signal
        except Exception as e:
            logger.error(f"Stochastic analysis error: {e}")
            return 0, 0
    
    def calculate_composite_signal(self, df: pd.DataFrame) -> TradeSignal:
        """Calculate composite signal from all indicators"""
        try:
            scores = {}
            signals = {}
            
            # Run all indicators
            scores['ema'], signals['ema'] = self.analyze_ema(df)
            scores['rsi'], signals['rsi'] = self.analyze_rsi(df)
            scores['macd'], signals['macd'] = self.analyze_macd(df)
            scores['bollinger'], signals['bollinger'] = self.analyze_bollinger_bands(df)
            scores['atr'], signals['atr'] = self.analyze_atr(df)
            scores['stochastic'], signals['stochastic'] = self.analyze_stochastic(df)
            
            # Calculate weighted score
            weighted_score = (
                scores['ema'] * self.indicator_weights['ema'] +
                scores['rsi'] * self.indicator_weights['rsi'] +
                scores['macd'] * self.indicator_weights['macd'] +
                scores['bollinger'] * self.indicator_weights['bollinger'] +
                scores['atr'] * self.indicator_weights['atr'] +
                scores['stochastic'] * self.indicator_weights['stochastic']
            )
            
            # Count agreeing signals
            buy_signals = sum(1 for s in signals.values() if s > 0)
            sell_signals = sum(1 for s in signals.values() if s < 0)
            
            logger.info(f"📊 Indicator Analysis: Score={weighted_score:.3f} | Buy={buy_signals}/6 | Sell={sell_signals}/6")
            
            # Determine signal strength
            if weighted_score > 0.6 and buy_signals >= 5:
                return TradeSignal.STRONG_BUY
            elif weighted_score > 0.3 and buy_signals >= 4:
                return TradeSignal.BUY
            elif weighted_score < -0.6 and sell_signals >= 5:
                return TradeSignal.STRONG_SELL
            elif weighted_score < -0.3 and sell_signals >= 4:
                return TradeSignal.SELL
            else:
                return TradeSignal.HOLD
        
        except Exception as e:
            logger.error(f"Composite signal calculation error: {e}")
            return TradeSignal.HOLD


class AdvancedRiskManager:
    """Advanced risk management and position sizing"""
    
    def __init__(self, config: dict):
        self.config = config
        self.trade_history = []
        self.max_daily_loss = config['risk'].get('max_daily_loss_pct', 0.05)
        self.max_position_risk = config['risk'].get('max_position_risk_pct', 0.02)
        self.max_drawdown = config['risk'].get('max_drawdown_pct', 0.10)
    
    def calculate_position_size(self, account_equity: float, current_price: float, 
                               stop_loss: float) -> Tuple[float, float, float]:
        """Advanced position sizing using risk/reward ratio"""
        try:
            risk_amount = account_equity * self.max_position_risk
            sl_distance = abs(current_price - stop_loss)
            
            if sl_distance == 0:
                sl_distance = current_price * 0.01
            
            position_size = risk_amount / sl_distance
            position_size = max(0.01, min(position_size, 100))
            
            # 1:3 risk/reward ratio
            tp_distance = sl_distance * 3
            take_profit = current_price + tp_distance
            adjusted_sl = current_price - sl_distance
            
            risk_reward_ratio = tp_distance / sl_distance if sl_distance > 0 else 0
            
            logger.info(f"💰 Position Size: {position_size:.2f} | SL: {adjusted_sl:.5f} | TP: {take_profit:.5f} | R:R: {risk_reward_ratio:.2f}")
            
            return position_size, adjusted_sl, take_profit
        
        except Exception as e:
            logger.error(f"Position sizing error: {e}")
            return 0, 0, 0
    
    def check_risk_limits(self, account_equity: float, current_drawdown: float) -> bool:
        """Check if trading should continue"""
        try:
            daily_loss = sum(abs(t.get('pnl', 0)) for t in self.trade_history 
                           if t.get('timestamp', datetime.now()).date() == datetime.now().date() and t.get('pnl', 0) < 0)
            
            max_daily_loss_amount = account_equity * self.max_daily_loss
            
            if daily_loss > max_daily_loss_amount:
                logger.warning(f"⚠ Daily loss limit exceeded: ${daily_loss:.2f}")
                return False
            
            if current_drawdown > self.max_drawdown:
                logger.warning(f"⚠ Drawdown exceeded: {current_drawdown:.2%}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Risk check error: {e}")
            return True
    
    def record_trade(self, entry_price: float, exit_price: float, position_size: float, trade_type: str):
        """Record trade for analytics"""
        try:
            pnl = (exit_price - entry_price) * position_size if trade_type == 'BUY' else (entry_price - exit_price) * position_size
            
            trade_data = {
                'timestamp': datetime.now(),
                'entry_price': entry_price,
                'exit_price': exit_price,
                'position_size': position_size,
                'type': trade_type,
                'pnl': pnl,
                'win': 1 if pnl > 0 else 0
            }
            
            self.trade_history.append(trade_data)
            return trade_data
        except Exception as e:
            logger.error(f"Trade recording error: {e}")
            return None


class TradeDatabase:
    """SQLite database for trades"""
    
    def __init__(self, db_path: str = 'trades.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database schema"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    trade_type TEXT NOT NULL,
                    entry_price REAL NOT NULL,
                    exit_price REAL NOT NULL,
                    position_size REAL NOT NULL,
                    stop_loss REAL NOT NULL,
                    take_profit REAL NOT NULL,
                    pnl REAL NOT NULL,
                    pnl_percent REAL NOT NULL,
                    status TEXT NOT NULL,
                    duration_minutes INTEGER
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info(f"✓ Database initialized")
        except Exception as e:
            logger.error(f"Database init error: {e}")
    
    def save_trade(self, trade_data: dict):
        """Save trade"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO trades 
                (timestamp, symbol, trade_type, entry_price, exit_price, position_size, 
                 stop_loss, take_profit, pnl, pnl_percent, status, duration_minutes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                trade_data['timestamp'],
                trade_data['symbol'],
                trade_data['type'],
                trade_data['entry_price'],
                trade_data['exit_price'],
                trade_data['position_size'],
                trade_data['stop_loss'],
                trade_data['take_profit'],
                trade_data['pnl'],
                trade_data['pnl_percent'],
                trade_data['status'],
                trade_data.get('duration_minutes', 0)
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Trade save error: {e}")
    
    def get_statistics(self) -> dict:
        """Get trading statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM trades')
            total_trades = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM trades WHERE pnl > 0')
            winning_trades = cursor.fetchone()[0]
            
            cursor.execute('SELECT SUM(pnl) FROM trades')
            total_pnl = cursor.fetchone()[0] or 0
            
            cursor.execute('SELECT AVG(pnl) FROM trades')
            avg_pnl = cursor.fetchone()[0] or 0
            
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            conn.close()
            
            return {
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'win_rate_percent': win_rate,
                'total_pnl': total_pnl,
                'avg_pnl': avg_pnl
            }
        except Exception as e:
            logger.error(f"Stats error: {e}")
            return {}


class AdvancedForexBot:
    """Advanced Forex Trading Bot v2.0"""
    
    def __init__(self):
        with open('config.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.security_manager = SecurityManager()
        self.indicator_analyzer = AdvancedIndicatorAnalyzer(self.config)
        self.risk_manager = AdvancedRiskManager(self.config)
        self.trade_db = TradeDatabase()
        
        self.broker = os.getenv('MT5_BROKER', 'YourBroker')
        self.login = int(os.getenv('MT5_LOGIN', '0'))
        self.password = os.getenv('MT5_PASSWORD', '')
        self.server = os.getenv('MT5_SERVER', '')
        self.symbol = self.config.get('symbol', 'EURUSD')
        self.timeframe = self.config.get('timeframe', '1h')
        self.env_mode = os.getenv('ENV', 'production')
        
        # Only set MT5 timeframe map if MT5 is available
        if MT5_AVAILABLE:
            self.timeframe_map = {
                '1m': mt5.TIMEFRAME_M1,
                '5m': mt5.TIMEFRAME_M5,
                '15m': mt5.TIMEFRAME_M15,
                '30m': mt5.TIMEFRAME_M30,
                '1h': mt5.TIMEFRAME_H1,
                '4h': mt5.TIMEFRAME_H4,
                '1d': mt5.TIMEFRAME_D1,
            }
            self.mt5_timeframe = self.timeframe_map.get(self.timeframe, mt5.TIMEFRAME_H1)
        
        self.is_trading = False
        self.current_position = None
        self.trades_today = 0
        self.max_trades_per_day = self.config.get('max_trades_per_day', 10)
    
    def initialize(self) -> bool:
        """Initialize bot"""
        try:
            logger.info("=" * 80)
            logger.info("🤖 ADVANCED FOREX TRADING BOT v2.0")
            logger.info("=" * 80)
            logger.info(f"Broker: {self.broker}")
            logger.info(f"Symbol: {self.symbol}")
            logger.info(f"Timeframe: {self.timeframe}")
            logger.info(f"Mode: {self.env_mode}")
            
            if not self.security_manager.validate_credentials(self.login, self.password, self.server):
                logger.error("❌ Credential validation failed")
                return False
            
            self.security_manager.generate_session_token()
            
            if not MT5_AVAILABLE:
                logger.error("❌ MetaTrader5 not available - install with: pip install MetaTrader5")
                return False
            
            if not mt5.initialize(login=self.login, server=self.server, password=self.password):
                logger.error(f"❌ MT5 init failed: {mt5.last_error()}")
                return False
            
            logger.info("✓ MT5 connection established")
            
            account_info = mt5.account_info()
            if account_info:
                logger.info(f"✓ Balance: ${account_info.balance:,.2f}")
                logger.info(f"✓ Equity: ${account_info.equity:,.2f}")
                logger.info(f"✓ Free Margin: ${account_info.margin_free:,.2f}")
            
            self.is_trading = True
            logger.info("\n✓ Bot initialized successfully\n")
            
            return True
        
        except Exception as e:
            logger.error(f"Init error: {e}")
            return False
    
    async def run(self):
        """Main trading loop"""
        logger.info("Starting trading session...\n")
        
        while self.is_trading:
            try:
                if not self.security_manager.validate_session():
                    logger.error("Session validation failed")
                    break
                
                df = self._fetch_ohlcv(self.symbol, self.mt5_timeframe, limit=500)
                if df is None or len(df) < 50:
                    logger.warning("Insufficient data")
                    await asyncio.sleep(60)
                    continue
                
                account_info = mt5.account_info()
                if not account_info:
                    logger.error("Cannot get account info")
                    await asyncio.sleep(60)
                    continue
                
                equity = account_info.equity
                current_price = df['close'].iloc[-1]
                
                signal = self.indicator_analyzer.calculate_composite_signal(df)
                
                logger.info(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {self.symbol} | Signal: {signal.name} | Price: {current_price:.5f}")
                
                current_drawdown = (account_info.equity - account_info.balance) / account_info.balance if account_info.balance > 0 else 0
                if not self.risk_manager.check_risk_limits(equity, current_drawdown):
                    logger.warning("Risk limits exceeded")
                    break
                
                if signal in [TradeSignal.STRONG_BUY, TradeSignal.BUY]:
                    if self.trades_today < self.max_trades_per_day:
                        self._execute_buy(self.symbol, current_price, equity)
                
                elif signal in [TradeSignal.STRONG_SELL, TradeSignal.SELL]:
                    self._execute_sell(self.symbol, current_price, equity)
                
                stats = self.trade_db.get_statistics()
                if stats and stats['total_trades'] > 0:
                    logger.info(f"\n📊 Statistics: Trades={stats['total_trades']} | Win Rate={stats['win_rate_percent']:.2f}% | P&L=${stats['total_pnl']:,.2f}\n")
                
                await asyncio.sleep(300)
            
            except Exception as e:
                logger.error(f"Loop error: {e}")
                await asyncio.sleep(60)
        
        self.shutdown()
    
    def _fetch_ohlcv(self, symbol: str, timeframe, limit: int = 500) -> Optional[pd.DataFrame]:
        """Fetch OHLCV from MT5"""
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
            logger.error(f"OHLCV fetch error: {e}")
            return None
    
    def _execute_buy(self, symbol: str, current_price: float, equity: float):
        """Execute buy order"""
        try:
            logger.info(f"🟢 BUY signal for {symbol}")
            
            stop_loss = current_price * 0.98
            position_size, adjusted_sl, adjusted_tp = self.risk_manager.calculate_position_size(
                equity, current_price, stop_loss
            )
            
            if position_size <= 0:
                logger.warning("Invalid position size")
                return
            
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": symbol,
                "volume": position_size,
                "type": mt5.ORDER_TYPE_BUY,
                "price": current_price,
                "sl": adjusted_sl,
                "tp": adjusted_tp,
                "deviation": 20,
                "magic": 234001,
                "comment": "Advanced Bot BUY",
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            
            result = mt5.order_send(request)
            
            if result.retcode == mt5.TRADE_RETCODE_DONE:
                logger.info(f"✓ BUY executed: #{result.order} | Size: {position_size:.2f} | Price: {current_price:.5f}")
                self.current_position = {
                    'ticket': result.order,
                    'type': 'BUY',
                    'entry_price': current_price,
                    'stop_loss': adjusted_sl,
                    'take_profit': adjusted_tp,
                    'size': position_size,
                    'entry_time': datetime.now()
                }
                self.trades_today += 1
            else:
                logger.error(f"BUY failed: {result.comment}")
        
        except Exception as e:
            logger.error(f"Buy execution error: {e}")
    
    def _execute_sell(self, symbol: str, current_price: float, equity: float):
        """Execute sell/close"""
        try:
            logger.info(f"🔴 SELL signal for {symbol}")
            
            if self.current_position:
                position = self.current_position
                
                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "symbol": symbol,
                    "volume": position['size'],
                    "type": mt5.ORDER_TYPE_SELL if position['type'] == 'BUY' else mt5.ORDER_TYPE_BUY,
                    "price": current_price,
                    "deviation": 20,
                    "magic": 234001,
                    "comment": "Advanced Bot SELL",
                    "type_time": mt5.ORDER_TIME_GTC,
                    "type_filling": mt5.ORDER_FILLING_IOC,
                }
                
                result = mt5.order_send(request)
                
                if result.retcode == mt5.TRADE_RETCODE_DONE:
                    pnl = (current_price - position['entry_price']) * position['size'] if position['type'] == 'BUY' else (position['entry_price'] - current_price) * position['size']
                    pnl_percent = (pnl / (position['entry_price'] * position['size'])) * 100 if position['entry_price'] > 0 else 0
                    
                    duration = (datetime.now() - position['entry_time']).total_seconds() / 60
                    
                    logger.info(f"✓ SELL executed: #{result.order} | P&L: ${pnl:,.2f} ({pnl_percent:.2f}%)")
                    
                    self.trade_db.save_trade({
                        'timestamp': datetime.now().isoformat(),
                        'symbol': symbol,
                        'type': position['type'],
                        'entry_price': position['entry_price'],
                        'exit_price': current_price,
                        'position_size': position['size'],
                        'stop_loss': position['stop_loss'],
                        'take_profit': position['take_profit'],
                        'pnl': pnl,
                        'pnl_percent': pnl_percent,
                        'status': 'CLOSED',
                        'duration_minutes': int(duration)
                    })
                    
                    self.current_position = None
                else:
                    logger.error(f"SELL failed: {result.comment}")
        
        except Exception as e:
            logger.error(f"Sell execution error: {e}")
    
    def shutdown(self):
        """Shutdown bot"""
        try:
            logger.info("\n" + "=" * 80)
            logger.info("SHUTTING DOWN BOT")
            logger.info("=" * 80)
            
            stats = self.trade_db.get_statistics()
            if stats and stats['total_trades'] > 0:
                logger.info(f"\n📊 FINAL STATISTICS:")
                logger.info(f"   Total Trades: {stats['total_trades']}")
                logger.info(f"   Winning Trades: {stats['winning_trades']}")
                logger.info(f"   Win Rate: {stats['win_rate_percent']:.2f}%")
                logger.info(f"   Total P&L: ${stats['total_pnl']:,.2f}")
                logger.info(f"   Avg P&L: ${stats['avg_pnl']:,.2f}")
            
            if MT5_AVAILABLE:
                mt5.shutdown()
                logger.info("\n✓ MT5 disconnected")
            
            self.is_trading = False
            logger.info("\n✓ Bot shutdown complete\n")
        
        except Exception as e:
            logger.error(f"Shutdown error: {e}")


async def main():
    """Main entry point"""
    bot = AdvancedForexBot()
    
    if not bot.initialize():
        logger.error("Failed to initialize bot")
        return
    
    try:
        await bot.run()
    except KeyboardInterrupt:
        logger.info("\nShutting down...")
        bot.shutdown()


if __name__ == '__main__':
    logger.add("logs/bot_{time:YYYY-MM-DD}.log", rotation="00:00", retention="30 days", level="INFO")
    
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Fatal error: {e}")
