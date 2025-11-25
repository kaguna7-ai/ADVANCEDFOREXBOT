import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { useNavigate } from 'react-router-dom'
import { TrendingUp, TrendingDown, Activity, DollarSign, Target, Award } from 'lucide-react'

export default function Dashboard() {
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState(null)
  const [accounts, setAccounts] = useState([])
  const [recentTrades, setRecentTrades] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    checkUser()
    loadDashboardData()
  }, [])

  const checkUser = async () => {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) {
      navigate('/login')
    }
  }

  const loadDashboardData = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) return

      const [userProfile, mt5Accounts, trades] = await Promise.all([
        supabase.from('users').select('*').eq('id', user.id).maybeSingle(),
        supabase.from('mt5_accounts').select('*').eq('user_id', user.id),
        supabase.from('trades').select('*').eq('user_id', user.id).order('opened_at', { ascending: false }).limit(10)
      ])

      setStats(userProfile.data)
      setAccounts(mt5Accounts.data || [])
      setRecentTrades(trades.data || [])
    } catch (error) {
      console.error('Error loading dashboard:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    )
  }

  return (
    <div style={{ padding: '3rem 0', minHeight: 'calc(100vh - 80px)' }}>
      <div className="container">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <h1 style={{ fontSize: '2.5rem' }}>Trading Dashboard</h1>
          <button
            onClick={() => navigate('/settings')}
            className="btn btn-primary"
          >
            Connect MT5 Account
          </button>
        </div>

        <div className="grid grid-3" style={{ marginBottom: '3rem' }}>
          <div className="stat-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <DollarSign size={32} style={{ color: 'var(--success)' }} />
              <div>
                <div className="stat-label">Total Profit</div>
                <div className="stat-value" style={{ color: stats?.total_profit >= 0 ? 'var(--success)' : 'var(--danger)' }}>
                  ${stats?.total_profit?.toFixed(2) || '0.00'}
                </div>
              </div>
            </div>
          </div>

          <div className="stat-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <Activity size={32} style={{ color: 'var(--primary)' }} />
              <div>
                <div className="stat-label">Total Trades</div>
                <div className="stat-value">{stats?.total_trades || 0}</div>
              </div>
            </div>
          </div>

          <div className="stat-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <Award size={32} style={{ color: 'var(--warning)' }} />
              <div>
                <div className="stat-label">Win Rate</div>
                <div className="stat-value">{stats?.win_rate?.toFixed(1) || '0.0'}%</div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-2" style={{ marginBottom: '3rem' }}>
          <div className="card">
            <h3 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>MT5 Accounts</h3>
            {accounts.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                <p>No MT5 accounts connected yet</p>
                <button
                  onClick={() => navigate('/settings')}
                  className="btn btn-primary"
                  style={{ marginTop: '1rem' }}
                >
                  Add Account
                </button>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {accounts.map((account) => (
                  <div
                    key={account.id}
                    style={{
                      padding: '1rem',
                      backgroundColor: 'var(--bg-tertiary)',
                      borderRadius: '0.5rem',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: '600', marginBottom: '0.25rem' }}>
                        {account.account_name}
                      </div>
                      <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                        {account.broker} - {account.account_number}
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontWeight: '600' }}>${account.balance?.toFixed(2)}</div>
                      <span className={`badge ${account.is_active ? 'badge-success' : 'badge-danger'}`}>
                        {account.is_active ? 'Active' : 'Inactive'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="card">
            <h3 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Recent Trades</h3>
            {recentTrades.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                No trades yet. Start a trading session to see results here.
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {recentTrades.slice(0, 5).map((trade) => (
                  <div
                    key={trade.id}
                    style={{
                      padding: '0.75rem',
                      backgroundColor: 'var(--bg-tertiary)',
                      borderRadius: '0.5rem',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                      {trade.pnl >= 0 ? (
                        <TrendingUp size={20} style={{ color: 'var(--success)' }} />
                      ) : (
                        <TrendingDown size={20} style={{ color: 'var(--danger)' }} />
                      )}
                      <div>
                        <div style={{ fontWeight: '600' }}>{trade.symbol}</div>
                        <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                          {trade.trade_type}
                        </div>
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{
                        fontWeight: '600',
                        color: trade.pnl >= 0 ? 'var(--success)' : 'var(--danger)'
                      }}>
                        ${trade.pnl?.toFixed(2)}
                      </div>
                      <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                        {trade.pnl_percent?.toFixed(2)}%
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
