import { useState, useEffect } from 'react'
import { supabase } from '../lib/supabase'
import { useNavigate } from 'react-router-dom'
import { Settings as SettingsIcon, Plus, Trash2, Save } from 'lucide-react'

export default function Settings() {
  const [loading, setLoading] = useState(true)
  const [accounts, setAccounts] = useState([])
  const [showAddForm, setShowAddForm] = useState(false)
  const [formData, setFormData] = useState({
    accountName: '',
    broker: '',
    accountNumber: '',
    server: '',
    password: '',
  })
  const [botSettings, setBotSettings] = useState({
    symbol: 'EURUSD',
    timeframe: '1h',
    maxPositionRisk: 2,
    maxDailyLoss: 5,
    maxDrawdown: 10,
    maxTradesPerDay: 10,
    emaShort: 9,
    emaLong: 21,
    rsiPeriod: 14,
    useMl: true,
    minConfidence: 65,
  })
  const [saving, setSaving] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    checkUser()
    loadSettings()
  }, [])

  const checkUser = async () => {
    const { data: { user } } = await supabase.auth.getUser()
    if (!user) {
      navigate('/login')
    }
  }

  const loadSettings = async () => {
    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) return

      const { data: mt5Accounts } = await supabase
        .from('mt5_accounts')
        .select('*')
        .eq('user_id', user.id)

      setAccounts(mt5Accounts || [])

      const { data: settings } = await supabase
        .from('bot_settings')
        .select('*')
        .eq('user_id', user.id)
        .maybeSingle()

      if (settings) {
        setBotSettings({
          symbol: settings.symbol,
          timeframe: settings.timeframe,
          maxPositionRisk: settings.max_position_risk_pct * 100,
          maxDailyLoss: settings.max_daily_loss_pct * 100,
          maxDrawdown: settings.max_drawdown_pct * 100,
          maxTradesPerDay: settings.max_trades_per_day,
          emaShort: settings.ema_short,
          emaLong: settings.ema_long,
          rsiPeriod: settings.rsi_period,
          useMl: settings.use_ml_prediction,
          minConfidence: settings.min_confidence_threshold * 100,
        })
      }
    } catch (error) {
      console.error('Error loading settings:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddAccount = async (e) => {
    e.preventDefault()
    setSaving(true)

    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) return

      const { error } = await supabase.from('mt5_accounts').insert([
        {
          user_id: user.id,
          account_name: formData.accountName,
          broker: formData.broker,
          account_number: formData.accountNumber,
          server: formData.server,
          encrypted_password: btoa(formData.password),
        },
      ])

      if (error) throw error

      setShowAddForm(false)
      setFormData({
        accountName: '',
        broker: '',
        accountNumber: '',
        server: '',
        password: '',
      })
      loadSettings()
    } catch (error) {
      console.error('Error adding account:', error)
      alert('Failed to add account: ' + error.message)
    } finally {
      setSaving(false)
    }
  }

  const handleDeleteAccount = async (accountId) => {
    if (!confirm('Are you sure you want to delete this account?')) return

    try {
      const { error } = await supabase
        .from('mt5_accounts')
        .delete()
        .eq('id', accountId)

      if (error) throw error
      loadSettings()
    } catch (error) {
      console.error('Error deleting account:', error)
      alert('Failed to delete account')
    }
  }

  const handleSaveBotSettings = async () => {
    setSaving(true)

    try {
      const { data: { user } } = await supabase.auth.getUser()
      if (!user) return

      const { error } = await supabase.from('bot_settings').upsert([
        {
          user_id: user.id,
          symbol: botSettings.symbol,
          timeframe: botSettings.timeframe,
          max_position_risk_pct: botSettings.maxPositionRisk / 100,
          max_daily_loss_pct: botSettings.maxDailyLoss / 100,
          max_drawdown_pct: botSettings.maxDrawdown / 100,
          max_trades_per_day: botSettings.maxTradesPerDay,
          ema_short: botSettings.emaShort,
          ema_long: botSettings.emaLong,
          rsi_period: botSettings.rsiPeriod,
          use_ml_prediction: botSettings.useMl,
          min_confidence_threshold: botSettings.minConfidence / 100,
        },
      ])

      if (error) throw error
      alert('Settings saved successfully')
    } catch (error) {
      console.error('Error saving settings:', error)
      alert('Failed to save settings')
    } finally {
      setSaving(false)
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
        <h1 style={{ fontSize: '2.5rem', marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <SettingsIcon size={40} />
          Settings
        </h1>

        <div className="grid grid-2" style={{ marginBottom: '3rem' }}>
          <div className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
              <h3 style={{ fontSize: '1.5rem' }}>MT5 Accounts</h3>
              <button
                onClick={() => setShowAddForm(!showAddForm)}
                className="btn btn-primary"
              >
                <Plus size={18} />
                Add Account
              </button>
            </div>

            {showAddForm && (
              <form onSubmit={handleAddAccount} style={{ marginBottom: '2rem', padding: '1.5rem', backgroundColor: 'var(--bg-tertiary)', borderRadius: '0.5rem' }}>
                <div style={{ marginBottom: '1rem' }}>
                  <label className="label">Account Name</label>
                  <input
                    type="text"
                    className="input"
                    value={formData.accountName}
                    onChange={(e) => setFormData({ ...formData, accountName: e.target.value })}
                    required
                    placeholder="My Trading Account"
                  />
                </div>

                <div style={{ marginBottom: '1rem' }}>
                  <label className="label">Broker</label>
                  <input
                    type="text"
                    className="input"
                    value={formData.broker}
                    onChange={(e) => setFormData({ ...formData, broker: e.target.value })}
                    required
                    placeholder="Pepperstone"
                  />
                </div>

                <div style={{ marginBottom: '1rem' }}>
                  <label className="label">Account Number</label>
                  <input
                    type="text"
                    className="input"
                    value={formData.accountNumber}
                    onChange={(e) => setFormData({ ...formData, accountNumber: e.target.value })}
                    required
                    placeholder="12345678"
                  />
                </div>

                <div style={{ marginBottom: '1rem' }}>
                  <label className="label">Server</label>
                  <input
                    type="text"
                    className="input"
                    value={formData.server}
                    onChange={(e) => setFormData({ ...formData, server: e.target.value })}
                    required
                    placeholder="Pepperstone-Live"
                  />
                </div>

                <div style={{ marginBottom: '1rem' }}>
                  <label className="label">Password</label>
                  <input
                    type="password"
                    className="input"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required
                    placeholder="Enter MT5 password"
                  />
                </div>

                <div style={{ display: 'flex', gap: '1rem' }}>
                  <button type="submit" className="btn btn-primary" disabled={saving}>
                    {saving ? 'Adding...' : 'Add Account'}
                  </button>
                  <button
                    type="button"
                    className="btn"
                    style={{ backgroundColor: 'var(--bg-secondary)' }}
                    onClick={() => setShowAddForm(false)}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            )}

            {accounts.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                No accounts connected yet
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
                    <button
                      onClick={() => handleDeleteAccount(account.id)}
                      className="btn btn-danger"
                      style={{ padding: '0.5rem 1rem' }}
                    >
                      <Trash2 size={18} />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="card">
            <h3 style={{ fontSize: '1.5rem', marginBottom: '1.5rem' }}>Bot Configuration</h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <label className="label">Symbol</label>
                <select
                  className="input"
                  value={botSettings.symbol}
                  onChange={(e) => setBotSettings({ ...botSettings, symbol: e.target.value })}
                >
                  <option value="EURUSD">EURUSD</option>
                  <option value="GBPUSD">GBPUSD</option>
                  <option value="USDJPY">USDJPY</option>
                  <option value="AUDUSD">AUDUSD</option>
                  <option value="USDCAD">USDCAD</option>
                </select>
              </div>

              <div>
                <label className="label">Timeframe</label>
                <select
                  className="input"
                  value={botSettings.timeframe}
                  onChange={(e) => setBotSettings({ ...botSettings, timeframe: e.target.value })}
                >
                  <option value="1m">1 Minute</option>
                  <option value="5m">5 Minutes</option>
                  <option value="15m">15 Minutes</option>
                  <option value="30m">30 Minutes</option>
                  <option value="1h">1 Hour</option>
                  <option value="4h">4 Hours</option>
                  <option value="1d">1 Day</option>
                </select>
              </div>

              <div>
                <label className="label">Max Position Risk (%)</label>
                <input
                  type="number"
                  className="input"
                  value={botSettings.maxPositionRisk}
                  onChange={(e) => setBotSettings({ ...botSettings, maxPositionRisk: parseFloat(e.target.value) })}
                  min="0.1"
                  max="10"
                  step="0.1"
                />
              </div>

              <div>
                <label className="label">Max Daily Loss (%)</label>
                <input
                  type="number"
                  className="input"
                  value={botSettings.maxDailyLoss}
                  onChange={(e) => setBotSettings({ ...botSettings, maxDailyLoss: parseFloat(e.target.value) })}
                  min="1"
                  max="20"
                  step="0.5"
                />
              </div>

              <div>
                <label className="label">Max Drawdown (%)</label>
                <input
                  type="number"
                  className="input"
                  value={botSettings.maxDrawdown}
                  onChange={(e) => setBotSettings({ ...botSettings, maxDrawdown: parseFloat(e.target.value) })}
                  min="5"
                  max="30"
                  step="1"
                />
              </div>

              <div>
                <label className="label">Max Trades Per Day</label>
                <input
                  type="number"
                  className="input"
                  value={botSettings.maxTradesPerDay}
                  onChange={(e) => setBotSettings({ ...botSettings, maxTradesPerDay: parseInt(e.target.value) })}
                  min="1"
                  max="50"
                />
              </div>

              <div>
                <label className="label">
                  <input
                    type="checkbox"
                    checked={botSettings.useMl}
                    onChange={(e) => setBotSettings({ ...botSettings, useMl: e.target.checked })}
                    style={{ marginRight: '0.5rem' }}
                  />
                  Use ML Prediction
                </label>
              </div>

              <button
                onClick={handleSaveBotSettings}
                className="btn btn-success"
                disabled={saving}
                style={{ width: '100%', marginTop: '1rem' }}
              >
                <Save size={18} />
                {saving ? 'Saving...' : 'Save Settings'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
