import { action, computed, reatomForm, withAsync, wrap } from '@reatom/core'
import fetches from '@siberiacancode/fetches'
import { z } from 'zod'
import { authStatusAtom, authErrorAtom, type RegisterRequest, type UserResponse } from '../../model'

export const registerAction = action(
  async (body: RegisterRequest) => {
    authStatusAtom.set('loading')
    authErrorAtom.set(null)

    try {
      const response = await wrap(fetches.post<UserResponse>('/api/v1/auth/register', body))

      const user = response.data
      authStatusAtom.set('idle')
      return user
    } catch (error: any) {

      authStatusAtom.set('error')
      const errorMessage =
        error?.response?.data?.detail || error?.message || 'Registration failed'
      authErrorAtom.set(errorMessage)
      throw error
    }
  }
).extend(withAsync())

export const registerForm = reatomForm(
  {
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
    full_name: '',
  },
  {
    schema: z.object({
      email: z.string().min(1, 'Email is required').email('Please enter a valid email address'),
      username: z.string().min(3, 'Username must be at least 3 characters').max(100, 'Username must be less than 100 characters'),
      password: z.string().min(8, 'Password must be at least 8 characters'),
      confirmPassword: z.string().min(1, 'Please confirm your password'),
      full_name: z.string().optional(),
    }),
    keepErrorOnChange: false,
    validateOnChange: false,
    onSubmit: async (state) => {
      try {
        const registerResponse = await registerAction({
          email: state.email,
          username: state.username,
          password: state.password,
          full_name: state.full_name || null,
        })
        console.log('registerResponse', registerResponse)
      } catch {
        // Error is handled in registerAction
      }
    },
  }
)

export const isLoading = computed(
  () => !!registerAction.pending() || !!registerForm.submit.pending()
)

