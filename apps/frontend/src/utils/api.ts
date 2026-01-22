// Helper to get auth headers - reads token from localStorage
// Note: In actions/components, the token should be read from the atom directly
// but for utility functions, we read from localStorage as a fallback
export const getAuthHeaders = (): Record<string, string> => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null
  if (token) {
    return {
      Authorization: `Bearer ${token}`,
    }
  }
  return {}
}

