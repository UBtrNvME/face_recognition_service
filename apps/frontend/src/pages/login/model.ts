import { action, computed, reatomForm, withAsync, wrap } from '@reatom/core'
import fetches from '@siberiacancode/fetches'
import { z } from 'zod'
import { authStatusAtom, authErrorAtom, tokenAtom, userAtom, type UserResponse } from '../../model'

export interface TokenResponse {
    access_token: string
}

export const loginAction = action(
    async (username: string, password: string) => {
        authStatusAtom.set('loading')
        authErrorAtom.set(null)

        try {
            // OAuth2PasswordRequestForm expects form data with username and password
            const formData = new URLSearchParams()
            formData.append('username', username)
            formData.append('password', password)

            const response = await wrap(
                fetches.post<TokenResponse>(
                    '/api/v1/auth/login',
                    formData.toString(),
                    {
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                    }
                )
            )

            const token = response.data.access_token
            tokenAtom.set(token)
            localStorage.setItem('token', token)

            // Fetch user info
            const userResponse = await wrap(
                fetches.get<UserResponse>('/api/v1/auth/me', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })
            )

            userAtom.set(userResponse.data)
            authStatusAtom.set('authenticated')
            return userResponse.data
        } catch (error: any) {
            authStatusAtom.set('error')
            const errorMessage =
                error?.response?.data?.detail || error?.message || 'Login failed'
            authErrorAtom.set(errorMessage)
            throw error
        }
    }
).extend(withAsync())

export const loginForm = reatomForm(
    {
        username: '',
        password: '',
    },
    {
        schema: z.object({
            username: z.string().min(1, 'Username or email is required'),
            password: z.string().min(1, 'Password is required'),
        }),
        keepErrorOnChange: false,
        validateOnChange: false,
        onSubmit: async (state) => {
            try {
                await loginAction(state.username, state.password)
                // Navigation will be handled in the component after successful login
            } catch {
                // Error is handled in loginAction
            }
        },
    }
)

export const isLoading = computed(
    () => !!loginAction.pending() || !!loginForm.submit.pending()
)

