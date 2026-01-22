import { bindField, reatomComponent } from '@reatom/react'
import { isLoading, registerForm } from './model'
import { authErrorAtom } from '../../model'
import { wrap } from '@reatom/core'


export const RegisterPage = reatomComponent(() => {
  const loading = isLoading()
  const error = authErrorAtom()
  const emailField = bindField(registerForm.fields.email)
  const usernameField = bindField(registerForm.fields.username)
  const passwordField = bindField(registerForm.fields.password)
  const confirmPasswordField = bindField(registerForm.fields.confirmPassword)
  const fullNameField = bindField(registerForm.fields.full_name)
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
          registerForm.submit()
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
          Register
        </h1>
        <p style={{
          color: '#6b7280',
          textAlign: 'center',
          marginBottom: '2rem',
        }}>
          Create a new account
        </p>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <label htmlFor="email" style={{ fontWeight: 500 }}>
              Email
            </label>
            <input
              id="email"
              type="email"
              {...emailField}
              placeholder="Enter your email"
              style={{
                padding: '0.75rem',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '1rem',
              }}
            />
            {emailField.error && (
              <p style={{ color: '#dc2626', fontSize: '0.875rem', margin: 0 }}>
                {emailField.error}
              </p>
            )}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <label htmlFor="username" style={{ fontWeight: 500 }}>
              Username
            </label>
            <input
              id="username"
              type="text"
              {...usernameField}
              placeholder="Enter your username"
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

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <label htmlFor="confirmPassword" style={{ fontWeight: 500 }}>
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              type="password"
              {...confirmPasswordField}
              placeholder="Confirm your password"
              style={{
                padding: '0.75rem',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '1rem',
              }}
            />
            {confirmPasswordField.error && (
              <p style={{ color: '#dc2626', fontSize: '0.875rem', margin: 0 }}>
                {confirmPasswordField.error}
              </p>
            )}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <label htmlFor="full_name" style={{ fontWeight: 500 }}>
              Full Name (Optional)
            </label>
            <input
              id="full_name"
              type="text"
              {...fullNameField}
              placeholder="Enter your full name"
              style={{
                padding: '0.75rem',
                border: '1px solid #ccc',
                borderRadius: '4px',
                fontSize: '1rem',
              }}
            />
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
            {loading ? 'Registering...' : 'Register'}
          </button>
        </div>
      </form>
    </div>
  )
})

