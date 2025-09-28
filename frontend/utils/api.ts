import { supabase } from './supabase'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// API client with authentication
class ApiClient {
  private baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  private async getAuthHeaders() {
    const { data: { session } } = await supabase.auth.getSession()
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    }

    if (session?.access_token) {
      headers['Authorization'] = `Bearer ${session.access_token}`
    }

    return headers
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`
    const headers = await this.getAuthHeaders()

    const config: RequestInit = {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      },
    }

    const response = await fetch(url, config)

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
    }

    return response.json()
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' })
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }

  async uploadFile<T>(endpoint: string, formData: FormData): Promise<T> {
    const { data: { session } } = await supabase.auth.getSession()
    const headers: Record<string, string> = {}

    if (session?.access_token) {
      headers['Authorization'] = `Bearer ${session.access_token}`
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      method: 'POST',
      headers,
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`)
    }

    return response.json()
  }
}

export const apiClient = new ApiClient(API_BASE_URL)

// API endpoints
export const api = {
  // Health check
  health: () => apiClient.get('/health'),

  // User endpoints
  user: {
    profile: () => apiClient.get('/api/user/profile'),
    updateProfile: (data: any) => apiClient.put('/api/user/profile', data),
    stats: () => apiClient.get('/api/user/stats'),
  },

  // Video endpoints
  videos: {
    list: (params?: { page?: number; limit?: number }) => {
      const query = new URLSearchParams()
      if (params?.page) query.append('page', params.page.toString())
      if (params?.limit) query.append('limit', params.limit.toString())
      return apiClient.get(`/api/videos?${query.toString()}`)
    },
    
    get: (id: string) => apiClient.get(`/api/videos/${id}`),
    
    create: (data: {
      title: string
      description?: string
      text_content: string
      settings: {
        quality: 'low' | 'medium' | 'high'
        speed: number
        voice: 'male' | 'female'
        language: string
      }
    }) => apiClient.post('/api/videos/create', data),
    
    uploadImage: (videoId: string, file: File) => {
      const formData = new FormData()
      formData.append('image', file)
      return apiClient.uploadFile(`/api/videos/${videoId}/upload-image`, formData)
    },
    
    status: (id: string) => apiClient.get(`/api/videos/${id}/status`),
    
    process: (id: string) => apiClient.post(`/api/videos/${id}/process`),
    
    download: (id: string) => apiClient.get(`/api/videos/${id}/download`),
    
    delete: (id: string) => apiClient.delete(`/api/videos/${id}`),
    
    incrementViews: (id: string) => apiClient.post(`/api/videos/${id}/views`),
  },

  // Audio endpoints
  audio: {
    generateFromText: (data: {
      text: string
      language: string
      voice: 'male' | 'female'
      speed: number
    }) => apiClient.post('/api/audio/generate', data),
    
    upload: (file: File) => {
      const formData = new FormData()
      formData.append('audio', file)
      return apiClient.uploadFile('/api/audio/upload', formData)
    },
  },

  // Translation endpoints
  translation: {
    translate: (data: {
      text: string
      source_language: string
      target_language: string
    }) => apiClient.post('/api/translation/translate', data),
    
    detectLanguage: (text: string) => 
      apiClient.post('/api/translation/detect', { text }),
    
    supportedLanguages: () => apiClient.get('/api/translation/languages'),
  },

  // File management
  files: {
    upload: (file: File, type: 'image' | 'audio' | 'video') => {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('type', type)
      return apiClient.uploadFile('/api/files/upload', formData)
    },
    
    delete: (fileId: string) => apiClient.delete(`/api/files/${fileId}`),
  },

  // System endpoints
  system: {
    info: () => apiClient.get('/api/system/info'),
    stats: () => apiClient.get('/api/system/stats'),
  },
}

// Response types
export interface ApiResponse<T = any> {
  success: boolean
  data: T
  message?: string
  error?: string
}

export interface VideoCreateResponse {
  video_id: string
  status: 'created'
  message: string
}

export interface VideoStatusResponse {
  video_id: string
  status: 'processing' | 'completed' | 'failed'
  progress: number
  current_step: string
  estimated_time_remaining?: number
  error?: string
}

export interface UserStatsResponse {
  total_videos: number
  total_views: number
  total_duration: number
  storage_used: number
  videos_this_month: number
}

export interface SystemInfoResponse {
  version: string
  uptime: number
  memory_usage: number
  cpu_usage: number
  disk_usage: number
  active_processes: number
}

// Error handling
export class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public code?: string
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

// Utility functions
export const handleApiError = (error: any): string => {
  if (error instanceof ApiError) {
    return error.message
  }
  
  if (error.message) {
    return error.message
  }
  
  return 'An unexpected error occurred'
}

export const isApiError = (error: any): error is ApiError => {
  return error instanceof ApiError
}

// Request interceptors for common patterns
export const withRetry = async <T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  delay = 1000
): Promise<T> => {
  let lastError: Error

  for (let i = 0; i <= maxRetries; i++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error
      
      if (i === maxRetries) {
        throw lastError
      }
      
      await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, i)))
    }
  }
  
  throw lastError!
}

export const withTimeout = <T>(
  promise: Promise<T>,
  timeoutMs = 30000
): Promise<T> => {
  return Promise.race([
    promise,
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error('Request timeout')), timeoutMs)
    ),
  ])
}

// Polling utility for video status
export const pollVideoStatus = async (
  videoId: string,
  onUpdate?: (status: VideoStatusResponse) => void,
  intervalMs = 2000,
  maxAttempts = 150 // 5 minutes max
): Promise<VideoStatusResponse> => {
  let attempts = 0

  return new Promise((resolve, reject) => {
    const poll = async () => {
      try {
        attempts++
        const status = await api.videos.status(videoId) as VideoStatusResponse
        
        onUpdate?.(status)
        
        if (status.status === 'completed' || status.status === 'failed') {
          resolve(status)
          return
        }
        
        if (attempts >= maxAttempts) {
          reject(new Error('Polling timeout: Video processing took too long'))
          return
        }
        
        setTimeout(poll, intervalMs)
      } catch (error) {
        reject(error)
      }
    }
    
    poll()
  })
}