'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useSupabaseClient } from '@supabase/auth-helpers-react'
import { toast } from 'react-hot-toast'
import { 
  EnvelopeIcon, 
  CheckCircleIcon,
  ArrowPathIcon,
  PlayIcon
} from '@heroicons/react/24/outline'
import { useLanguage } from '../../providers'

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 }
}

export default function VerifyEmailPage() {
  const [isResending, setIsResending] = useState(false)
  const [resendCooldown, setResendCooldown] = useState(0)
  const [email, setEmail] = useState('')
  
  const router = useRouter()
  const supabase = useSupabaseClient()
  const { language, isRTL } = useLanguage()

  useEffect(() => {
    // Get email from localStorage or URL params
    const storedEmail = localStorage.getItem('verification_email')
    if (storedEmail) {
      setEmail(storedEmail)
    }

    // Start cooldown timer if exists
    const cooldownEnd = localStorage.getItem('resend_cooldown')
    if (cooldownEnd) {
      const remaining = Math.max(0, parseInt(cooldownEnd) - Date.now())
      if (remaining > 0) {
        setResendCooldown(Math.ceil(remaining / 1000))
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
        return () => clearInterval(timer)
      }
    }
  }, [])

  const handleResendEmail = async () => {
    if (!email) {
      toast.error(
        language === 'ar' 
          ? 'لم يتم العثور على البريد الإلكتروني'
          : 'Email not found'
      )
      return
    }

    setIsResending(true)

    try {
      const { error } = await supabase.auth.resend({
        type: 'signup',
        email: email
      })

      if (error) {
        const errorMsg = error.message.toLowerCase()
        
        if (errorMsg.includes('rate limit') || errorMsg.includes('too many')) {
          toast.error(
            language === 'ar' 
              ? 'تم إرسال عدد كبير من الطلبات. يرجى الانتظار قبل المحاولة مرة أخرى.'
              : 'Too many requests. Please wait before trying again.'
          )
        } else if (errorMsg.includes('already confirmed')) {
          toast.success(
            language === 'ar' 
              ? 'تم تأكيد البريد الإلكتروني بالفعل. يمكنك تسجيل الدخول الآن.'
              : 'Email already confirmed. You can now log in.'
          )
          setTimeout(() => router.push('/auth/login'), 2000)
        } else {
          toast.error(
            language === 'ar' 
              ? `فشل في إعادة إرسال البريد: ${error.message}`
              : `Failed to resend email: ${error.message}`
          )
        }
      } else {
        toast.success(
          language === 'ar' 
            ? 'تم إعادة إرسال البريد بنجاح!'
            : 'Email resent successfully!'
        )
        
        // Set 60 second cooldown
        const cooldownEnd = Date.now() + 60000
        localStorage.setItem('resend_cooldown', cooldownEnd.toString())
        setResendCooldown(60)
        
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
      }
    } catch (error) {
      toast.error(
        language === 'ar' 
          ? 'حدث خطأ غير متوقع. حاول مرة أخرى.'
          : 'An unexpected error occurred. Please try again.'
      )
    } finally {
      setIsResending(false)
    }
  }

  const handleBackToLogin = () => {
    localStorage.removeItem('verification_email')
    router.push('/auth/login')
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

        {/* Main Content */}
        <div className="text-center">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mx-auto flex items-center justify-center h-24 w-24 rounded-full bg-green-100 dark:bg-green-900/20 mb-6"
          >
            <EnvelopeIcon className="h-12 w-12 text-green-600 dark:text-green-400" />
          </motion.div>

          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            {language === 'ar' ? 'تحقق من بريدك الإلكتروني' : 'Check your email'}
          </h2>
          
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            {language === 'ar' 
              ? 'لقد أرسلنا رابط التأكيد إلى بريدك الإلكتروني. انقر على الرابط لتفعيل حسابك.'
              : 'We sent a confirmation link to your email address. Click the link to activate your account.'
            }
          </p>

          {email && (
            <p className="text-sm text-gray-500 dark:text-gray-400 mb-8">
              {language === 'ar' ? 'تم الإرسال إلى: ' : 'Sent to: '}
              <span className="font-medium text-gray-900 dark:text-white">{email}</span>
            </p>
          )}

          {/* Instructions */}
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-8">
            <div className="flex">
              <div className="flex-shrink-0">
                <CheckCircleIcon className="h-5 w-5 text-blue-400" />
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-blue-800 dark:text-blue-200">
                  {language === 'ar' ? 'خطوات التفعيل:' : 'Activation steps:'}
                </h3>
                <div className="mt-2 text-sm text-blue-700 dark:text-blue-300">
                  <ol className={`list-decimal ${isRTL ? 'list-inside' : 'list-inside'} space-y-1`}>
                    <li>{language === 'ar' ? 'افتح بريدك الإلكتروني' : 'Open your email inbox'}</li>
                    <li>{language === 'ar' ? 'ابحث عن رسالة من VEO7' : 'Look for an email from VEO7'}</li>
                    <li>{language === 'ar' ? 'انقر على رابط التأكيد' : 'Click the confirmation link'}</li>
                    <li>{language === 'ar' ? 'ستتم إعادة توجيهك تلقائياً' : 'You will be redirected automatically'}</li>
                  </ol>
                </div>
              </div>
            </div>
          </div>

          {/* Resend Email Button */}
          <div className="space-y-4">
            <button
              onClick={handleResendEmail}
              disabled={isResending || resendCooldown > 0}
              className="btn-outline w-full flex justify-center items-center py-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isResending ? (
                <>
                  <ArrowPathIcon className="w-5 h-5 mr-2 animate-spin" />
                  {language === 'ar' ? 'جاري الإرسال...' : 'Sending...'}
                </>
              ) : resendCooldown > 0 ? (
                <>
                  <ArrowPathIcon className="w-5 h-5 mr-2" />
                  {language === 'ar' 
                    ? `إعادة الإرسال خلال ${resendCooldown}ث`
                    : `Resend in ${resendCooldown}s`
                  }
                </>
              ) : (
                <>
                  <ArrowPathIcon className="w-5 h-5 mr-2" />
                  {language === 'ar' ? 'إعادة إرسال البريد' : 'Resend email'}
                </>
              )}
            </button>

            <button
              onClick={handleBackToLogin}
              className="btn-ghost w-full py-3"
            >
              {language === 'ar' ? 'العودة إلى تسجيل الدخول' : 'Back to login'}
            </button>
          </div>

          {/* Help Text */}
          <div className="mt-8 text-sm text-gray-500 dark:text-gray-400">
            <p>
              {language === 'ar' 
                ? 'لم تستلم البريد؟ تحقق من مجلد الرسائل غير المرغوب فيها أو '
                : "Didn't receive the email? Check your spam folder or "
              }
              <button
                onClick={handleResendEmail}
                disabled={resendCooldown > 0}
                className="text-primary-600 hover:text-primary-500 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {language === 'ar' ? 'أعد المحاولة' : 'try again'}
              </button>
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  )
}