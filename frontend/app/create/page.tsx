'use client'

import { useState, useRef, useCallback } from 'react'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { useAuth } from '../../contexts/AuthContext'
import { useDropzone } from 'react-dropzone'
import { toast } from 'react-hot-toast'
import { 
  PhotoIcon,
  SpeakerWaveIcon,
  PlayIcon,
  ArrowRightIcon,
  ArrowLeftIcon,
  CloudArrowUpIcon,
  DocumentTextIcon,
  LanguageIcon,
  CogIcon,
  CheckIcon,
  XMarkIcon
} from '@heroicons/react/24/outline'
import { useLanguage } from '../providers'
import Link from 'next/link'
import FileUpload from '@/components/ui/FileUpload'
import BackButton from '@/components/ui/BackButton'
import LanguageSwitcher from '@/components/ui/LanguageSwitcher'
import ThemeSwitcher from '@/components/ui/ThemeSwitcher'

interface VideoSettings {
  quality: 'low' | 'medium' | 'high'
  speed: number
  voice: 'male' | 'female'
  language: string
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

export default function CreatePage() {
  const [currentStep, setCurrentStep] = useState(1)
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [text, setText] = useState('')
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [settings, setSettings] = useState<VideoSettings>({
    quality: 'medium',
    speed: 1.0,
    voice: 'female',
    language: 'ar'
  })
  const [isProcessing, setIsProcessing] = useState(false)
  const [processingStep, setProcessingStep] = useState('')
  const [progress, setProgress] = useState(0)
  
  const { user, loading } = useAuth()
  const router = useRouter()
  const { language, isRTL } = useLanguage()

  const validateStep = (step: number) => {
    switch (step) {
      case 1:
        if (!selectedImage) {
          toast.error(
            language === 'ar' 
              ? 'يرجى اختيار صورة'
              : 'Please select an image'
          )
          return false
        }
        return true
      case 2:
        if (!text.trim()) {
          toast.error(
            language === 'ar' 
              ? 'يرجى إدخال النص'
              : 'Please enter text'
          )
          return false
        }
        if (text.length > 1000) {
          toast.error(
            language === 'ar' 
              ? 'النص طويل جداً (الحد الأقصى 1000 حرف)'
              : 'Text too long (max 1000 characters)'
          )
          return false
        }
        return true
      case 3:
        if (!title.trim()) {
          toast.error(
            language === 'ar' 
              ? 'يرجى إدخال عنوان الفيديو'
              : 'Please enter video title'
          )
          return false
        }
        return true
      default:
        return true
    }
  }

  const nextStep = () => {
    if (validateStep(currentStep)) {
      setCurrentStep(prev => Math.min(prev + 1, 4))
    }
  }

  const prevStep = () => {
    setCurrentStep(prev => Math.max(prev - 1, 1))
  }

  const handleCreateVideo = async () => {
    if (!user) {
      toast.error(
        language === 'ar' 
          ? 'يرجى تسجيل الدخول أولاً'
          : 'Please login first'
      )
      return
    }

    if (!validateStep(3)) return

    setIsProcessing(true)
    setProgress(0)

    try {
      // Step 1: Upload image
      setProcessingStep(
        language === 'ar' 
          ? 'رفع الصورة...'
          : 'Uploading image...'
      )
      setProgress(10)

      const formData = new FormData()
      formData.append('image', selectedImage!)
      formData.append('text', text)
      formData.append('title', title)
      formData.append('description', description)
      formData.append('settings', JSON.stringify(settings))

      const response = await fetch('/api/videos/create', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${user.access_token}`
        },
        body: formData
      })

      if (!response.ok) {
        throw new Error('Failed to create video')
      }

      const data = await response.json()
      const videoId = data.video_id

      // Step 2: Monitor processing
      setProcessingStep(
        language === 'ar' 
          ? 'معالجة الصوت...'
          : 'Processing audio...'
      )
      setProgress(30)

      // Poll for status updates
      const pollStatus = async () => {
        try {
          const statusResponse = await fetch(`/api/videos/${videoId}/status`, {
            headers: {
              'Authorization': `Bearer ${user.access_token}`
            }
          })

          if (statusResponse.ok) {
            const statusData = await statusResponse.json()
            
            switch (statusData.status) {
              case 'processing_audio':
                setProcessingStep(
                  language === 'ar' 
                    ? 'معالجة الصوت...'
                    : 'Processing audio...'
                )
                setProgress(40)
                break
              case 'processing_video':
                setProcessingStep(
                  language === 'ar' 
                    ? 'إنشاء الفيديو...'
                    : 'Creating video...'
                )
                setProgress(70)
                break
              case 'uploading':
                setProcessingStep(
                  language === 'ar' 
                    ? 'رفع الفيديو...'
                    : 'Uploading video...'
                )
                setProgress(90)
                break
              case 'completed':
                setProcessingStep(
                  language === 'ar' 
                    ? 'تم بنجاح!'
                    : 'Completed!'
                )
                setProgress(100)
                
                toast.success(
                  language === 'ar' 
                    ? 'تم إنشاء الفيديو بنجاح!'
                    : 'Video created successfully!'
                )
                
                setTimeout(() => {
                  router.push('/dashboard')
                }, 2000)
                return
              case 'failed':
                throw new Error(statusData.error || 'Video processing failed')
            }
            
            // Continue polling
            setTimeout(pollStatus, 2000)
          }
        } catch (error) {
          console.error('Status polling error:', error)
          setTimeout(pollStatus, 5000) // Retry after 5 seconds
        }
      }

      // Start polling
      setTimeout(pollStatus, 2000)

    } catch (error) {
      console.error('Video creation error:', error)
      toast.error(
        language === 'ar' 
          ? 'فشل في إنشاء الفيديو. حاول مرة أخرى.'
          : 'Failed to create video. Please try again.'
      )
      setIsProcessing(false)
    }
  }

  const supportedLanguages = [
    { code: 'ar', name: language === 'ar' ? 'العربية' : 'Arabic' },
    { code: 'en', name: language === 'ar' ? 'الإنجليزية' : 'English' },
    { code: 'fr', name: language === 'ar' ? 'الفرنسية' : 'French' },
    { code: 'es', name: language === 'ar' ? 'الإسبانية' : 'Spanish' },
    { code: 'de', name: language === 'ar' ? 'الألمانية' : 'German' },
    { code: 'it', name: language === 'ar' ? 'الإيطالية' : 'Italian' }
  ]

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            {language === 'ar' ? 'يرجى تسجيل الدخول' : 'Please Login'}
          </h2>
          <Link href="/auth/login" className="btn-primary">
            {language === 'ar' ? 'تسجيل الدخول' : 'Login'}
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className={`min-h-screen ${isRTL ? 'rtl' : 'ltr'} relative overflow-hidden`}>
      {/* Professional Background Effects */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-forest opacity-20 animate-aurora"></div>
        <div className="absolute top-1/4 left-0 w-96 h-96 bg-gradient-ice rounded-full blur-3xl opacity-15 animate-float"></div>
        <div className="absolute bottom-1/4 right-0 w-80 h-80 bg-gradient-gold rounded-full blur-3xl opacity-15 animate-levitate"></div>
        <div className="absolute inset-0 bg-gray-50/95 dark:bg-gray-900/95 backdrop-blur-sm"></div>
      </div>

      {/* Creative Floating Elements */}
      <div className="fixed inset-0 -z-5 pointer-events-none">
        {[...Array(12)].map((_, i) => (
          <div
            key={i}
            className={`absolute w-2 h-2 bg-gradient-to-r from-accent-400 to-secondary-400 rounded-full opacity-25 animate-cosmic-drift`}
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 6}s`,
              animationDuration: `${10 + Math.random() * 6}s`
            }}
          />
        ))}
      </div>

      {/* Header */}
      <motion.div 
        className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl shadow-lg shadow-accent-500/10 border-b border-gray-200/50 dark:border-gray-700/50"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <motion.div 
              className="flex items-center"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
            >
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <BackButton href="/dashboard" className="mr-4" />
              </motion.div>
              <Link href="/" className="flex items-center space-x-2 mr-8 group">
                <motion.div 
                  className="w-8 h-8 bg-gradient-forest rounded-lg flex items-center justify-center shadow-lg group-hover:shadow-xl group-hover:shadow-accent-500/50 transition-all duration-300"
                  whileHover={{ scale: 1.1, rotate: 5 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <PlayIcon className="w-5 h-5 text-white group-hover:animate-pulse" />
                </motion.div>
                <motion.span 
                  className="text-xl font-bold bg-gradient-forest bg-clip-text text-transparent group-hover:animate-shimmer"
                  whileHover={{ scale: 1.05 }}
                >
                  VEO7
                </motion.span>
              </Link>
              <motion.h1 
                className="text-2xl font-bold bg-gradient-ice bg-clip-text text-transparent"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
              >
                {language === 'ar' ? 'إنشاء فيديو جديد' : 'Create New Video'}
              </motion.h1>
            </motion.div>
            
            <motion.div 
              className="flex items-center space-x-4"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <ThemeSwitcher variant="icon-only" />
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <LanguageSwitcher variant="minimal" />
              </motion.div>
              
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Link href="/dashboard" className="btn-ghost relative overflow-hidden group">
                  <span className="relative z-10">{language === 'ar' ? 'العودة للوحة التحكم' : 'Back to Dashboard'}</span>
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-accent-500/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
                </Link>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </motion.div>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            {[
              { step: 1, title: language === 'ar' ? 'اختيار الصورة' : 'Select Image' },
              { step: 2, title: language === 'ar' ? 'إدخال النص' : 'Enter Text' },
              { step: 3, title: language === 'ar' ? 'تفاصيل الفيديو' : 'Video Details' },
              { step: 4, title: language === 'ar' ? 'المعاينة والإنشاء' : 'Preview & Create' }
            ].map((item, index) => (
              <div key={item.step} className="flex items-center">
                <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${
                  currentStep >= item.step 
                    ? 'bg-primary-600 border-primary-600 text-white' 
                    : 'border-gray-300 text-gray-500'
                }`}>
                  {currentStep > item.step ? (
                    <CheckIcon className="w-6 h-6" />
                  ) : (
                    <span className="text-sm font-medium">{item.step}</span>
                  )}
                </div>
                <div className="ml-3">
                  <p className={`text-sm font-medium ${
                    currentStep >= item.step ? 'text-primary-600' : 'text-gray-500'
                  }`}>
                    {item.title}
                  </p>
                </div>
                {index < 3 && (
                  <div className={`flex-1 h-0.5 mx-4 ${
                    currentStep > item.step ? 'bg-primary-600' : 'bg-gray-300'
                  }`} />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Step Content */}
        <motion.div
          key={currentStep}
          variants={fadeInUp}
          initial="initial"
          animate="animate"
          className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8"
        >
          {/* Step 1: Image Selection */}
          {currentStep === 1 && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                {language === 'ar' ? 'اختر صورة الوجه' : 'Select Face Image'}
              </h2>
              
              <FileUpload
                 onFileSelect={(file) => {
                   setSelectedImage(file)
                   const reader = new FileReader()
                   reader.onload = (e) => {
                     setImagePreview(e.target?.result as string)
                   }
                   reader.readAsDataURL(file)
                 }}
                 onFileRemove={() => {
                   setSelectedImage(null)
                   setImagePreview(null)
                 }}
                 selectedFile={selectedImage}
                 filePreview={imagePreview}
                 acceptedTypes={{
                   'image/*': ['.jpeg', '.jpg', '.png', '.webp', '.gif']
                 }}
                 maxSize={10 * 1024 * 1024}
                 className="mb-6"
                 language={language}
               />
            </div>
          )}

          {/* Step 2: Text Input */}
          {currentStep === 2 && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                {language === 'ar' ? 'أدخل النص المراد تحويله لصوت' : 'Enter Text for Speech'}
              </h2>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    {language === 'ar' ? 'النص' : 'Text'}
                  </label>
                  <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    rows={8}
                    className="input-primary resize-none"
                    placeholder={
                      language === 'ar' 
                        ? 'اكتب النص الذي تريد تحويله إلى صوت...'
                        : 'Write the text you want to convert to speech...'
                    }
                    maxLength={1000}
                  />
                  <div className="flex justify-between mt-2 text-sm text-gray-500">
                    <span>
                      {language === 'ar' 
                        ? `${text.length} / 1000 حرف`
                        : `${text.length} / 1000 characters`
                      }
                    </span>
                    <span>
                      {language === 'ar' 
                        ? `تقريباً ${Math.ceil(text.length / 150)} ثانية`
                        : `~${Math.ceil(text.length / 150)} seconds`
                      }
                    </span>
                  </div>
                </div>

                {/* Voice Settings */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      {language === 'ar' ? 'اللغة' : 'Language'}
                    </label>
                    <select
                      value={settings.language}
                      onChange={(e) => setSettings(prev => ({ ...prev, language: e.target.value }))}
                      className="input-primary"
                    >
                      {supportedLanguages.map(lang => (
                        <option key={lang.code} value={lang.code}>
                          {lang.name}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      {language === 'ar' ? 'نوع الصوت' : 'Voice Type'}
                    </label>
                    <select
                      value={settings.voice}
                      onChange={(e) => setSettings(prev => ({ ...prev, voice: e.target.value as 'male' | 'female' }))}
                      className="input-primary"
                    >
                      <option value="female">
                        {language === 'ar' ? 'أنثى' : 'Female'}
                      </option>
                      <option value="male">
                        {language === 'ar' ? 'ذكر' : 'Male'}
                      </option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    {language === 'ar' ? `سرعة الصوت: ${settings.speed}x` : `Speech Speed: ${settings.speed}x`}
                  </label>
                  <input
                    type="range"
                    min="0.5"
                    max="2.0"
                    step="0.1"
                    value={settings.speed}
                    onChange={(e) => setSettings(prev => ({ ...prev, speed: parseFloat(e.target.value) }))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
                  />
                  <div className="flex justify-between text-xs text-gray-500 mt-1">
                    <span>0.5x</span>
                    <span>1.0x</span>
                    <span>2.0x</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Step 3: Video Details */}
          {currentStep === 3 && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                {language === 'ar' ? 'تفاصيل الفيديو' : 'Video Details'}
              </h2>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    {language === 'ar' ? 'عنوان الفيديو' : 'Video Title'}
                  </label>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="input-primary"
                    placeholder={
                      language === 'ar' 
                        ? 'أدخل عنوان الفيديو...'
                        : 'Enter video title...'
                    }
                    maxLength={100}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    {language === 'ar' ? 'وصف الفيديو (اختياري)' : 'Video Description (Optional)'}
                  </label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={4}
                    className="input-primary resize-none"
                    placeholder={
                      language === 'ar' 
                        ? 'أدخل وصف الفيديو...'
                        : 'Enter video description...'
                    }
                    maxLength={500}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    {language === 'ar' ? 'جودة الفيديو' : 'Video Quality'}
                  </label>
                  <div className="grid grid-cols-3 gap-4">
                    {[
                      { value: 'low', label: language === 'ar' ? 'منخفضة' : 'Low', desc: '480p' },
                      { value: 'medium', label: language === 'ar' ? 'متوسطة' : 'Medium', desc: '720p' },
                      { value: 'high', label: language === 'ar' ? 'عالية' : 'High', desc: '1080p' }
                    ].map(quality => (
                      <button
                        key={quality.value}
                        onClick={() => setSettings(prev => ({ ...prev, quality: quality.value as any }))}
                        className={`p-4 rounded-lg border-2 text-center transition-colors ${
                          settings.quality === quality.value
                            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                            : 'border-gray-300 dark:border-gray-600 hover:border-primary-300'
                        }`}
                      >
                        <div className="font-medium text-gray-900 dark:text-white">
                          {quality.label}
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400">
                          {quality.desc}
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Step 4: Preview & Create */}
          {currentStep === 4 && (
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                {language === 'ar' ? 'المعاينة والإنشاء' : 'Preview & Create'}
              </h2>
              
              {!isProcessing ? (
                <div className="space-y-6">
                  {/* Preview */}
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
                        {language === 'ar' ? 'الصورة المختارة' : 'Selected Image'}
                      </h3>
                      <img
                        src={imagePreview!}
                        alt="Preview"
                        className="w-full rounded-lg shadow-lg"
                      />
                    </div>
                    
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">
                        {language === 'ar' ? 'تفاصيل الفيديو' : 'Video Details'}
                      </h3>
                      <div className="space-y-4">
                        <div>
                          <span className="text-sm font-medium text-gray-500 dark:text-gray-400">
                            {language === 'ar' ? 'العنوان:' : 'Title:'}
                          </span>
                          <p className="text-gray-900 dark:text-white">{title}</p>
                        </div>
                        
                        {description && (
                          <div>
                            <span className="text-sm font-medium text-gray-500 dark:text-gray-400">
                              {language === 'ar' ? 'الوصف:' : 'Description:'}
                            </span>
                            <p className="text-gray-900 dark:text-white">{description}</p>
                          </div>
                        )}
                        
                        <div>
                          <span className="text-sm font-medium text-gray-500 dark:text-gray-400">
                            {language === 'ar' ? 'النص:' : 'Text:'}
                          </span>
                          <p className="text-gray-900 dark:text-white line-clamp-4">{text}</p>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <span className="text-gray-500 dark:text-gray-400">
                              {language === 'ar' ? 'الجودة:' : 'Quality:'}
                            </span>
                            <p className="text-gray-900 dark:text-white capitalize">{settings.quality}</p>
                          </div>
                          <div>
                            <span className="text-gray-500 dark:text-gray-400">
                              {language === 'ar' ? 'اللغة:' : 'Language:'}
                            </span>
                            <p className="text-gray-900 dark:text-white">
                              {supportedLanguages.find(l => l.code === settings.language)?.name}
                            </p>
                          </div>
                          <div>
                            <span className="text-gray-500 dark:text-gray-400">
                              {language === 'ar' ? 'نوع الصوت:' : 'Voice:'}
                            </span>
                            <p className="text-gray-900 dark:text-white capitalize">{settings.voice}</p>
                          </div>
                          <div>
                            <span className="text-gray-500 dark:text-gray-400">
                              {language === 'ar' ? 'السرعة:' : 'Speed:'}
                            </span>
                            <p className="text-gray-900 dark:text-white">{settings.speed}x</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Create Button */}
                  <div className="text-center">
                    <button
                      onClick={handleCreateVideo}
                      className="btn-primary px-8 py-4 text-lg"
                    >
                      <PlayIcon className="w-6 h-6 mr-2" />
                      {language === 'ar' ? 'إنشاء الفيديو' : 'Create Video'}
                    </button>
                  </div>
                </div>
              ) : (
                /* Processing State */
                <div className="text-center py-12">
                  <div className="w-24 h-24 mx-auto mb-6">
                    <div className="relative">
                      <div className="w-24 h-24 border-4 border-gray-200 rounded-full"></div>
                      <div 
                        className="absolute top-0 left-0 w-24 h-24 border-4 border-primary-600 rounded-full animate-spin"
                        style={{
                          borderRightColor: 'transparent',
                          transform: `rotate(${progress * 3.6}deg)`
                        }}
                      ></div>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-lg font-bold text-primary-600">{progress}%</span>
                      </div>
                    </div>
                  </div>
                  
                  <h3 className="text-xl font-medium text-gray-900 dark:text-white mb-2">
                    {language === 'ar' ? 'جاري إنشاء الفيديو...' : 'Creating Video...'}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-6">
                    {processingStep}
                  </p>
                  
                  <div className="max-w-md mx-auto bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                      className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${progress}%` }}
                    ></div>
                  </div>
                  
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-4">
                    {language === 'ar' 
                      ? 'هذا قد يستغرق بضع دقائق. لا تغلق هذه الصفحة.'
                      : 'This may take a few minutes. Please do not close this page.'
                    }
                  </p>
                </div>
              )}
            </div>
          )}
        </motion.div>

        {/* Navigation Buttons */}
        {!isProcessing && (
          <div className="flex justify-between mt-8">
            <button
              onClick={prevStep}
              disabled={currentStep === 1}
              className="btn-ghost flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isRTL ? <ArrowRightIcon className="w-5 h-5" /> : <ArrowLeftIcon className="w-5 h-5" />}
              <span>{language === 'ar' ? 'السابق' : 'Previous'}</span>
            </button>
            
            {currentStep < 4 ? (
              <button
                onClick={nextStep}
                className="btn-primary flex items-center space-x-2"
              >
                <span>{language === 'ar' ? 'التالي' : 'Next'}</span>
                {isRTL ? <ArrowLeftIcon className="w-5 h-5" /> : <ArrowRightIcon className="w-5 h-5" />}
              </button>
            ) : null}
          </div>
        )}
      </div>
    </div>
  )
}