import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  },
  realtime: {
    params: {
      eventsPerSecond: 10
    }
  }
})

// Database types
export interface UserProfile {
  id: string
  email: string
  full_name: string
  avatar_url?: string
  created_at: string
  updated_at: string
}

export interface Video {
  id: string
  user_id: string
  title: string
  description?: string
  text_content: string
  image_url: string
  audio_url: string
  video_url: string
  thumbnail_url?: string
  duration: number
  views: number
  status: 'processing' | 'completed' | 'failed'
  settings: {
    quality: 'low' | 'medium' | 'high'
    speed: number
    voice: 'male' | 'female'
    language: string
  }
  created_at: string
  updated_at: string
}

// Storage buckets
export const STORAGE_BUCKETS = {
  IMAGES: 'images',
  AUDIO: 'audio', 
  VIDEOS: 'videos',
  THUMBNAILS: 'thumbnails'
} as const

// Helper functions
export const getPublicUrl = (bucket: string, path: string) => {
  const { data } = supabase.storage.from(bucket).getPublicUrl(path)
  return data.publicUrl
}

export const uploadFile = async (
  bucket: string, 
  path: string, 
  file: File,
  options?: { upsert?: boolean }
) => {
  const { data, error } = await supabase.storage
    .from(bucket)
    .upload(path, file, {
      upsert: options?.upsert || false,
      cacheControl: '3600'
    })
  
  if (error) throw error
  return data
}

export const deleteFile = async (bucket: string, path: string) => {
  const { error } = await supabase.storage
    .from(bucket)
    .remove([path])
  
  if (error) throw error
}

// Auth helpers
export const getCurrentUser = async () => {
  const { data: { user }, error } = await supabase.auth.getUser()
  if (error) throw error
  return user
}

export const signOut = async () => {
  const { error } = await supabase.auth.signOut()
  if (error) throw error
}

// Database helpers
export const getUserProfile = async (userId: string): Promise<UserProfile | null> => {
  const { data, error } = await supabase
    .from('user_profiles')
    .select('*')
    .eq('id', userId)
    .single()
  
  if (error && error.code !== 'PGRST116') throw error
  return data
}

export const updateUserProfile = async (userId: string, updates: Partial<UserProfile>) => {
  const { data, error } = await supabase
    .from('user_profiles')
    .update(updates)
    .eq('id', userId)
    .select()
    .single()
  
  if (error) throw error
  return data
}

export const getUserVideos = async (userId: string): Promise<Video[]> => {
  const { data, error } = await supabase
    .from('videos')
    .select('*')
    .eq('user_id', userId)
    .order('created_at', { ascending: false })
  
  if (error) throw error
  return data || []
}

export const getVideo = async (videoId: string): Promise<Video | null> => {
  const { data, error } = await supabase
    .from('videos')
    .select('*')
    .eq('id', videoId)
    .single()
  
  if (error && error.code !== 'PGRST116') throw error
  return data
}

export const createVideo = async (video: Omit<Video, 'id' | 'created_at' | 'updated_at'>) => {
  const { data, error } = await supabase
    .from('videos')
    .insert(video)
    .select()
    .single()
  
  if (error) throw error
  return data
}

export const updateVideo = async (videoId: string, updates: Partial<Video>) => {
  const { data, error } = await supabase
    .from('videos')
    .update(updates)
    .eq('id', videoId)
    .select()
    .single()
  
  if (error) throw error
  return data
}

export const deleteVideo = async (videoId: string) => {
  const { error } = await supabase
    .from('videos')
    .delete()
    .eq('id', videoId)
  
  if (error) throw error
}

export const incrementVideoViews = async (videoId: string) => {
  const { error } = await supabase.rpc('increment_video_views', {
    video_id: videoId
  })
  
  if (error) throw error
}

// Real-time subscriptions
export const subscribeToVideoUpdates = (
  videoId: string, 
  callback: (payload: any) => void
) => {
  return supabase
    .channel(`video-${videoId}`)
    .on(
      'postgres_changes',
      {
        event: 'UPDATE',
        schema: 'public',
        table: 'videos',
        filter: `id=eq.${videoId}`
      },
      callback
    )
    .subscribe()
}

export const subscribeToUserVideos = (
  userId: string,
  callback: (payload: any) => void
) => {
  return supabase
    .channel(`user-videos-${userId}`)
    .on(
      'postgres_changes',
      {
        event: '*',
        schema: 'public', 
        table: 'videos',
        filter: `user_id=eq.${userId}`
      },
      callback
    )
    .subscribe()
}

// Error handling
export const handleSupabaseError = (error: any) => {
  console.error('Supabase error:', error)
  
  if (error.code === 'PGRST116') {
    return 'Record not found'
  }
  
  if (error.code === '23505') {
    return 'Record already exists'
  }
  
  if (error.code === '42501') {
    return 'Permission denied'
  }
  
  if (error.message?.includes('JWT')) {
    return 'Authentication required'
  }
  
  return error.message || 'An unexpected error occurred'
}