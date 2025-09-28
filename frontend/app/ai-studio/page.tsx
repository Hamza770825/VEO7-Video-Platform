'use client'

import { useState, useRef } from 'react'
import { motion } from 'framer-motion'
import { useAuth } from '../../contexts/AuthContext'
import { useLanguage } from '../providers'
import { toast } from 'react-hot-toast'
import { 
  PhotoIcon,
  SpeakerWaveIcon,
  VideoCameraIcon,
  SparklesIcon,
  ArrowUpTrayIcon,
  PlayIcon,
  StopIcon,
  CheckIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline'
import BackButton from '@/components/ui/BackButton'
import LanguageSwitcher from '@/components/ui/LanguageSwitcher'
import ThemeSwitcher from '@/components/ui/ThemeSwitcher'

interface AIModelStatus {
  sadtalker: boolean
  wav2lip: boolean
  realesrgan: boolean
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

export default function AIStudioPage() {
  const [activeTab, setActiveTab] = useState<'sadtalker' | 'wav2lip' | 'enhance'>('sadtalker')
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState(0)
  const [processingStep, setProcessingStep] = useState('')
  const [modelStatus, setModelStatus] = useState<AIModelStatus>({
    sadtalker: false,
    wav2lip: false,
    realesrgan: false
  })
  
  // SadTalker states
  const [sadtalkerImage, setSadtalkerImage] = useState<File | null>(null)
  const [sadtalkerAudio, setSadtalkerAudio] = useState<File | null>(null)
  const [sadtalkerImagePreview, setSadtalkerImagePreview] = useState<string | null>(null)
  const [sadtalkerQuality, setSadtalkerQuality] = useState<'low' | 'medium' | 'high'>('medium')
  
  // Wav2Lip states
  const [wav2lipVideo, setWav2lipVideo] = useState<File | null>(null)
  const [wav2lipAudio, setWav2lipAudio] = useState<File | null>(null)
  const [wav2lipVideoPreview, setWav2lipVideoPreview] = useState<string | null>(null)
  const [wav2lipQuality, setWav2lipQuality] = useState<'low' | 'medium' | 'high'>('medium')
  
  // Image Enhancement states
  const [enhanceImage, setEnhanceImage] = useState<File | null>(null)
  const [enhanceImagePreview, setEnhanceImagePreview] = useState<string | null>(null)
  const [enhanceScale, setEnhanceScale] = useState<number>(2)
  
  const { user, loading } = useAuth()
  const { language, isRTL } = useLanguage()
  
  const imageInputRef = useRef<HTMLInputElement>(null)
  const audioInputRef = useRef<HTMLInputElement>(null)
  const videoInputRef = useRef<HTMLInputElement>(null)
  const enhanceInputRef = useRef<HTMLInputElement>(null)

  // Check AI models status
  const checkModelsStatus = async () => {
    try {
      const response = await fetch('/api/ai-models/status', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        setModelStatus(data.status)
      }
    } catch (error) {
      console.error('Error checking models status:', error)
    }
  }

  // Initialize AI models
  const initializeModels = async () => {
    if (!user || user.role !== 'admin') {
      toast.error(
        language === 'ar' 
          ? 'يتطلب صلاحيات المدير لتهيئة النماذج'
          : 'Admin privileges required to initialize models'
      )
      return
    }

    try {
      setIsProcessing(true)
      setProcessingStep(
        language === 'ar' 
          ? 'تهيئة نماذج الذكاء الاصطناعي...'
          : 'Initializing AI models...'
      )

      const response = await fetch('/api/ai-models/initialize', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        toast.success(
          language === 'ar' 
            ? 'تم تهيئة النماذج بنجاح'
            : 'Models initialized successfully'
        )
        await checkModelsStatus()
      } else {
        throw new Error('Failed to initialize models')
      }
    } catch (error) {
      toast.error(
        language === 'ar' 
          ? 'فشل في تهيئة النماذج'
          : 'Failed to initialize models'
      )
    } finally {
      setIsProcessing(false)
      setProcessingStep('')
    }
  }

  // Handle file uploads
  const handleImageUpload = (file: File, type: 'sadtalker' | 'enhance') => {
    if (type === 'sadtalker') {
      setSadtalkerImage(file)
      const reader = new FileReader()
      reader.onload = (e) => setSadtalkerImagePreview(e.target?.result as string)
      reader.readAsDataURL(file)
    } else {
      setEnhanceImage(file)
      const reader = new FileReader()
      reader.onload = (e) => setEnhanceImagePreview(e.target?.result as string)
      reader.readAsDataURL(file)
    }
  }

  const handleAudioUpload = (file: File, type: 'sadtalker' | 'wav2lip') => {
    if (type === 'sadtalker') {
      setSadtalkerAudio(file)
    } else {
      setWav2lipAudio(file)
    }
  }

  const handleVideoUpload = (file: File) => {
    setWav2lipVideo(file)
    const reader = new FileReader()
    reader.onload = (e) => setWav2lipVideoPreview(e.target?.result as string)
    reader.readAsDataURL(file)
  }

  // Generate SadTalker video
  const generateSadTalkerVideo = async () => {
    if (!sadtalkerImage || !sadtalkerAudio) {
      toast.error(
        language === 'ar' 
          ? 'يرجى رفع الصورة والصوت'
          : 'Please upload image and audio'
      )
      return
    }

    try {
      setIsProcessing(true)
      setProgress(0)
      setProcessingStep(
        language === 'ar' 
          ? 'توليد فيديو SadTalker...'
          : 'Generating SadTalker video...'
      )

      const formData = new FormData()
      formData.append('image', sadtalkerImage)
      formData.append('audio', sadtalkerAudio)
      formData.append('quality', sadtalkerQuality)

      const response = await fetch('/api/ai-models/generate-sadtalker', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `sadtalker_video_${Date.now()}.mp4`
        a.click()
        
        toast.success(
          language === 'ar' 
            ? 'تم توليد الفيديو بنجاح'
            : 'Video generated successfully'
        )
      } else {
        throw new Error('Failed to generate video')
      }
    } catch (error) {
      toast.error(
        language === 'ar' 
          ? 'فشل في توليد الفيديو'
          : 'Failed to generate video'
      )
    } finally {
      setIsProcessing(false)
      setProgress(0)
      setProcessingStep('')
    }
  }

  // Generate Wav2Lip video
  const generateWav2LipVideo = async () => {
    if (!wav2lipVideo || !wav2lipAudio) {
      toast.error(
        language === 'ar' 
          ? 'يرجى رفع الفيديو والصوت'
          : 'Please upload video and audio'
      )
      return
    }

    try {
      setIsProcessing(true)
      setProgress(0)
      setProcessingStep(
        language === 'ar' 
          ? 'مزامنة حركة الشفاه...'
          : 'Synchronizing lip movement...'
      )

      const formData = new FormData()
      formData.append('video', wav2lipVideo)
      formData.append('audio', wav2lipAudio)
      formData.append('quality', wav2lipQuality)

      const response = await fetch('/api/ai-models/generate-wav2lip', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `wav2lip_video_${Date.now()}.mp4`
        a.click()
        
        toast.success(
          language === 'ar' 
            ? 'تم مزامنة الفيديو بنجاح'
            : 'Video synchronized successfully'
        )
      } else {
        throw new Error('Failed to synchronize video')
      }
    } catch (error) {
      toast.error(
        language === 'ar' 
          ? 'فشل في مزامنة الفيديو'
          : 'Failed to synchronize video'
      )
    } finally {
      setIsProcessing(false)
      setProgress(0)
      setProcessingStep('')
    }
  }

  // Enhance image quality
  const enhanceImageQuality = async () => {
    if (!enhanceImage) {
      toast.error(
        language === 'ar' 
          ? 'يرجى رفع صورة'
          : 'Please upload an image'
      )
      return
    }

    try {
      setIsProcessing(true)
      setProgress(0)
      setProcessingStep(
        language === 'ar' 
          ? 'تحسين جودة الصورة...'
          : 'Enhancing image quality...'
      )

      const formData = new FormData()
      formData.append('file', enhanceImage)
      formData.append('scale', enhanceScale.toString())

      const response = await fetch('/api/ai-models/enhance-image', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: formData
      })

      if (response.ok) {
        const blob = await response.blob()
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `enhanced_${enhanceImage.name}`
        a.click()
        
        toast.success(
          language === 'ar' 
            ? 'تم تحسين الصورة بنجاح'
            : 'Image enhanced successfully'
        )
      } else {
        throw new Error('Failed to enhance image')
      }
    } catch (error) {
      toast.error(
        language === 'ar' 
          ? 'فشل في تحسين الصورة'
          : 'Failed to enhance image'
      )
    } finally {
      setIsProcessing(false)
      setProgress(0)
      setProcessingStep('')
    }
  }

  const tabs = [
    {
      id: 'sadtalker',
      name: language === 'ar' ? 'SadTalker' : 'SadTalker',
      description: language === 'ar' ? 'توليد فيديو من صورة وصوت' : 'Generate video from image and audio',
      icon: VideoCameraIcon
    },
    {
      id: 'wav2lip',
      name: language === 'ar' ? 'Wav2Lip' : 'Wav2Lip',
      description: language === 'ar' ? 'مزامنة حركة الشفاه' : 'Lip sync video',
      icon: SpeakerWaveIcon
    },
    {
      id: 'enhance',
      name: language === 'ar' ? 'تحسين الصور' : 'Image Enhancement',
      description: language === 'ar' ? 'تحسين جودة الصور بالذكاء الاصطناعي' : 'AI-powered image enhancement',
      icon: SparklesIcon
    }
  ]

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">
            {language === 'ar' ? 'يرجى تسجيل الدخول' : 'Please Login'}
          </h1>
          <p className="text-gray-600 mb-8">
            {language === 'ar' 
              ? 'تحتاج إلى تسجيل الدخول للوصول إلى استوديو الذكاء الاصطناعي'
              : 'You need to login to access AI Studio'
            }
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className={`min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 ${isRTL ? 'rtl' : 'ltr'}`}>
      {/* Header */}
      <div className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4 rtl:space-x-reverse">
              <BackButton />
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  {language === 'ar' ? 'استوديو الذكاء الاصطناعي' : 'AI Studio'}
                </h1>
                <p className="text-sm text-gray-600">
                  {language === 'ar' 
                    ? 'أدوات متقدمة لتوليد وتحسين المحتوى'
                    : 'Advanced tools for content generation and enhancement'
                  }
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4 rtl:space-x-reverse">
              <LanguageSwitcher />
              <ThemeSwitcher />
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Models Status */}
        <motion.div
          initial="initial"
          animate="animate"
          variants={fadeInUp}
          className="mb-8"
        >
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">
                {language === 'ar' ? 'حالة النماذج' : 'Models Status'}
              </h2>
              {user?.role === 'admin' && (
                <button
                  onClick={initializeModels}
                  disabled={isProcessing}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {language === 'ar' ? 'تهيئة النماذج' : 'Initialize Models'}
                </button>
              )}
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {Object.entries(modelStatus).map(([model, status]) => (
                <div key={model} className="flex items-center space-x-3 rtl:space-x-reverse">
                  <div className={`w-3 h-3 rounded-full ${status ? 'bg-green-500' : 'bg-red-500'}`} />
                  <span className="text-sm font-medium text-gray-700 capitalize">
                    {model}
                  </span>
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    status 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {status 
                      ? (language === 'ar' ? 'متاح' : 'Available')
                      : (language === 'ar' ? 'غير متاح' : 'Unavailable')
                    }
                  </span>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Tabs */}
        <motion.div
          initial="initial"
          animate="animate"
          variants={staggerChildren}
          className="mb-8"
        >
          <div className="flex space-x-1 rtl:space-x-reverse bg-gray-100 p-1 rounded-xl">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex-1 flex items-center justify-center space-x-2 rtl:space-x-reverse px-4 py-3 rounded-lg transition-all ${
                  activeTab === tab.id
                    ? 'bg-white text-blue-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                <div className="text-left rtl:text-right">
                  <div className="font-medium">{tab.name}</div>
                  <div className="text-xs opacity-75">{tab.description}</div>
                </div>
              </button>
            ))}
          </div>
        </motion.div>

        {/* Content */}
        <motion.div
          key={activeTab}
          initial="initial"
          animate="animate"
          variants={fadeInUp}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
        >
          {/* SadTalker Tab */}
          {activeTab === 'sadtalker' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {language === 'ar' ? 'توليد فيديو SadTalker' : 'SadTalker Video Generation'}
                </h3>
                <p className="text-gray-600">
                  {language === 'ar' 
                    ? 'قم برفع صورة وملف صوتي لتوليد فيديو متحرك'
                    : 'Upload an image and audio file to generate an animated video'
                  }
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Image Upload */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === 'ar' ? 'الصورة' : 'Image'}
                  </label>
                  <div
                    onClick={() => imageInputRef.current?.click()}
                    className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-500 transition-colors"
                  >
                    {sadtalkerImagePreview ? (
                      <img
                        src={sadtalkerImagePreview}
                        alt="Preview"
                        className="max-w-full h-32 object-cover mx-auto rounded"
                      />
                    ) : (
                      <div>
                        <PhotoIcon className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                        <p className="text-gray-600">
                          {language === 'ar' ? 'انقر لرفع صورة' : 'Click to upload image'}
                        </p>
                      </div>
                    )}
                  </div>
                  <input
                    ref={imageInputRef}
                    type="file"
                    accept="image/*"
                    onChange={(e) => e.target.files?.[0] && handleImageUpload(e.target.files[0], 'sadtalker')}
                    className="hidden"
                  />
                </div>

                {/* Audio Upload */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === 'ar' ? 'الصوت' : 'Audio'}
                  </label>
                  <div
                    onClick={() => audioInputRef.current?.click()}
                    className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-500 transition-colors"
                  >
                    {sadtalkerAudio ? (
                      <div>
                        <SpeakerWaveIcon className="w-12 h-12 text-blue-500 mx-auto mb-2" />
                        <p className="text-gray-900 font-medium">{sadtalkerAudio.name}</p>
                        <p className="text-gray-600 text-sm">
                          {(sadtalkerAudio.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                      </div>
                    ) : (
                      <div>
                        <SpeakerWaveIcon className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                        <p className="text-gray-600">
                          {language === 'ar' ? 'انقر لرفع ملف صوتي' : 'Click to upload audio'}
                        </p>
                      </div>
                    )}
                  </div>
                  <input
                    ref={audioInputRef}
                    type="file"
                    accept="audio/*"
                    onChange={(e) => e.target.files?.[0] && handleAudioUpload(e.target.files[0], 'sadtalker')}
                    className="hidden"
                  />
                </div>
              </div>

              {/* Quality Settings */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {language === 'ar' ? 'جودة الفيديو' : 'Video Quality'}
                </label>
                <select
                  value={sadtalkerQuality}
                  onChange={(e) => setSadtalkerQuality(e.target.value as any)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="low">{language === 'ar' ? 'منخفضة' : 'Low'}</option>
                  <option value="medium">{language === 'ar' ? 'متوسطة' : 'Medium'}</option>
                  <option value="high">{language === 'ar' ? 'عالية' : 'High'}</option>
                </select>
              </div>

              {/* Generate Button */}
              <button
                onClick={generateSadTalkerVideo}
                disabled={!sadtalkerImage || !sadtalkerAudio || isProcessing}
                className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 rtl:space-x-reverse"
              >
                {isProcessing ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>{processingStep}</span>
                  </>
                ) : (
                  <>
                    <PlayIcon className="w-5 h-5" />
                    <span>
                      {language === 'ar' ? 'توليد الفيديو' : 'Generate Video'}
                    </span>
                  </>
                )}
              </button>
            </div>
          )}

          {/* Wav2Lip Tab */}
          {activeTab === 'wav2lip' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {language === 'ar' ? 'مزامنة حركة الشفاه' : 'Lip Sync with Wav2Lip'}
                </h3>
                <p className="text-gray-600">
                  {language === 'ar' 
                    ? 'قم برفع فيديو وملف صوتي لمزامنة حركة الشفاه'
                    : 'Upload a video and audio file to synchronize lip movement'
                  }
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Video Upload */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === 'ar' ? 'الفيديو' : 'Video'}
                  </label>
                  <div
                    onClick={() => videoInputRef.current?.click()}
                    className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-500 transition-colors"
                  >
                    {wav2lipVideoPreview ? (
                      <video
                        src={wav2lipVideoPreview}
                        className="max-w-full h-32 object-cover mx-auto rounded"
                        controls
                      />
                    ) : (
                      <div>
                        <VideoCameraIcon className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                        <p className="text-gray-600">
                          {language === 'ar' ? 'انقر لرفع فيديو' : 'Click to upload video'}
                        </p>
                      </div>
                    )}
                  </div>
                  <input
                    ref={videoInputRef}
                    type="file"
                    accept="video/*"
                    onChange={(e) => e.target.files?.[0] && handleVideoUpload(e.target.files[0])}
                    className="hidden"
                  />
                </div>

                {/* Audio Upload */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    {language === 'ar' ? 'الصوت الجديد' : 'New Audio'}
                  </label>
                  <div
                    onClick={() => audioInputRef.current?.click()}
                    className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-500 transition-colors"
                  >
                    {wav2lipAudio ? (
                      <div>
                        <SpeakerWaveIcon className="w-12 h-12 text-blue-500 mx-auto mb-2" />
                        <p className="text-gray-900 font-medium">{wav2lipAudio.name}</p>
                        <p className="text-gray-600 text-sm">
                          {(wav2lipAudio.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                      </div>
                    ) : (
                      <div>
                        <SpeakerWaveIcon className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                        <p className="text-gray-600">
                          {language === 'ar' ? 'انقر لرفع ملف صوتي' : 'Click to upload audio'}
                        </p>
                      </div>
                    )}
                  </div>
                  <input
                    ref={audioInputRef}
                    type="file"
                    accept="audio/*"
                    onChange={(e) => e.target.files?.[0] && handleAudioUpload(e.target.files[0], 'wav2lip')}
                    className="hidden"
                  />
                </div>
              </div>

              {/* Quality Settings */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {language === 'ar' ? 'جودة المعالجة' : 'Processing Quality'}
                </label>
                <select
                  value={wav2lipQuality}
                  onChange={(e) => setWav2lipQuality(e.target.value as any)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="low">{language === 'ar' ? 'منخفضة' : 'Low'}</option>
                  <option value="medium">{language === 'ar' ? 'متوسطة' : 'Medium'}</option>
                  <option value="high">{language === 'ar' ? 'عالية' : 'High'}</option>
                </select>
              </div>

              {/* Generate Button */}
              <button
                onClick={generateWav2LipVideo}
                disabled={!wav2lipVideo || !wav2lipAudio || isProcessing}
                className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 rtl:space-x-reverse"
              >
                {isProcessing ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>{processingStep}</span>
                  </>
                ) : (
                  <>
                    <SpeakerWaveIcon className="w-5 h-5" />
                    <span>
                      {language === 'ar' ? 'مزامنة الفيديو' : 'Sync Video'}
                    </span>
                  </>
                )}
              </button>
            </div>
          )}

          {/* Image Enhancement Tab */}
          {activeTab === 'enhance' && (
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {language === 'ar' ? 'تحسين جودة الصور' : 'Image Quality Enhancement'}
                </h3>
                <p className="text-gray-600">
                  {language === 'ar' 
                    ? 'استخدم Real-ESRGAN لتحسين جودة ودقة الصور'
                    : 'Use Real-ESRGAN to enhance image quality and resolution'
                  }
                </p>
              </div>

              {/* Image Upload */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {language === 'ar' ? 'الصورة' : 'Image'}
                </label>
                <div
                  onClick={() => enhanceInputRef.current?.click()}
                  className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-500 transition-colors"
                >
                  {enhanceImagePreview ? (
                    <img
                      src={enhanceImagePreview}
                      alt="Preview"
                      className="max-w-full h-48 object-cover mx-auto rounded"
                    />
                  ) : (
                    <div>
                      <PhotoIcon className="w-12 h-12 text-gray-400 mx-auto mb-2" />
                      <p className="text-gray-600">
                        {language === 'ar' ? 'انقر لرفع صورة' : 'Click to upload image'}
                      </p>
                    </div>
                  )}
                </div>
                <input
                  ref={enhanceInputRef}
                  type="file"
                  accept="image/*"
                  onChange={(e) => e.target.files?.[0] && handleImageUpload(e.target.files[0], 'enhance')}
                  className="hidden"
                />
              </div>

              {/* Scale Settings */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {language === 'ar' ? 'معامل التكبير' : 'Scale Factor'}
                </label>
                <select
                  value={enhanceScale}
                  onChange={(e) => setEnhanceScale(parseInt(e.target.value))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value={2}>2x</option>
                  <option value={4}>4x</option>
                  <option value={8}>8x</option>
                </select>
                <p className="text-sm text-gray-600 mt-1">
                  {language === 'ar' 
                    ? 'كلما زاد المعامل، زادت الجودة ووقت المعالجة'
                    : 'Higher scale means better quality but longer processing time'
                  }
                </p>
              </div>

              {/* Enhance Button */}
              <button
                onClick={enhanceImageQuality}
                disabled={!enhanceImage || isProcessing}
                className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 rtl:space-x-reverse"
              >
                {isProcessing ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>{processingStep}</span>
                  </>
                ) : (
                  <>
                    <SparklesIcon className="w-5 h-5" />
                    <span>
                      {language === 'ar' ? 'تحسين الصورة' : 'Enhance Image'}
                    </span>
                  </>
                )}
              </button>
            </div>
          )}
        </motion.div>

        {/* Info Section */}
        <motion.div
          initial="initial"
          animate="animate"
          variants={fadeInUp}
          className="mt-8"
        >
          <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
            <div className="flex items-start space-x-3 rtl:space-x-reverse">
              <InformationCircleIcon className="w-6 h-6 text-blue-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="text-lg font-semibold text-blue-900 mb-2">
                  {language === 'ar' ? 'معلومات مهمة' : 'Important Information'}
                </h3>
                <ul className="space-y-2 text-blue-800">
                  <li>
                    {language === 'ar' 
                      ? '• تأكد من أن النماذج متاحة قبل البدء في المعالجة'
                      : '• Make sure models are available before starting processing'
                    }
                  </li>
                  <li>
                    {language === 'ar' 
                      ? '• قد تستغرق المعالجة وقتاً طويلاً حسب حجم الملفات وجودة المعالجة'
                      : '• Processing may take time depending on file size and quality settings'
                    }
                  </li>
                  <li>
                    {language === 'ar' 
                      ? '• يُنصح باستخدام ملفات صغيرة الحجم للحصول على نتائج أسرع'
                      : '• Use smaller files for faster results'
                    }
                  </li>
                  <li>
                    {language === 'ar' 
                      ? '• تحتاج صلاحيات المدير لتهيئة النماذج'
                      : '• Admin privileges required to initialize models'
                    }
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}