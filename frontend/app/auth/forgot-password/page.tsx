'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import { toast } from 'react-hot-toast'
import { 
  EnvelopeIcon,
  ArrowLeftIcon,
  ArrowRightIcon,
  PlayIcon
} from '@heroicons/react/24/outline'
import { useLanguage } from '../../providers'
import Link from 'next/link'

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.6 } }
}

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isEmailSent, setIsEmailSent] = useState(false)
  
  const router = useRouter()
  const { language, isRTL } = useLanguage()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      // محاكاة إرسال البريد الإلكتروني
      await new Promise(resolve => setTimeout(resolve, 2000))
      
      setIsEmailSent(true)
      toast.success(
        language === 'ar' 
          ? 'تم إرسال رابط إعادة تعيين كلمة المرور إلى بريدك الإلكتروني'
          : 'Password reset link has been sent to your email'
      )
    } catch (error: any) {
      toast.error(
        language === 'ar' 
          ? 'حدث خطأ أثناء إرسال البريد الإلكتروني'
          : 'An error occurred while sending the email'
      )
    } finally {
      setIsLoading(false)
    }
  }

  const handleBackToLogin = () => {
    router.push('/auth/login')
  }

  if (isEmailSent) {
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

          {/* Success Message */}
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
              {language === 'ar' ? 'تم إرسال البريد الإلكتروني' : 'Email sent'}
            </h2>
            
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {language === 'ar' 
                ? `تم إرسال رابط إعادة تعيين كلمة المرور إلى ${email}. تحقق من صندوق الوارد الخاص بك.`
                : `A password reset link has been sent to ${email}. Please check your inbox.`
              }
            </p>

            <button
              onClick={handleBackToLogin}
              className="btn-primary w-full py-3"
            >
              {language === 'ar' ? 'العودة إلى تسجيل الدخول' : 'Back to login'}
            </button>
          </div>
        </motion.div>
      </div>
    )
  }

  return (
    <div className={`min-h-screen flex ${isRTL ? 'rtl' : 'ltr'}`}>
      {/* Left Side - Form */}
      <div className="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-20 xl:px-24">
        <motion.div
          className="mx-auto w-full max-w-sm lg:w-96"
          initial="initial"
          animate="animate"
          variants={fadeInUp}
        >
          {/* Logo */}
          <div className="flex items-center justify-center mb-8">
            <Link href="/" className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-gradient-to-r from-primary-600 to-secondary-600 rounded-lg flex items-center justify-center">
                <PlayIcon className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold gradient-text">VEO7</span>
            </Link>
          </div>

          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
              {language === 'ar' ? 'نسيت كلمة المرور؟' : 'Forgot your password?'}
            </h2>
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
              {language === 'ar' 
                ? 'أدخل بريدك الإلكتروني وسنرسل لك رابط إعادة تعيين كلمة المرور'
                : 'Enter your email and we\'ll send you a password reset link'
              }
            </p>
          </div>

          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* Email Field */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {language === 'ar' ? 'البريد الإلكتروني' : 'Email address'}
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <EnvelopeIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="input-primary pl-10"
                  placeholder={language === 'ar' ? 'أدخل بريدك الإلكتروني' : 'Enter your email'}
                />
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full flex justify-center py-3"
            >
              {isLoading ? (
                <div className="spinner"></div>
              ) : (
                language === 'ar' ? 'إرسال رابط إعادة التعيين' : 'Send reset link'
              )}
            </button>
          </form>

          {/* Back to Login */}
          <div className="mt-6 text-center">
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
                  <ArrowLeftIcon className="w-4 h-4 mr-2" />
                  {language === 'ar' ? 'العودة إلى تسجيل الدخول' : 'Back to login'}
                </>
              )}
            </button>
          </div>
        </motion.div>
      </div>

      {/* Right Side - Image/Illustration */}
      <div className="hidden lg:block relative w-0 flex-1">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-600 to-secondary-600">
          <div className="absolute inset-0 bg-black/20"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center text-white p-8">
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8, delay: 0.2 }}
              >
                <div className="w-24 h-24 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-6">
                  <EnvelopeIcon className="w-12 h-12" />
                </div>
                <h3 className="text-3xl font-bold mb-4">
                  {language === 'ar' ? 'استعادة الحساب' : 'Account Recovery'}
                </h3>
                <p className="text-xl opacity-90">
                  {language === 'ar' 
                    ? 'سنساعدك في استعادة الوصول إلى حسابك'
                    : 'We\'ll help you regain access to your account'
                  }
                </p>
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}