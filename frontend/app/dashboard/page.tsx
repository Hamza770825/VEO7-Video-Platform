'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { toast } from 'react-hot-toast'
import { useAuth } from '../../contexts/AuthContext'
import { 
  PlusIcon,
  PlayIcon,
  DocumentTextIcon,
  PhotoIcon,
  ClockIcon,
  EyeIcon,
  TrashIcon,
  ArrowDownTrayIcon,
  ShareIcon,
  ChartBarIcon,
  UserIcon,
  CogIcon,
  ArrowRightIcon,
  ArrowLeftIcon,
  ChevronDownIcon,
  ArrowRightOnRectangleIcon,
  VideoCameraIcon,
  WalletIcon,
  CreditCardIcon,
  ChatBubbleLeftRightIcon,
  StarIcon,
  Bars3Icon,
  XMarkIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'
import { useLanguage } from '../providers'
import Link from 'next/link'

interface Video {
  id: string
  title: string
  description: string
  thumbnail_url: string
  video_url: string
  duration: number
  views: number
  created_at: string
  status: 'processing' | 'completed' | 'failed'
}

interface DashboardStats {
  totalVideos: number
  totalViews: number
  totalDuration: number
  thisMonthVideos: number
  coinsBalance: number
  subscriptionStatus: string
}

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 }
}

const staggerChildren = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
}

