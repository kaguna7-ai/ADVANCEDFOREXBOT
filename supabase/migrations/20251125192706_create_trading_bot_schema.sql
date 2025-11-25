/*
  # Trading Bot Platform - Database Schema
  
  1. New Tables
    - `users`
      - Extended user profile with subscription info
      - Links to auth.users
    - `mt5_accounts`
      - Stores encrypted MT5 account credentials
      - Links to users
    - `trading_sessions`
      - Active and historical trading sessions
      - Performance tracking
    - `trades`
      - Individual trade records
      - P&L tracking
    - `bot_settings`
      - User-specific bot configuration
      - Strategy parameters
    - `subscriptions`
      - Subscription plans and billing
      
  2. Security
    - Enable RLS on all tables
    - Users can only access their own data
    - Encrypted credential storage
*/

-- Users profile extension
CREATE TABLE IF NOT EXISTS users (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email text NOT NULL,
  full_name text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  subscription_tier text DEFAULT 'free' CHECK (subscription_tier IN ('free', 'basic', 'pro', 'enterprise')),
  subscription_expires_at timestamptz,
  total_profit decimal(15,2) DEFAULT 0,
  total_trades integer DEFAULT 0,
  win_rate decimal(5,2) DEFAULT 0
);

ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own profile"
  ON users FOR SELECT
  TO authenticated
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON users FOR UPDATE
  TO authenticated
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- MT5 Accounts (encrypted credentials)
CREATE TABLE IF NOT EXISTS mt5_accounts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  account_name text NOT NULL,
  broker text NOT NULL,
  account_number text NOT NULL,
  server text NOT NULL,
  encrypted_password text NOT NULL,
  is_active boolean DEFAULT true,
  balance decimal(15,2) DEFAULT 0,
  equity decimal(15,2) DEFAULT 0,
  last_sync_at timestamptz,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

ALTER TABLE mt5_accounts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own MT5 accounts"
  ON mt5_accounts FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can create own MT5 accounts"
  ON mt5_accounts FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own MT5 accounts"
  ON mt5_accounts FOR UPDATE
  TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can delete own MT5 accounts"
  ON mt5_accounts FOR DELETE
  TO authenticated
  USING (user_id = auth.uid());

-- Trading Sessions
CREATE TABLE IF NOT EXISTS trading_sessions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  mt5_account_id uuid NOT NULL REFERENCES mt5_accounts(id) ON DELETE CASCADE,
  status text NOT NULL DEFAULT 'stopped' CHECK (status IN ('running', 'stopped', 'paused', 'error')),
  started_at timestamptz DEFAULT now(),
  stopped_at timestamptz,
  total_trades integer DEFAULT 0,
  winning_trades integer DEFAULT 0,
  losing_trades integer DEFAULT 0,
  total_pnl decimal(15,2) DEFAULT 0,
  win_rate decimal(5,2) DEFAULT 0,
  max_drawdown decimal(5,2) DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

ALTER TABLE trading_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own sessions"
  ON trading_sessions FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can create own sessions"
  ON trading_sessions FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own sessions"
  ON trading_sessions FOR UPDATE
  TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

-- Trades
CREATE TABLE IF NOT EXISTS trades (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  session_id uuid NOT NULL REFERENCES trading_sessions(id) ON DELETE CASCADE,
  mt5_account_id uuid NOT NULL REFERENCES mt5_accounts(id) ON DELETE CASCADE,
  symbol text NOT NULL,
  trade_type text NOT NULL CHECK (trade_type IN ('BUY', 'SELL')),
  signal_type text NOT NULL,
  entry_price decimal(15,5) NOT NULL,
  exit_price decimal(15,5),
  position_size decimal(15,2) NOT NULL,
  stop_loss decimal(15,5) NOT NULL,
  take_profit decimal(15,5) NOT NULL,
  pnl decimal(15,2) DEFAULT 0,
  pnl_percent decimal(5,2) DEFAULT 0,
  status text NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'closed', 'cancelled')),
  opened_at timestamptz DEFAULT now(),
  closed_at timestamptz,
  duration_minutes integer,
  confidence_score decimal(3,2)
);

ALTER TABLE trades ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own trades"
  ON trades FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can create own trades"
  ON trades FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own trades"
  ON trades FOR UPDATE
  TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

-- Bot Settings
CREATE TABLE IF NOT EXISTS bot_settings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  mt5_account_id uuid REFERENCES mt5_accounts(id) ON DELETE CASCADE,
  symbol text DEFAULT 'EURUSD',
  timeframe text DEFAULT '1h',
  max_position_risk_pct decimal(3,2) DEFAULT 0.02,
  max_daily_loss_pct decimal(3,2) DEFAULT 0.05,
  max_drawdown_pct decimal(3,2) DEFAULT 0.10,
  max_trades_per_day integer DEFAULT 10,
  ema_short integer DEFAULT 9,
  ema_long integer DEFAULT 21,
  rsi_period integer DEFAULT 14,
  use_ml_prediction boolean DEFAULT true,
  min_confidence_threshold decimal(3,2) DEFAULT 0.65,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE(user_id, mt5_account_id)
);

ALTER TABLE bot_settings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own settings"
  ON bot_settings FOR SELECT
  TO authenticated
  USING (user_id = auth.uid());

CREATE POLICY "Users can create own settings"
  ON bot_settings FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own settings"
  ON bot_settings FOR UPDATE
  TO authenticated
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can delete own settings"
  ON bot_settings FOR DELETE
  TO authenticated
  USING (user_id = auth.uid());

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_mt5_accounts_user_id ON mt5_accounts(user_id);
CREATE INDEX IF NOT EXISTS idx_trading_sessions_user_id ON trading_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_trading_sessions_status ON trading_sessions(status);
CREATE INDEX IF NOT EXISTS idx_trades_user_id ON trades(user_id);
CREATE INDEX IF NOT EXISTS idx_trades_session_id ON trades(session_id);
CREATE INDEX IF NOT EXISTS idx_trades_status ON trades(status);
CREATE INDEX IF NOT EXISTS idx_bot_settings_user_id ON bot_settings(user_id);