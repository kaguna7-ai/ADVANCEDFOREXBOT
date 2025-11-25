import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { supabase, signOut } from '../lib/supabase'
import { Activity, LogOut, Settings, User } from 'lucide-react'

export default function Navbar() {
  const [user, setUser] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null)
    })

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => subscription.unsubscribe()
  }, [])

  const handleSignOut = async () => {
    await signOut()
    navigate('/')
  }

  return (
    <nav style={{
      backgroundColor: 'var(--bg-secondary)',
      borderBottom: '1px solid var(--border)',
      padding: '1rem 0',
    }}>
      <div className="container" style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <Link to="/" style={{
          textDecoration: 'none',
          color: 'var(--text-primary)',
          display: 'flex',
          alignItems: 'center',
          gap: '0.5rem',
          fontSize: '1.5rem',
          fontWeight: '700',
        }}>
          <Activity size={32} />
          Advanced Forex Bot
        </Link>

        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          {user ? (
            <>
              <Link to="/dashboard" style={{ textDecoration: 'none', color: 'var(--text-secondary)' }}>
                Dashboard
              </Link>
              <Link to="/settings" style={{ textDecoration: 'none', color: 'var(--text-secondary)' }}>
                <Settings size={20} />
              </Link>
              <button onClick={handleSignOut} className="btn btn-danger" style={{ padding: '0.5rem 1rem' }}>
                <LogOut size={18} />
                Sign Out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-primary">
                Sign In
              </Link>
              <Link to="/signup" className="btn" style={{ backgroundColor: 'var(--bg-tertiary)' }}>
                Sign Up
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}