export default function DashboardPage() {
  const [videos, setVideos] = useState<Video[]>([])
  const [stats, setStats] = useState<DashboardStats>({
    totalVideos: 0,
    totalViews: 0,
    totalDuration: 0,
    thisMonthVideos: 0,
    coinsBalance: 100,
    subscriptionStatus: 'free'
  })
  const [isLoading, setIsLoading] = useState(true)
  const [selectedVideo, setSelectedVideo] = useState<Video | null>(null)
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [activeTab, setActiveTab] = useState('projects')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  
  const { user, loading, signOut } = useAuth()
  const router = useRouter()
  const { language, isRTL } = useLanguage()

  useEffect(() => {
    if (loading) return
    
    if (!user) {
      router.push('/auth/login')
      return
    }
    
    fetchUserVideos()
    fetchUserStats()
  }, [user, loading])

  const fetchUserVideos = async () => {
    try {
      setIsLoading(true)
      // Mock data for now
      const mockVideos: Video[] = [
        {
          id: '1',
          title: language === 'ar' ? 'فيديو تجريبي 1' : 'Sample Video 1',
          description: language === 'ar' ? 'وصف الفيديو التجريبي' : 'Sample video description',
          thumbnail_url: '/placeholder-thumbnail.jpg',
          video_url: '/placeholder-video.mp4',
          duration: 120,
          views: 150,
          created_at: new Date().toISOString(),
          status: 'completed'
        },
        {
          id: '2',
          title: language === 'ar' ? 'فيديو تجريبي 2' : 'Sample Video 2',
          description: language === 'ar' ? 'وصف الفيديو التجريبي' : 'Sample video description',
          thumbnail_url: '/placeholder-thumbnail.jpg',
          video_url: '/placeholder-video.mp4',
          duration: 90,
          views: 89,
          created_at: new Date().toISOString(),
          status: 'processing'
        }
      ]
      setVideos(mockVideos)
    } catch (error) {
      toast.error(language === 'ar' ? 'خطأ في تحميل الفيديوهات' : 'Error loading videos')
    } finally {
      setIsLoading(false)
    }
  }

  const fetchUserStats = async () => {
    try {
      // Mock stats for now
      setStats({
        totalVideos: 12,
        totalViews: 1250,
        totalDuration: 1800,
        thisMonthVideos: 5,
        coinsBalance: 100,
        subscriptionStatus: 'free'
      })
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  const handleSignOut = async () => {
    try {
      await signOut()
      router.push('/')
    } catch (error) {
      toast.error(
        language === 'ar' 
          ? 'حدث خطأ في تسجيل الخروج'
          : 'Error signing out'
      )
    }
  }

  const formatDuration = (seconds: number) => {
    const minutes = Math.floor(seconds / 60)
    const remainingSeconds = seconds % 60
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString(language === 'ar' ? 'ar-SA' : 'en-US')
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600 bg-green-100'
      case 'processing': return 'text-yellow-600 bg-yellow-100'
      case 'failed': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getStatusText = (status: string) => {
    if (language === 'ar') {
      switch (status) {
        case 'completed': return 'مكتمل'
        case 'processing': return 'قيد المعالجة'
        case 'failed': return 'فشل'
        default: return 'غير معروف'
      }
    } else {
      switch (status) {
        case 'completed': return 'Completed'
        case 'processing': return 'Processing'
        case 'failed': return 'Failed'
        default: return 'Unknown'
      }
    }
  }

  const sidebarItems = [
    {
      id: 'projects',
      icon: VideoCameraIcon,
      label: language === 'ar' ? 'المشاريع' : 'Projects',
      count: stats.totalVideos
    },
    {
      id: 'create',
      icon: PlusIcon,
      label: language === 'ar' ? 'إنشاء جديد' : 'Create New',
      count: null
    },
    {
      id: 'ai-studio',
      icon: SparklesIcon,
      label: language === 'ar' ? 'استوديو الذكاء الاصطناعي' : 'AI Studio',
      count: null,
      href: '/ai-studio'
    },
    {
      id: 'wallet',
      icon: WalletIcon,
      label: language === 'ar' ? 'المحفظة' : 'Wallet',
      count: stats.coinsBalance
    },
    {
      id: 'subscriptions',
      icon: CreditCardIcon,
      label: language === 'ar' ? 'الاشتراكات' : 'Subscriptions',
      count: null
    },
    {
      id: 'comments',
      icon: ChatBubbleLeftRightIcon,
      label: language === 'ar' ? 'التعليقات' : 'Comments',
      count: null
    },
    {
      id: 'settings',
      icon: CogIcon,
      label: language === 'ar' ? 'الإعدادات' : 'Settings',
      count: null
    }
  ]

  if (!user) {
    return null
  }

  return (
    <div className={`min-h-screen ${isRTL ? 'rtl' : 'ltr'} bg-gray-50 dark:bg-gray-900`}>
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo and Mobile Menu */}
            <div className="flex items-center">
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden p-2 rounded-md text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                {sidebarOpen ? (
                  <XMarkIcon className="w-6 h-6" />
                ) : (
                  <Bars3Icon className="w-6 h-6" />
                )}
              </button>
              
              <Link href="/" className="flex items-center space-x-2 ml-4 lg:ml-0">
                <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                  <VideoCameraIcon className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                  VEO7
                </span>
              </Link>
            </div>

            {/* User Menu */}
            <div className="relative">
              <button
                onClick={() => setShowUserMenu(!showUserMenu)}
                className="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                  <UserIcon className="w-5 h-5 text-white" />
                </div>
                <span className="hidden md:block text-gray-700 dark:text-gray-300 font-medium">
                  {user.email}
                </span>
                <ChevronDownIcon className="w-4 h-4 text-gray-500" />
              </button>

              {showUserMenu && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50"
                >
                  <div className="py-2">
                    <Link
                      href="/profile"
                      className="flex items-center px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                    >
                      <UserIcon className="w-4 h-4 mr-3" />
                      {language === 'ar' ? 'الملف الشخصي' : 'Profile'}
                    </Link>
                    <Link
                      href="/settings"
                      className="flex items-center px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                    >
                      <CogIcon className="w-4 h-4 mr-3" />
                      {language === 'ar' ? 'الإعدادات' : 'Settings'}
                    </Link>
                    <hr className="my-2 border-gray-200 dark:border-gray-700" />
                    <button
                      onClick={handleSignOut}
                      className="flex items-center w-full px-4 py-2 text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20"
                    >
                      <ArrowRightOnRectangleIcon className="w-4 h-4 mr-3" />
                      {language === 'ar' ? 'تسجيل الخروج' : 'Sign Out'}
                    </button>
                  </div>
                </motion.div>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className={`${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0 fixed lg:static inset-y-0 left-0 z-40 w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 transition-transform duration-300 ease-in-out`}>
          <div className="p-6">
            <nav className="space-y-2">
              {sidebarItems.map((item) => (
                item.href ? (
                  <Link
                    key={item.id}
                    href={item.href}
                    onClick={() => setSidebarOpen(false)}
                    className="w-full flex items-center justify-between px-4 py-3 rounded-lg transition-colors text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    <div className="flex items-center space-x-3 rtl:space-x-reverse">
                      <item.icon className="w-5 h-5" />
                      <span className="font-medium">{item.label}</span>
                    </div>
                    {item.count !== null && (
                      <span className="px-2 py-1 text-xs rounded-full bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400">
                        {item.count}
                      </span>
                    )}
                  </Link>
                ) : (
                  <button
                    key={item.id}
                    onClick={() => {
                      setActiveTab(item.id)
                      setSidebarOpen(false)
                    }}
                    className={`w-full flex items-center justify-between px-4 py-3 rounded-lg transition-colors ${
                      activeTab === item.id
                        ? 'bg-purple-100 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400'
                        : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                    }`}
                  >
                    <div className="flex items-center space-x-3 rtl:space-x-reverse">
                      <item.icon className="w-5 h-5" />
                      <span className="font-medium">{item.label}</span>
                    </div>
                    {item.count !== null && (
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        activeTab === item.id
                          ? 'bg-purple-200 dark:bg-purple-800 text-purple-700 dark:text-purple-300'
                          : 'bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
                      }`}>
                        {item.count}
                      </span>
                    )}
                  </button>
                )
              ))}
            </nav>
          </div>
        </aside>

        {/* Overlay for mobile */}
        {sidebarOpen && (
          <div
            className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Main Content */}
        <main className="flex-1 p-6">
          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 dark:text-gray-400 text-sm font-medium">
                    {language === 'ar' ? 'إجمالي الفيديوهات' : 'Total Videos'}
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {stats.totalVideos}
                  </p>
                </div>
                <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center">
                  <VideoCameraIcon className="w-6 h-6 text-purple-600 dark:text-purple-400" />
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 dark:text-gray-400 text-sm font-medium">
                    {language === 'ar' ? 'إجمالي المشاهدات' : 'Total Views'}
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {stats.totalViews.toLocaleString()}
                  </p>
                </div>
                <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                  <EyeIcon className="w-6 h-6 text-blue-600 dark:text-blue-400" />
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 dark:text-gray-400 text-sm font-medium">
                    {language === 'ar' ? 'رصيد الكوينز' : 'Coins Balance'}
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {stats.coinsBalance}
                  </p>
                </div>
                <div className="w-12 h-12 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg flex items-center justify-center">
                  <WalletIcon className="w-6 h-6 text-yellow-600 dark:text-yellow-400" />
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-600 dark:text-gray-400 text-sm font-medium">
                    {language === 'ar' ? 'هذا الشهر' : 'This Month'}
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {stats.thisMonthVideos}
                  </p>
                </div>
                <div className="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center">
                  <ChartBarIcon className="w-6 h-6 text-green-600 dark:text-green-400" />
                </div>
              </div>
            </motion.div>
          </div>

          {/* Content based on active tab */}
          {activeTab === 'projects' && (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
              <div className="p-6 border-b border-gray-200 dark:border-gray-700">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                    {language === 'ar' ? 'مشاريعي' : 'My Projects'}
                  </h2>
                  <Link
                    href="/create"
                    className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-4 py-2 rounded-lg hover:shadow-lg transition-all duration-300 transform hover:scale-105 flex items-center space-x-2"
                  >
                    <PlusIcon className="w-4 h-4" />
                    <span>{language === 'ar' ? 'إنشاء جديد' : 'Create New'}</span>
                  </Link>
                </div>
              </div>

              <div className="p-6">
                {isLoading ? (
                  <div className="flex items-center justify-center py-12">
                    <div className="w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
                  </div>
                ) : videos.length === 0 ? (
                  <div className="text-center py-12">
                    <VideoCameraIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                      {language === 'ar' ? 'لا توجد فيديوهات بعد' : 'No videos yet'}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 mb-6">
                      {language === 'ar' 
                        ? 'ابدأ بإنشاء أول فيديو لك'
                        : 'Start by creating your first video'
                      }
                    </p>
                    <Link
                      href="/create"
                      className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-3 rounded-lg hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                    >
                      {language === 'ar' ? 'إنشاء فيديو' : 'Create Video'}
                    </Link>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {videos.map((video, index) => (
                      <motion.div
                        key={video.id}
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="group relative bg-gray-50 dark:bg-gray-700 rounded-lg overflow-hidden hover:shadow-lg transition-all duration-300"
                      >
                        <div className="aspect-video bg-gradient-to-br from-purple-100 to-pink-100 dark:from-purple-900/20 dark:to-pink-900/20 flex items-center justify-center">
                          <PlayIcon className="w-12 h-12 text-purple-600 dark:text-purple-400" />
                        </div>
                        
                        <div className="p-4">
                          <div className="flex items-center justify-between mb-2">
                            <h3 className="font-medium text-gray-900 dark:text-white truncate">
                              {video.title}
                            </h3>
                            <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(video.status)}`}>
                              {getStatusText(video.status)}
                            </span>
                          </div>
                          
                          <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2">
                            {video.description}
                          </p>
                          
                          <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
                            <div className="flex items-center space-x-4">
                              <div className="flex items-center space-x-1">
                                <EyeIcon className="w-4 h-4" />
                                <span>{video.views}</span>
                              </div>
                              <div className="flex items-center space-x-1">
                                <ClockIcon className="w-4 h-4" />
                                <span>{formatDuration(video.duration)}</span>
                              </div>
                            </div>
                            <span>{formatDate(video.created_at)}</span>
                          </div>
                          
                          <div className="flex items-center justify-between mt-4">
                            <div className="flex items-center space-x-2">
                              <button className="p-2 text-gray-600 dark:text-gray-400 hover:text-purple-600 dark:hover:text-purple-400 transition-colors">
                                <PlayIcon className="w-4 h-4" />
                              </button>
                              <button className="p-2 text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                                <ArrowDownTrayIcon className="w-4 h-4" />
                              </button>
                              <button className="p-2 text-gray-600 dark:text-gray-400 hover:text-green-600 dark:hover:text-green-400 transition-colors">
                                <ShareIcon className="w-4 h-4" />
                              </button>
                            </div>
                            <button className="p-2 text-gray-600 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors">
                              <TrashIcon className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'create' && (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8">
              <div className="text-center">
                <PlusIcon className="w-16 h-16 text-purple-600 dark:text-purple-400 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  {language === 'ar' ? 'إنشاء فيديو جديد' : 'Create New Video'}
                </h2>
                <p className="text-gray-600 dark:text-gray-400 mb-8">
                  {language === 'ar' 
                    ? 'اختر نوع الفيديو الذي تريد إنشاؤه'
                    : 'Choose the type of video you want to create'
                  }
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-4xl mx-auto">
                  <Link
                    href="/create/image-to-video"
                    className="group p-6 border-2 border-gray-200 dark:border-gray-700 rounded-xl hover:border-purple-500 dark:hover:border-purple-400 transition-colors"
                  >
                    <PhotoIcon className="w-12 h-12 text-purple-600 dark:text-purple-400 mx-auto mb-4 group-hover:scale-110 transition-transform" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      {language === 'ar' ? 'صورة إلى فيديو' : 'Image to Video'}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">
                      {language === 'ar' 
                        ? 'حول صورك إلى فيديوهات متحركة'
                        : 'Transform your images into animated videos'
                      }
                    </p>
                  </Link>

                  <Link
                    href="/create/text-to-video"
                    className="group p-6 border-2 border-gray-200 dark:border-gray-700 rounded-xl hover:border-purple-500 dark:hover:border-purple-400 transition-colors"
                  >
                    <DocumentTextIcon className="w-12 h-12 text-blue-600 dark:text-blue-400 mx-auto mb-4 group-hover:scale-110 transition-transform" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      {language === 'ar' ? 'نص إلى فيديو' : 'Text to Video'}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">
                      {language === 'ar' 
                        ? 'أنشئ فيديوهات من النصوص'
                        : 'Create videos from text descriptions'
                      }
                    </p>
                  </Link>

                  <Link
                    href="/create/audio-to-video"
                    className="group p-6 border-2 border-gray-200 dark:border-gray-700 rounded-xl hover:border-purple-500 dark:hover:border-purple-400 transition-colors"
                  >
                    <PlayIcon className="w-12 h-12 text-green-600 dark:text-green-400 mx-auto mb-4 group-hover:scale-110 transition-transform" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      {language === 'ar' ? 'صوت إلى فيديو' : 'Audio to Video'}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">
                      {language === 'ar' 
                        ? 'حول الصوت إلى فيديوهات تفاعلية'
                        : 'Convert audio to interactive videos'
                      }
                    </p>
                  </Link>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'wallet' && (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8">
              <div className="text-center">
                <WalletIcon className="w-16 h-16 text-yellow-600 dark:text-yellow-400 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  {language === 'ar' ? 'محفظة الكوينز' : 'Coins Wallet'}
                </h2>
                <div className="text-4xl font-bold text-yellow-600 dark:text-yellow-400 mb-2">
                  {stats.coinsBalance}
                </div>
                <p className="text-gray-600 dark:text-gray-400 mb-8">
                  {language === 'ar' ? 'كوين متاح' : 'Coins Available'}
                </p>
                
                <button className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white px-8 py-3 rounded-lg hover:shadow-lg transition-all duration-300 transform hover:scale-105">
                  {language === 'ar' ? 'شراء كوينز' : 'Buy Coins'}
                </button>
              </div>
            </div>
          )}

          {activeTab === 'subscriptions' && (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8">
              <div className="text-center">
                <CreditCardIcon className="w-16 h-16 text-blue-600 dark:text-blue-400 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  {language === 'ar' ? 'الاشتراكات' : 'Subscriptions'}
                </h2>
                <p className="text-gray-600 dark:text-gray-400 mb-8">
                  {language === 'ar' 
                    ? 'اختر الخطة المناسبة لك'
                    : 'Choose the plan that suits you'
                  }
                </p>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
                  <div className="border-2 border-gray-200 dark:border-gray-700 rounded-xl p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      {language === 'ar' ? 'مجاني' : 'Free'}
                    </h3>
                    <div className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                      $0<span className="text-sm text-gray-500">/month</span>
                    </div>
                    <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-2">
                      <li>• 5 videos per month</li>
                      <li>• Basic quality</li>
                      <li>• Community support</li>
                    </ul>
                  </div>

                  <div className="border-2 border-purple-500 rounded-xl p-6 relative">
                    <div className="absolute -top-3 left-1/2 transform -translate-x-1/2 bg-purple-500 text-white px-4 py-1 rounded-full text-sm">
                      Popular
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      {language === 'ar' ? 'احترافي' : 'Pro'}
                    </h3>
                    <div className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                      $19<span className="text-sm text-gray-500">/month</span>
                    </div>
                    <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-2">
                      <li>• 50 videos per month</li>
                      <li>• HD quality</li>
                      <li>• Priority support</li>
                      <li>• Advanced features</li>
                    </ul>
                  </div>

                  <div className="border-2 border-gray-200 dark:border-gray-700 rounded-xl p-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      {language === 'ar' ? 'مؤسسي' : 'Enterprise'}
                    </h3>
                    <div className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                      $99<span className="text-sm text-gray-500">/month</span>
                    </div>
                    <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-2">
                      <li>• Unlimited videos</li>
                      <li>• 4K quality</li>
                      <li>• 24/7 support</li>
                      <li>• Custom features</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'comments' && (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8">
              <div className="text-center">
                <ChatBubbleLeftRightIcon className="w-16 h-16 text-green-600 dark:text-green-400 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  {language === 'ar' ? 'التعليقات والتقييمات' : 'Comments & Reviews'}
                </h2>
                <p className="text-gray-600 dark:text-gray-400">
                  {language === 'ar' 
                    ? 'لا توجد تعليقات بعد'
                    : 'No comments yet'
                  }
                </p>
              </div>
            </div>
          )}

          {activeTab === 'settings' && (
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-8">
              <div className="text-center">
                <CogIcon className="w-16 h-16 text-gray-600 dark:text-gray-400 mx-auto mb-4" />
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  {language === 'ar' ? 'الإعدادات' : 'Settings'}
                </h2>
                <p className="text-gray-600 dark:text-gray-400">
                  {language === 'ar' 
                    ? 'إعدادات الحساب والتطبيق'
                    : 'Account and application settings'
                  }
                </p>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}