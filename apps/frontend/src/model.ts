import { atom } from '@reatom/core'

// Type definitions for API responses
export interface UserResponse {
  id: number
  email: string
  username: string
  full_name: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
  full_name?: string | null
}

export interface FaceMatch {
  user_id: number
  distance: number
}

export interface FaceEnrollResponse {
  user_id: number
  faces_enrolled: number
}

export interface FaceUploadResponse {
  detected_faces: number
  matches: FaceMatch[]
}

export interface UserListResponse {
  users: UserResponse[]
  total: number
}

// Atoms - following reference repo pattern
export const userAtom = atom<UserResponse | null>(null, 'user')
export const tokenAtom = atom<string | null>(
  typeof window !== 'undefined' ? localStorage.getItem('token') : null,
  'token'
)
export const authStatusAtom = atom<'idle' | 'loading' | 'authenticated' | 'error'>('idle', 'authStatus')
export const authErrorAtom = atom<string | null>(null, 'authError')

// Sync token to localStorage - using atom's onChange if available
// Note: In newer Reatom versions, this might need to be handled differently
if (typeof window !== 'undefined' && 'onChange' in tokenAtom) {
  (tokenAtom as any).onChange((token: string | null) => {
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  })
}

