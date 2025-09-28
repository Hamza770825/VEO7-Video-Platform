'use client'

import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useSupabaseClient } from '@supabase/auth-helpers-react'
import { motion } from 'framer-motion'
import Link from 'next/link'
import { 
  CheckCircleIcon, 
  ExclamationTriangleIcon, 
  PlayIcon,
  ArrowRightIcon,
  ClockIcon
} from '@heroicons/react/24/outline'
import { useLanguage } from '@/contexts/LanguageContext'
import { toast } from 'react-hot-toast'

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.6 } }
}

export default function AuthCallbackPage() {
  const [status, setStatus] = useState<'loading' | 'success' | 'error' | 'expired'>('loading')
  const [errorMessage, setErrorMessage] = useState('')
  const [isResending, setIsResending] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(0)
  
  const router = useRouter()
  const searchParams = useSearchParams()
  const supabase = useSupabaseClient()
  const { language, isRTL } = useLanguage()

  useEffect(() => {
    const handleAuthCallback = async () => {
      try {
        const { data, error } = await supabase.auth.getSession()
        
        if (error) {
          console.error('Auth callback error:', error)
          
          // التحقق من نوع الخطأ
          if (error.message.includes('expired') || error.message.includes('invalid')) {
            setStatus('expired')
            setErrorMessage(error.message)
          } else {
            setStatus('error')
            setErrorMessage(error.message)
          }
          return
        }

        if (data.session) {
          // نجح التحقق
          setStatus('success')
          
          toast.success(
            language === 'ar' 
              ? 'تم تأكيد البريد الإلكتروني بنجاح!'
              : 'Email verified successfully!'
          )
          
          // إعادة توجيه إلى لوحة التحكم بعد ثانيتين
          setTimeout(() => {
            router.push('/dashboard')
          }, 2000)
        } else {
          // لم يتم العثور على جلسة
          setStatus('error')
          setErrorMessage('No session found')
        }
      } catch (error: any) {
        console.error('Unexpected error:', error)
        setStatus('error')
        setErrorMessage(error.message || 'Unexpected error occurred')
      }
    }

    handleAuthCallback()
  }, [supabase, router, language])

  const handleResendVerification = async () => {
    if (resendCooldown > 0) return
    
    setIsResending(true)
    
    try {
      const email = localStorage.getItem('verification_email') || ''
      
      if (!email) {
        toast.error(
          language === 'ar' 
            ? 'لم يتم العثور على البريد الإلكتروني. يرجى المحاولة مرة أخرى من صفحة التسجيل.'
            : 'Email not found. Please try again from the registration page.'
        )
        return
      }

      const { error } = await supabase.auth.resend({
        type: 'signup',
        email: email
      })

      if (error) {
        toast.error(
          language === 'ar' 
            ? `خطأ في إرسال رابط التحقق: ${error.message}`
            : `Error sending verification link: ${error.message}`
        )
        return
      }

      toast.success(
        language === 'ar' 
          ? 'تم إرسال رابط التحقق الجديد إلى بريدك الإلكتروني'
          : 'New verification link sent to your email'
      )

      // بدء العد التنازلي
      setResendCooldown(60)
      const cooldownEnd = Date.now() + 60000
      localStorage.setItem('resend_cooldown', cooldownEnd.toString())
      
      const timer = setInterval(() => {
        setResendCooldown(prev => {
          if (prev <= 1) {
            clearInterval(timer)
            localStorage.removeItem('resend_cooldown')
            return 0
          }
          return prev - 1
        })
      }, 1000)

    } catch (error: any) {
      toast.error(
        language === 'ar' 
          ? 'حدث خطأ غير متوقع'
          : 'An unexpected error occurred'
      )
    } finally {
      setIsResending(false)
    }
  }

  const handleBackToLogin = () => {
    localStorage.removeItem('verification_email')
    router.push('/auth/login')
  }

  const renderContent = () => {
    switch (status) {
      case 'loading':
        return (
          <div className="text-center">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5 }}
              className="mx-auto flex items-center justify-center h-24 w-24 rounded-full bg-blue-100 dark:bg-blue-900/20 mb-6"
            >
              <div className="spinner w-8 h-8"></div>
            </motion.div>
            
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              {language === 'ar' ? 'جاري التحقق...' : 'Verifying...'}
            </h2>
            
            <p className="text-gray-600 dark:text-gray-400">
              {language === 'ar' 
                ? 'يرجى الانتظار بينما نتحقق من بريدك الإلكتروني'
                : 'Please wait while we verify your email'
              }
            </p>
          </div>
        )

      case 'success':
        return (
          <div className="text-center">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5 }}
              className="mx-auto flex items-center justify-center h-24 w-24 rounded-full bg-green-100 dark:bg-green-900/20 mb-6"
            >
              <CheckCircleIcon className="h-12 w-12 text-green-600 dark:text-green-400" />
            </motion.div>
            
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              {language === 'ar' ? 'تم التحقق بنجاح!' : 'Verification Successful!'}
            </h2>
            
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {language === 'ar' 
                ? 'تم تأكيد بريدك الإلكتروني بنجاح. سيتم إعادة توجيهك إلى لوحة التحكم...'
                : 'Your email has been verified successfully. Redirecting to dashboard...'
              }
            </p>
            
            <div className="spinner mx-auto"></div>
          </div>
        )

      case 'expired':
        return (
          <div className="text-center">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5 }}
              className="mx-auto flex items-center justify-center h-24 w-24 rounded-full bg-yellow-100 dark:bg-yellow-900/20 mb-6"
            >
              <ClockIcon className="h-12 w-12 text-yellow-600 dark:text-yellow-400" />
            </motion.div>
            
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              {language === 'ar' ? 'انتهت صلاحية الرابط' : 'Link Expired'}
            </h2>
            
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {language === 'ar' 
                ? 'انتهت صلاحية رابط التحقق. يرجى طلب رابط جديد.'
                : 'The verification link has expired. Please request a new one.'
              }
            </p>

            <div className="space-y-4">
              <button
                onClick={handleResendVerification}
                disabled={isResending || resendCooldown > 0}
                className="btn-primary w-full flex justify-center py-3"
              >
                {isResending ? (
                  <div className="spinner"></div>
                ) : resendCooldown > 0 ? (
                  `${language === 'ar' ? 'إعادة الإرسال خلال' : 'Resend in'} ${resendCooldown}s`
                ) : (
                  language === 'ar' ? 'إرسال رابط جديد' : 'Send new link'
                )}
              </button>

              <button
                onClick={handleBackToLogin}
                className="flex items-center justify-center w-full text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                {isRTL ? (
                  <>
                    <ArrowRightIcon className="w-4 h-4 ml-2" />
                    {language === 'ar' ? 'العودة إلى تسجيل الدخول' : 'Back to login'}
                  </>
                ) : (
                  <>
                    <ArrowRightIcon className="w-4 h-4 mr-2 rotate-180" />
                    {language === 'ar' ? 'العودة إلى تسجيل الدخول' : 'Back to login'}
                  </>
                )}
              </button>
            </div>
          </div>
        )

      case 'error':
      default:
        return (
          <div className="text-center">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5 }}
              className="mx-auto flex items-center justify-center h-24 w-24 rounded-full bg-red-100 dark:bg-red-900/20 mb-6"
            >
              <ExclamationTriangleIcon className="h-12 w-12 text-red-600 dark:text-red-400" />
            </motion.div>
            
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              {language === 'ar' ? 'فشل التحقق' : 'Verification Failed'}
            </h2>
            
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {language === 'ar' 
                ? 'حدث خطأ أثناء التحقق من بريدك الإلكتروني. يرجى المحاولة مرة أخرى.'
                : 'An error occurred while verifying your email. Please try again.'
              }
            </p>

            {errorMessage && (
              <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 mb-6">
                <p className="text-sm text-red-600 dark:text-red-400">
                  {errorMessage}
                </p>
              </div>
            )}

            <div className="space-y-4">
              <button
                onClick={handleResendVerification}
                disabled={isResending || resendCooldown > 0}
                className="btn-primary w-full flex justify-center py-3"
              >
                {isResending ? (
                  <div className="spinner"></div>
                ) : resendCooldown > 0 ? (
                  `${language === 'ar' ? 'إعادة الإرسال خلال' : 'Resend in'} ${resendCooldown}s`
                ) : (
                  language === 'ar' ? 'إرسال رابط جديد' : 'Send new link'
                )}
              </button>

              <button
                onClick={handleBackToLogin}
                className="flex items-center justify-center w-full text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                {isRTL ? (
                  <>
                    <ArrowRightIcon className="w-4 h-4 ml-2" />
                    {language === 'ar' ? 'العودة إلى تسجيل الدخول' : 'Back to login'}
                  </>
                ) : (
                  <>
                    <ArrowRightIcon className="w-4 h-4 mr-2 rotate-180" />
                    {language === 'ar' ? 'العودة إلى تسجيل الدخول' : 'Back to login'}
                  </>
                )}
              </button>
            </div>
          </div>
        )
    }
  }

  return (
    <div className={`min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 ${isRTL ? 'rtl' : 'ltr'}`}>
      <motion.div
        className="max-w-md w-full space-y-8"
        initial="initial"
        animate="animate"
        variants={fadeInUp}
      >
        {/* Logo */}
        <div className="flex items-center justify-center">
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-12 h-12 bg-gradient-to-r from-primary-600 to-secondary-600 rounded-lg flex items-center justify-center">
              <PlayIcon className="w-7 h-7 text-white" />
            </div>
            <span className="text-3xl font-bold gradient-text">VEO7</span>
          </Link>
        </div>

        {/* Content */}
        {renderContent()}
      </motion.div>
    </div>
  )
}