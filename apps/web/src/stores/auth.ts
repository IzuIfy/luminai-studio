import { create } from 'zustand'
import { apiClient } from '@luminai/api-client'

interface User {
  id: string
  email: string
  name: string
  avatar?: string
  createdAt: string
}

interface AuthState {
  user: User | null
  token: string | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, name: string) => Promise<void>
  logout: () => Promise<void>
  setUser: (user: User | null) => void
  setToken: (token: string | null) => void
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: typeof window !== 'undefined' ? localStorage.getItem('authToken') : null,
  isLoading: false,
  isAuthenticated: false,

  login: async (email: string, password: string) => {
    set({ isLoading: true })
    try {
      const response = await apiClient.auth.login({ email, password })
      localStorage.setItem('authToken', response.token)
      set({
        token: response.token,
        user: response.user,
        isAuthenticated: true
      })
    } catch (error) {
      throw error
    } finally {
      set({ isLoading: false })
    }
  },

  register: async (email: string, password: string, name: string) => {
    set({ isLoading: true })
    try {
      const response = await apiClient.auth.register({ email, password, name })
      localStorage.setItem('authToken', response.token)
      set({
        token: response.token,
        user: response.user,
        isAuthenticated: true
      })
    } catch (error) {
      throw error
    } finally {
      set({ isLoading: false })
    }
  },

  logout: async () => {
    set({ isLoading: true })
    try {
      await apiClient.auth.logout()
      localStorage.removeItem('authToken')
      set({
        token: null,
        user: null,
        isAuthenticated: false
      })
    } catch (error) {
      throw error
    } finally {
      set({ isLoading: false })
    }
  },

  setUser: (user: User | null) => set({ user }),
  setToken: (token: string | null) => set({ token })
}))
