'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { useAuth } from '../contexts/AuthContext'
import Link from 'next/link'
import Image from 'next/image'
import { 
  PlayIcon, 
  SparklesIcon, 
  CameraIcon, 
  SpeakerWaveIcon,
  ArrowRightIcon,
  CheckIcon,
  StarIcon,
  UserGroupIcon,
  ClockIcon,
  ShieldCheckIcon,
  GlobeAltIcon,
  ChevronRightIcon,
  Bars3Icon,
  XMarkIcon,
  PhotoIcon,
  VideoCameraIcon,
  MicrophoneIcon,
  DocumentTextIcon
} from '@heroicons/react/24/outline'
import { useLanguage } from './providers'
import PricingSection from '../components/ui/pricing-section'

// Animation variants
const fadeInUp = {
  initial: { opacity: 0, y: 60 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6, ease: 'easeOut' }
}

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
}

const scaleIn = {
  initial: { opacity: 0, scale: 0.8 },
  animate: { opacity: 1, scale: 1 },
  transition: { duration: 0.5, ease: 'easeOut' }
}

export default function HomePage() {
  const { user, loading } = useAuth()
  const router = useRouter()
  const { language, isRTL } = useLanguage()
  const [isLoaded, setIsLoaded] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  useEffect(() => {
    setIsLoaded(true)
  }, [])

  const videoTypes = [
    {
      icon: PhotoIcon,
      title: language === 'ar' ? 'صورة إلى فيديو' : 'Image to Video',
      description: language === 'ar' 
        ? 'حول صورك الثابتة إلى فيديوهات متحركة مذهلة'
        : 'Transform your static images into stunning animated videos',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      icon: DocumentTextIcon,
      title: language === 'ar' ? 'نص إلى فيديو' : 'Text to Video',
      description: language === 'ar'
        ? 'أنشئ فيديوهات احترافية من النصوص فقط'
        : 'Create professional videos from text descriptions only',
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      icon: MicrophoneIcon,
      title: language === 'ar' ? 'صوت إلى فيديو' : 'Audio to Video',
      description: language === 'ar'
        ? 'حول التسجيلات الصوتية إلى فيديوهات تفاعلية'
        : 'Convert audio recordings into interactive videos',
      gradient: 'from-green-500 to-emerald-500'
    },
    {
      icon: SparklesIcon,
      title: language === 'ar' ? 'تأثيرات الذكاء الاصطناعي' : 'AI Video Effects',
      description: language === 'ar'
        ? 'أضف تأثيرات بصرية متقدمة بالذكاء الاصطناعي'
        : 'Add advanced visual effects with AI technology',
      gradient: 'from-orange-500 to-red-500'
    }
  ]

  const features = [
    {
      title: language === 'ar' ? 'جودة سينمائية' : 'Cinematic Quality',
      description: language === 'ar' 
        ? 'فيديوهات عالية الدقة تصل إلى 4K مع جودة احترافية'
        : 'High-definition videos up to 4K with professional quality'
    },
    {
      title: language === 'ar' ? 'سرعة فائقة' : 'Lightning Fast',
      description: language === 'ar'
        ? 'إنتاج الفيديوهات في ثوانٍ معدودة'
        : 'Generate videos in just seconds'
    },
    {
      title: language === 'ar' ? 'سهولة الاستخدام' : 'Easy to Use',
      description: language === 'ar'
        ? 'واجهة بسيطة ومناسبة لجميع المستخدمين'
        : 'Simple interface suitable for all users'
    }
  ]

  const stats = [
    { number: '1M+', label: language === 'ar' ? 'فيديو تم إنتاجه' : 'Videos Generated' },
    { number: '50K+', label: language === 'ar' ? 'مستخدم نشط' : 'Active Users' },
    { number: '99.9%', label: language === 'ar' ? 'معدل النجاح' : 'Success Rate' },
    { number: '4.9/5', label: language === 'ar' ? 'تقييم المستخدمين' : 'User Rating' }
  ]

  if (!isLoaded || loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-gray-600 dark:text-gray-400">
            {language === 'ar' ? 'جاري التحميل...' : 'Loading...'}
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className={`min-h-screen ${isRTL ? 'rtl' : 'ltr'} relative overflow-hidden bg-white dark:bg-gray-900`}>
      {/* Navigation */}
      <nav className="relative z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <VideoCameraIcon className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                VEO7
              </span>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-8">
              <Link href="#features" className="text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 transition-colors">
                {language === 'ar' ? 'المميزات' : 'Features'}
              </Link>
              <Link href="#pricing" className="text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 transition-colors">
                {language === 'ar' ? 'الأسعار' : 'Pricing'}
              </Link>
              <Link href="#about" className="text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 transition-colors">
                {language === 'ar' ? 'حول' : 'About'}
              </Link>
              {user && (
                <Link href="/ai-studio" className="text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 transition-colors flex items-center space-x-1">
                  <SparklesIcon className="w-4 h-4" />
                  <span>{language === 'ar' ? 'استوديو الذكاء الاصطناعي' : 'AI Studio'}</span>
                </Link>
              )}
              
              {user ? (
                <Link 
                  href="/dashboard"
                  className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-2 rounded-full hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                >
                  {language === 'ar' ? 'لوحة التحكم' : 'Dashboard'}
                </Link>
              ) : (
                <div className="flex items-center space-x-4">
                  <Link 
                    href="/auth/login"
                    className="text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 transition-colors"
                  >
                    {language === 'ar' ? 'تسجيل الدخول' : 'Sign In'}
                  </Link>
                  <Link 
                    href="/auth/register"
                    className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-2 rounded-full hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                  >
                    {language === 'ar' ? 'إنشاء حساب' : 'Sign Up'}
                  </Link>
                </div>
              )}
            </div>

            {/* Mobile menu button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-md text-gray-700 dark:text-gray-300"
            >
              {mobileMenuOpen ? (
                <XMarkIcon className="w-6 h-6" />
              ) : (
                <Bars3Icon className="w-6 h-6" />
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="md:hidden bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700"
          >
            <div className="px-4 py-4 space-y-4">
              <Link href="#features" className="block text-gray-700 dark:text-gray-300">
                {language === 'ar' ? 'المميزات' : 'Features'}
              </Link>
              <Link href="#pricing" className="block text-gray-700 dark:text-gray-300">
                {language === 'ar' ? 'الأسعار' : 'Pricing'}
              </Link>
              <Link href="#about" className="block text-gray-700 dark:text-gray-300">
                {language === 'ar' ? 'حول' : 'About'}
              </Link>
              {user && (
                <Link href="/ai-studio" className="block text-gray-700 dark:text-gray-300 flex items-center space-x-2">
                  <SparklesIcon className="w-4 h-4" />
                  <span>{language === 'ar' ? 'استوديو الذكاء الاصطناعي' : 'AI Studio'}</span>
                </Link>
              )}
              {user ? (
                <Link href="/dashboard" className="block bg-purple-500 text-white px-4 py-2 rounded-lg text-center">
                  {language === 'ar' ? 'لوحة التحكم' : 'Dashboard'}
                </Link>
              ) : (
                <div className="space-y-2">
                  <Link href="/auth/login" className="block text-center text-gray-700 dark:text-gray-300">
                    {language === 'ar' ? 'تسجيل الدخول' : 'Sign In'}
                  </Link>
                  <Link href="/auth/register" className="block bg-purple-500 text-white px-4 py-2 rounded-lg text-center">
                    {language === 'ar' ? 'إنشاء حساب' : 'Sign Up'}
                  </Link>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </nav>

      {/* Hero Section */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0 bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50 dark:from-gray-900 dark:via-purple-900/20 dark:to-gray-900"></div>
        <div className="absolute top-0 left-0 w-96 h-96 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-gradient-to-r from-blue-400 to-cyan-400 rounded-full blur-3xl opacity-20 animate-pulse delay-1000"></div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 bg-clip-text text-transparent">
                {language === 'ar' ? 'أنشئ فيديوهات مذهلة' : 'Create Amazing Videos'}
              </span>
              <br />
              <span className="text-gray-900 dark:text-white">
                {language === 'ar' ? 'بالذكاء الاصطناعي' : 'with AI'}
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              {language === 'ar' 
                ? 'حول صورك ونصوصك إلى فيديوهات احترافية في ثوانٍ معدودة باستخدام أحدث تقنيات الذكاء الاصطناعي'
                : 'Transform your images and text into professional videos in seconds using cutting-edge AI technology'
              }
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
              <Link
                href={user ? "/dashboard" : "/auth/register"}
                className="group bg-gradient-to-r from-purple-500 to-pink-500 text-white px-8 py-4 rounded-full text-lg font-semibold hover:shadow-2xl transition-all duration-300 transform hover:scale-105 flex items-center space-x-2"
              >
                <span>{language === 'ar' ? 'ابدأ الآن مجاناً' : 'Start Free Now'}</span>
                <ArrowRightIcon className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              
              <button className="group flex items-center space-x-2 text-gray-700 dark:text-gray-300 hover:text-purple-600 dark:hover:text-purple-400 transition-colors">
                <div className="w-12 h-12 bg-white dark:bg-gray-800 rounded-full flex items-center justify-center shadow-lg group-hover:shadow-xl transition-shadow">
                  <PlayIcon className="w-6 h-6 ml-1" />
                </div>
                <span className="text-lg font-medium">
                  {language === 'ar' ? 'شاهد العرض التوضيحي' : 'Watch Demo'}
                </span>
              </button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
              {stats.map((stat, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="text-center"
                >
                  <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
                    {stat.number}
                  </div>
                  <div className="text-gray-600 dark:text-gray-400 font-medium">
                    {stat.label}
                  </div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Video Types Section */}
      <section id="features" className="py-20 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                {language === 'ar' ? 'أنواع الفيديوهات' : 'Video Types'}
              </span>
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              {language === 'ar' 
                ? 'اختر من بين مجموعة متنوعة من أنواع الفيديوهات التي يمكن إنتاجها بالذكاء الاصطناعي'
                : 'Choose from a variety of video types that can be generated with AI'
              }
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {videoTypes.map((type, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className="group relative bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100 dark:border-gray-700"
              >
                <div className={`w-16 h-16 bg-gradient-to-r ${type.gradient} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <type.icon className="w-8 h-8 text-white" />
                </div>
                
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
                  {type.title}
                </h3>
                
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                  {type.description}
                </p>

                <div className="absolute inset-0 bg-gradient-to-r from-purple-500/10 to-pink-500/10 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                {language === 'ar' ? 'لماذا VEO7؟' : 'Why VEO7?'}
              </span>
            </h2>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
                className="text-center"
              >
                <div className="w-20 h-20 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6">
                  <CheckIcon className="w-10 h-10 text-white" />
                </div>
                
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 dark:text-gray-300 text-lg leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 bg-gray-50 dark:bg-gray-900">
        <PricingSection language={language} isRTL={language === 'ar'} session={user} />
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-purple-600 to-pink-600">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              {language === 'ar' ? 'جاهز لإنشاء فيديوهات مذهلة؟' : 'Ready to Create Amazing Videos?'}
            </h2>
            
            <p className="text-xl text-purple-100 mb-8 max-w-2xl mx-auto">
              {language === 'ar' 
                ? 'انضم إلى آلاف المبدعين الذين يستخدمون VEO7 لإنتاج محتوى استثنائي'
                : 'Join thousands of creators using VEO7 to produce exceptional content'
              }
            </p>

            <Link
              href={user ? "/dashboard" : "/auth/register"}
              className="inline-flex items-center space-x-2 bg-white text-purple-600 px-8 py-4 rounded-full text-lg font-semibold hover:shadow-2xl transition-all duration-300 transform hover:scale-105"
            >
              <span>{language === 'ar' ? 'ابدأ رحلتك الآن' : 'Start Your Journey Now'}</span>
              <ArrowRightIcon className="w-5 h-5" />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                  <VideoCameraIcon className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold">VEO7</span>
              </div>
              <p className="text-gray-400">
                {language === 'ar' 
                  ? 'منصة توليد الفيديو بالذكاء الاصطناعي الرائدة'
                  : 'Leading AI video generation platform'
                }
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">
                {language === 'ar' ? 'المنتج' : 'Product'}
              </h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#features" className="hover:text-white transition-colors">{language === 'ar' ? 'المميزات' : 'Features'}</Link></li>
                <li><Link href="#pricing" className="hover:text-white transition-colors">{language === 'ar' ? 'الأسعار' : 'Pricing'}</Link></li>
                <li><Link href="/dashboard" className="hover:text-white transition-colors">{language === 'ar' ? 'لوحة التحكم' : 'Dashboard'}</Link></li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">
                {language === 'ar' ? 'الشركة' : 'Company'}
              </h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#about" className="hover:text-white transition-colors">{language === 'ar' ? 'حول' : 'About'}</Link></li>
                <li><Link href="#contact" className="hover:text-white transition-colors">{language === 'ar' ? 'اتصل بنا' : 'Contact'}</Link></li>
                <li><Link href="#privacy" className="hover:text-white transition-colors">{language === 'ar' ? 'الخصوصية' : 'Privacy'}</Link></li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">
                {language === 'ar' ? 'الدعم' : 'Support'}
              </h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="#help" className="hover:text-white transition-colors">{language === 'ar' ? 'مركز المساعدة' : 'Help Center'}</Link></li>
                <li><Link href="#docs" className="hover:text-white transition-colors">{language === 'ar' ? 'الوثائق' : 'Documentation'}</Link></li>
                <li><Link href="#api" className="hover:text-white transition-colors">{language === 'ar' ? 'API' : 'API'}</Link></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 VEO7. {language === 'ar' ? 'جميع الحقوق محفوظة.' : 'All rights reserved.'}</p>
          </div>
        </div>
      </footer>
    </div>
  )
}