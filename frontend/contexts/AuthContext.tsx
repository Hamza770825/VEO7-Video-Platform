'use client'

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { User, Session } from '@supabase/supabase-js'
import { useSupabaseClient, useSessionContext } from '@supabase/auth-helpers-react'
import { useRouter } from 'next/navigation'
import { toast } from 'react-hot-toast'

// Types
interface UserProfile {
  id: string
  email: string
  full_name: string
  avatar_url?: string
  created_at: string
  updated_at: string
}

interface AuthContextType {
  // User state
  user: User | null
  profile: UserProfile | null
  session: Session | null
  
  // Loading states
  isLoading: boolean
  isInitializing: boolean
  
  // Auth methods
  signIn: (email: string, password: string) => Promise<{ success: boolean; error?: string }>
  signUp: (email: string, password: string, fullName: string) => Promise<{ success: boolean; error?: string }>
  signInWithGoogle: () => Promise<{ success: boolean; error?: string }>
  signOut: () => Promise<void>
  resetPassword: (email: string) => Promise<{ success: boolean; error?: string }>
  updateProfile: (updates: Partial<UserProfile>) => Promise<{ success: boolean; error?: string }>
  
  // Utility methods
  refreshSession: () => Promise<void>
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const supabase = useSupabaseClient()
  const { session, isLoading: sessionLoading } = useSessionContext()
  const router = useRouter()
  
  // State
  const [user, setUser] = useState<User | null>(null)
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isInitializing, setIsInitializing] = useState(true)

  // Initialize auth state
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        if (session?.user) {
          setUser(session.user)
          await fetchUserProfile(session.user.id)
        } else {
          setUser(null)
          setProfile(null)
        }
      } catch (error) {
        console.error('Error initializing auth:', error)
      } finally {
        setIsInitializing(false)
      }
    }

    initializeAuth()
  }, [session])

  // Fetch user profile
  const fetchUserProfile = async (userId: string) => {
    try {
      const { data, error } = await supabase
        .from('users')
        .select('*')
        .eq('id', userId)
        .single()

      if (error) {
        console.error('Error fetching profile:', error)
        return
      }

      setProfile(data)
    } catch (error) {
      console.error('Error fetching profile:', error)
    }
  }

  // Sign in with email and password
  const signIn = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      })

      if (error) {
        return { success: false, error: error.message }
      }

      if (data.user) {
        setUser(data.user)
        await fetchUserProfile(data.user.id)
        return { success: true }
      }

      return { success: false, error: 'Unknown error occurred' }
    } catch (error) {
      return { success: false, error: 'Network error occurred' }
    } finally {
      setIsLoading(false)
    }
  }

  // Sign up with email and password
  const signUp = async (email: string, password: string, fullName: string) => {
    setIsLoading(true)
    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: fullName,
          }
        }
      })

      if (error) {
        return { success: false, error: error.message }
      }

      if (data.user) {
        // Create user profile
        const { error: profileError } = await supabase
          .from('users')
          .insert([
            {
              id: data.user.id,
              email: data.user.email,
              full_name: fullName,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
            }
          ])

        if (profileError) {
          console.error('Error creating profile:', profileError)
        }

        return { success: true }
      }

      return { success: false, error: 'Unknown error occurred' }
    } catch (error) {
      return { success: false, error: 'Network error occurred' }
    } finally {
      setIsLoading(false)
    }
  }

  // Sign in with Google
  const signInWithGoogle = async () => {
    setIsLoading(true)
    try {
      const { error } = await supabase.auth.signInWithOAuth({
        provider: 'google',
        options: {
          redirectTo: `${window.location.origin}/dashboard`
        }
      })

      if (error) {
        return { success: false, error: error.message }
      }

      return { success: true }
    } catch (error) {
      return { success: false, error: 'Network error occurred' }
    } finally {
      setIsLoading(false)
    }
  }

  // Sign out
  const signOut = async () => {
    setIsLoading(true)
    try {
      const { error } = await supabase.auth.signOut()
      
      if (error) {
        toast.error('Error signing out')
        console.error('Sign out error:', error)
      } else {
        setUser(null)
        setProfile(null)
        router.push('/')
        toast.success('Signed out successfully')
      }
    } catch (error) {
      toast.error('Network error occurred')
      console.error('Sign out error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Reset password
  const resetPassword = async (email: string) => {
    setIsLoading(true)
    try {
      const { error } = await supabase.auth.resetPasswordForEmail(email, {
        redirectTo: `${window.location.origin}/auth/reset-password`,
      })

      if (error) {
        return { success: false, error: error.message }
      }

      return { success: true }
    } catch (error) {
      return { success: false, error: 'Network error occurred' }
    } finally {
      setIsLoading(false)
    }
  }

  // Update profile
  const updateProfile = async (updates: Partial<UserProfile>) => {
    if (!user) {
      return { success: false, error: 'User not authenticated' }
    }

    setIsLoading(true)
    try {
      const { data, error } = await supabase
        .from('users')
        .update({
          ...updates,
          updated_at: new Date().toISOString(),
        })
        .eq('id', user.id)
        .select()
        .single()

      if (error) {
        return { success: false, error: error.message }
      }

      setProfile(data)
      return { success: true }
    } catch (error) {
      return { success: false, error: 'Network error occurred' }
    } finally {
      setIsLoading(false)
    }
  }

  // Refresh session
  const refreshSession = async () => {
    try {
      const { data, error } = await supabase.auth.refreshSession()
      if (error) {
        console.error('Error refreshing session:', error)
      }
    } catch (error) {
      console.error('Error refreshing session:', error)
    }
  }

  const value: AuthContextType = {
    // User state
    user,
    profile,
    session,
    
    // Loading states
    isLoading: isLoading || sessionLoading,
    isInitializing,
    
    // Auth methods
    signIn,
    signUp,
    signInWithGoogle,
    signOut,
    resetPassword,
    updateProfile,
    
    // Utility methods
    refreshSession,
    isAuthenticated: !!user,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export default AuthProvider