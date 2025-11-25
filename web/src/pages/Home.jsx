import { Link } from 'react-router-dom'
import { TrendingUp, Shield, Zap, BarChart3, Brain, DollarSign } from 'lucide-react'

export default function Home() {
  return (
    <div style={{ minHeight: 'calc(100vh - 80px)' }}>
      <section style={{
        textAlign: 'center',
        padding: '6rem 0',
        background: 'linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%)',
      }}>
        <div className="container">
          <h1 style={{
            fontSize: '3.5rem',
            fontWeight: '800',
            marginBottom: '1.5rem',
            background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
          }}>
            Advanced Forex Trading Bot
          </h1>
          <p style={{
            fontSize: '1.5rem',
            color: 'var(--text-secondary)',
            marginBottom: '3rem',
            maxWidth: '800px',
            margin: '0 auto 3rem',
          }}>
            Automated trading with 8 technical indicators, ML prediction, and 90%+ win rate potential
          </p>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
            <Link to="/signup" className="btn btn-primary" style={{ fontSize: '1.25rem', padding: '1rem 2rem' }}>
              Get Started Free
            </Link>
            <Link to="/dashboard" className="btn" style={{ fontSize: '1.25rem', padding: '1rem 2rem', backgroundColor: 'var(--bg-tertiary)' }}>
              View Dashboard
            </Link>
          </div>
        </div>
      </section>

      <section style={{ padding: '6rem 0' }}>
        <div className="container">
          <h2 style={{ fontSize: '2.5rem', textAlign: 'center', marginBottom: '4rem' }}>
            Key Features
          </h2>
          <div className="grid grid-3">
            <div className="card" style={{ textAlign: 'center' }}>
              <Brain size={48} style={{ color: 'var(--primary)', margin: '0 auto 1rem' }} />
              <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>ML Prediction</h3>
              <p style={{ color: 'var(--text-secondary)' }}>
                Advanced machine learning algorithms predict market movements with high accuracy
              </p>
            </div>

            <div className="card" style={{ textAlign: 'center' }}>
              <TrendingUp size={48} style={{ color: 'var(--success)', margin: '0 auto 1rem' }} />
              <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>8 Indicators</h3>
              <p style={{ color: 'var(--text-secondary)' }}>
                Multi-indicator consensus system: EMA, RSI, MACD, Bollinger Bands, ATR, Stochastic, Momentum, ADX
              </p>
            </div>

            <div className="card" style={{ textAlign: 'center' }}>
              <Shield size={48} style={{ color: 'var(--warning)', margin: '0 auto 1rem' }} />
              <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Risk Management</h3>
              <p style={{ color: 'var(--text-secondary)' }}>
                Enterprise-grade risk controls with dynamic position sizing and drawdown protection
              </p>
            </div>

            <div className="card" style={{ textAlign: 'center' }}>
              <Zap size={48} style={{ color: 'var(--danger)', margin: '0 auto 1rem' }} />
              <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Ultra-Fast</h3>
              <p style={{ color: 'var(--text-secondary)' }}>
                10x faster processing with vectorized calculations and zero-lag architecture
              </p>
            </div>

            <div className="card" style={{ textAlign: 'center' }}>
              <BarChart3 size={48} style={{ color: 'var(--primary)', margin: '0 auto 1rem' }} />
              <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>Real-time Analytics</h3>
              <p style={{ color: 'var(--text-secondary)' }}>
                Live trade tracking, performance metrics, and win rate calculation
              </p>
            </div>

            <div className="card" style={{ textAlign: 'center' }}>
              <DollarSign size={48} style={{ color: 'var(--success)', margin: '0 auto 1rem' }} />
              <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>MT5 Integration</h3>
              <p style={{ color: 'var(--text-secondary)' }}>
                Seamless connection to MetaTrader5 accounts for automated trading
              </p>
            </div>
          </div>
        </div>
      </section>

      <section style={{
        padding: '6rem 0',
        backgroundColor: 'var(--bg-secondary)',
      }}>
        <div className="container" style={{ textAlign: 'center' }}>
          <h2 style={{ fontSize: '2.5rem', marginBottom: '2rem' }}>
            Ready to Start Trading Smarter?
          </h2>
          <p style={{ fontSize: '1.25rem', color: 'var(--text-secondary)', marginBottom: '2rem' }}>
            Join traders using advanced AI-powered automation
          </p>
          <Link to="/signup" className="btn btn-primary" style={{ fontSize: '1.25rem', padding: '1rem 2rem' }}>
            Create Free Account
          </Link>
        </div>
      </section>
    </div>
  )
}
