import { reatomComponent } from '@reatom/react'
import { Navigate, useLocation } from 'react-router-dom'
import { tokenAtom, authStatusAtom } from '../model'

interface PrivateRouteProps {
  children: React.ReactNode
}

export const PrivateRoute = reatomComponent<PrivateRouteProps>(({ children }) => {
  const token = tokenAtom()
  const authStatus = authStatusAtom()
  const location = useLocation()

  // If no token, redirect to login
  if (!token && authStatus !== 'loading') {
    return <Navigate to="/login" state={{ from: location }} replace />
  }

  // If we have a token but status is not authenticated, we might be loading
  if (token && authStatus === 'loading') {
    return (
      <div style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <p>Loading...</p>
      </div>
    )
  }

  return <>{children}</>
})

