import { bindField, reatomComponent } from '@reatom/react'
import { isLoading, loginForm } from './model'
import { authErrorAtom, authStatusAtom } from '../../model'
import { wrap } from '@reatom/core'
import { useNavigate, useLocation } from 'react-router-dom'
import { useEffect } from 'react'

export const LoginPage = reatomComponent(() => {
    const loading = isLoading()
    const error = authErrorAtom()
    const authStatus = authStatusAtom()
    const navigate = useNavigate()
    const location = useLocation()
    const usernameField = bindField(loginForm.fields.username)
    const passwordField = bindField(loginForm.fields.password)

    // Redirect after successful login
    useEffect(wrap(() => {
        if (authStatus === 'authenticated') {
            const from = (location.state as any)?.from?.pathname || '/'
            navigate(from, { replace: true })
        }
    }), [authStatus, navigate, location])

    return (
        <div style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#f9fafb',
            padding: '2rem',
        }}>
            <form
                onSubmit={wrap((event) => {
                    event.preventDefault()
                    loginForm.submit()
                })}
                style={{
                    width: '100%',
                    maxWidth: '400px',
                    backgroundColor: 'white',
                    padding: '2rem',
                    borderRadius: '8px',
                    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1)',
                }}
            >
                <h1 style={{
                    fontSize: '2rem',
                    fontWeight: 700,
                    marginBottom: '0.5rem',
                    textAlign: 'center',
                }}>
                    Login
                </h1>
                <p style={{
                    color: '#6b7280',
                    textAlign: 'center',
                    marginBottom: '2rem',
                }}>
                    Sign in to your account
                </p>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <label htmlFor="username" style={{ fontWeight: 500 }}>
                            Username or Email
                        </label>
                        <input
                            id="username"
                            type="text"
                            {...usernameField}
                            placeholder="Enter your username or email"
                            style={{
                                padding: '0.75rem',
                                border: '1px solid #ccc',
                                borderRadius: '4px',
                                fontSize: '1rem',
                            }}
                        />
                        {usernameField.error && (
                            <p style={{ color: '#dc2626', fontSize: '0.875rem', margin: 0 }}>
                                {usernameField.error}
                            </p>
                        )}
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <label htmlFor="password" style={{ fontWeight: 500 }}>
                            Password
                        </label>
                        <input
                            id="password"
                            type="password"
                            {...passwordField}
                            placeholder="Enter your password"
                            style={{
                                padding: '0.75rem',
                                border: '1px solid #ccc',
                                borderRadius: '4px',
                                fontSize: '1rem',
                            }}
                        />
                        {passwordField.error && (
                            <p style={{ color: '#dc2626', fontSize: '0.875rem', margin: 0 }}>
                                {passwordField.error}
                            </p>
                        )}
                    </div>

                    {error && (
                        <div style={{
                            color: '#dc2626',
                            fontSize: '0.875rem',
                            padding: '0.75rem',
                            backgroundColor: '#fef2f2',
                            border: '1px solid #fecaca',
                            borderRadius: '4px',
                        }}>
                            {error}
                        </div>
                    )}

                    <button
                        type="submit"
                        disabled={loading}
                        style={{
                            padding: '0.75rem 1.5rem',
                            backgroundColor: loading ? '#9ca3af' : '#2563eb',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            fontSize: '1rem',
                            fontWeight: 500,
                            cursor: loading ? 'not-allowed' : 'pointer',
                            transition: 'background-color 0.2s',
                        }}
                    >
                        {loading ? 'Logging in...' : 'Login'}
                    </button>

                    <p style={{ textAlign: 'center', margin: 0, color: '#6b7280', fontSize: '0.875rem' }}>
                        Don't have an account?{' '}
                        <a
                            href="/register"
                            onClick={(e) => {
                                e.preventDefault()
                                navigate('/register')
                            }}
                            style={{ color: '#2563eb', textDecoration: 'none' }}
                        >
                            Register
                        </a>
                    </p>
                </div>
            </form>
        </div>
    )
})

