import { BrowserRouter, Routes, Route, Link, useLocation, useNavigate } from 'react-router-dom'
import { RegisterPage } from '../pages/register/page'
import { LoginPage } from '../pages/login/page'
import { EnrollPage } from '../pages/enroll/page'
import { MatchPage } from '../pages/match/page'
import { PrivateRoute } from '../components/PrivateRoute'
import { reatomComponent } from '@reatom/react'
import { wrap } from '@reatom/core'
import { tokenAtom, userAtom } from '../model'
import { logoutAction } from '../utils/auth'
import { useEffect } from 'react'
import { initAuth } from '../utils/auth'

const Navigation = reatomComponent(() => {
  const location = useLocation()
  const navigate = useNavigate()
  const token = tokenAtom()
  const user = userAtom()
  
  const navStyle = {
    backgroundColor: 'white',
    borderBottom: '1px solid #e5e7eb',
    padding: '1rem 2rem',
    marginBottom: '2rem',
  }
  
  const navContent = {
    maxWidth: '1200px',
    margin: '0 auto',
    display: 'flex',
    gap: '1.5rem',
    alignItems: 'center',
    justifyContent: 'space-between',
  }
  
  const linkStyle = (isActive: boolean) => ({
    color: isActive ? '#2563eb' : '#6b7280',
    textDecoration: 'none',
    fontWeight: isActive ? 600 : 400,
    padding: '0.5rem 1rem',
    borderRadius: '4px',
    backgroundColor: isActive ? '#eff6ff' : 'transparent',
    transition: 'all 0.2s',
  })
  
  const handleLogout = () => {
    logoutAction()
    navigate('/login')
  }
  
  return (
    <nav style={navStyle}>
      <div style={navContent}>
        <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
          <Link to="/" style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1f2937', textDecoration: 'none' }}>
            Face Recognition
          </Link>
          {token && (
            <>
              <Link to="/enroll" style={linkStyle(location.pathname === '/enroll')}>
                Enroll
              </Link>
              <Link to="/match" style={linkStyle(location.pathname === '/match')}>
                Match
              </Link>
            </>
          )}
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          {token ? (
            <>
              {user && (
                <span style={{ color: '#6b7280', fontSize: '0.875rem' }}>
                  {user.username}
                </span>
              )}
              <button
                onClick={wrap(handleLogout)}
                style={{
                  padding: '0.5rem 1rem',
                  backgroundColor: '#dc2626',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  fontSize: '0.875rem',
                  fontWeight: 500,
                  cursor: 'pointer',
                }}
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" style={linkStyle(location.pathname === '/login')}>
                Login
              </Link>
              <Link to="/register" style={linkStyle(location.pathname === '/register')}>
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
})

export const App = reatomComponent(() => {
  useEffect(wrap(() => {
    initAuth()
  }), [initAuth])

  return (
    <BrowserRouter>
      <Navigation />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/"
          element={
            <PrivateRoute>
              <MatchPage />
            </PrivateRoute>
          }
        />
        <Route
          path="/enroll"
          element={
            <PrivateRoute>
              <EnrollPage />
            </PrivateRoute>
          }
        />
        <Route
          path="/match"
          element={
            <PrivateRoute>
              <MatchPage />
            </PrivateRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  )
})
