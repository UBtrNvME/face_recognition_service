import { action, withAsync, wrap } from '@reatom/core'
import fetches from '@siberiacancode/fetches'
import { tokenAtom, userAtom, authStatusAtom } from '../model'
import type { UserResponse } from '../model'

// Initialize auth state from localStorage
export const initAuth = action(async () => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
  
  if (token) {
    tokenAtom.set(token)
    authStatusAtom.set('loading')
    
    try {
      // Verify token and fetch user info
      const response = await wrap(
        fetches.get<UserResponse>('/api/v1/auth/me', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
      )
      
      userAtom.set(response.data)
      authStatusAtom.set('authenticated')
    } catch (error) {
      // Token is invalid, clear it
      tokenAtom.set(null)
      userAtom.set(null)
      authStatusAtom.set('idle')
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token')
      }
    }
  } else {
    authStatusAtom.set('idle')
  }
}).extend(withAsync())

// Logout action
export const logoutAction = action(() => {
  tokenAtom.set(null)
  userAtom.set(null)
  authStatusAtom.set('idle')
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token')
  }
})

