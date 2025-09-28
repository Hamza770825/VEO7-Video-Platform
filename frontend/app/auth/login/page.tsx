'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { toast } from 'react-hot-toast'
import { 
  EyeIcon, 
  EyeSlashIcon, 
  EnvelopeIcon, 
  LockClosedIcon,
  PlayIcon
} from '@heroicons/react/24/outline'
import { useLanguage } from '../../providers'
import { useAuth } from '../../../contexts/AuthContext'

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 }
}

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [isGoogleLoading, setIsGoogleLoading] = useState(false)
  
  const router = useRouter()
  const { signIn, signInWithGoogle } = useAuth()
  const { language, isRTL } = useLanguage()

  const handleEmailLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const result = await signIn(email, password)
      
      if (result.success) {
        toast.success(
          language === 'ar' 
            ? 'تم تسجيل الدخول بنجاح!'
            : 'Successfully logged in!'
        )
        router.push('/dashboard')
      } else {
        toast.error(
          language === 'ar' 
            ? result.error || 'خطأ في تسجيل الدخول. تحقق من بياناتك وحاول مرة أخرى.'
            : result.error || 'Login failed. Please check your credentials and try again.'
        )
      }
    } catch (error: any) {
      toast.error(
        language === 'ar' 
          ? 'خطأ في تسجيل الدخول. تحقق من بياناتك وحاول مرة أخرى.'
          : 'Login failed. Please check your credentials and try again.'
      )
    } finally {
      setIsLoading(false)
    }
  }

  const handleGoogleLogin = async () => {
    setIsGoogleLoading(true)

    try {
      const result = await signInWithGoogle()
      
      if (!result.success) {
        toast.error(
          language === 'ar' 
            ? result.error || 'فشل تسجيل الدخول بـ Google. حاول مرة أخرى.'
            : result.error || 'Google login failed. Please try again.'
        )
      }
      // Note: Google OAuth will handle redirect automatically via redirectTo option
    } catch (error: any) {
      toast.error(
        language === 'ar' 
          ? 'فشل تسجيل الدخول بـ Google. حاول مرة أخرى.'
          : 'Google login failed. Please try again.'
      )
    } finally {
      setIsGoogleLoading(false)
    }
  }

  return (
    <div className={`min-h-screen flex ${isRTL ? 'rtl' : 'ltr'} relative overflow-hidden`}>
      {/* Professional Background Effects */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-cyberpunk opacity-30 animate-aurora"></div>
        <div className="absolute top-1/3 left-1/4 w-96 h-96 bg-gradient-neon rounded-full blur-3xl opacity-20 animate-float"></div>
        <div className="absolute bottom-1/3 right-1/4 w-80 h-80 bg-gradient-electric rounded-full blur-3xl opacity-20 animate-levitate"></div>
        <div className="absolute inset-0 bg-gray-50/90 dark:bg-gray-900/90 backdrop-blur-sm"></div>
      </div>

      {/* Creative Floating Elements */}
      <div className="fixed inset-0 -z-5 pointer-events-none">
        {[...Array(15)].map((_, i) => (
          <div
            key={i}
            className={`absolute w-1.5 h-1.5 bg-gradient-to-r from-primary-400 to-accent-400 rounded-full opacity-30 animate-cosmic-drift`}
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 8}s`,
              animationDuration: `${12 + Math.random() * 8}s`
            }}
          />
        ))}
      </div>

      {/* Left Side - Form */}
      <div className="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-20 xl:px-24 relative z-10">
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
              {language === 'ar' ? 'مرحباً بعودتك' : 'Welcome back'}
            </h2>
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
              {language === 'ar' 
                ? 'سجل دخولك للوصول إلى حسابك'
                : 'Sign in to access your account'
              }
            </p>
          </div>

          <form className="space-y-6" onSubmit={handleEmailLogin}>
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

            {/* Password Field */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {language === 'ar' ? 'كلمة المرور' : 'Password'}
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <LockClosedIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input-primary pl-10 pr-10"
                  placeholder={language === 'ar' ? 'أدخل كلمة المرور' : 'Enter your password'}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeSlashIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  ) : (
                    <EyeIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  )}
                </button>
              </div>
            </div>

            {/* Remember Me & Forgot Password */}
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <input
                  id="remember-me"
                  name="remember-me"
                  type="checkbox"
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-900 dark:text-gray-300">
                  {language === 'ar' ? 'تذكرني' : 'Remember me'}
                </label>
              </div>

              <div className="text-sm">
                <Link href="/auth/forgot-password" className="font-medium text-primary-600 hover:text-primary-500">
                  {language === 'ar' ? 'نسيت كلمة المرور؟' : 'Forgot your password?'}
                </Link>
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
                language === 'ar' ? 'تسجيل الدخول' : 'Sign in'
              )}
            </button>
          </form>

          {/* Divider */}
          <div className="mt-6">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300 dark:border-gray-600" />
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white dark:bg-gray-900 text-gray-500">
                  {language === 'ar' ? 'أو' : 'Or'}
                </span>
              </div>
            </div>
          </div>

          {/* Google Login */}
          <button
            type="button"
            onClick={handleGoogleLogin}
            disabled={isGoogleLoading}
            className="mt-6 w-full btn-outline flex justify-center items-center py-3"
          >
            {isGoogleLoading ? (
              <div className="spinner"></div>
            ) : (
              <>
                <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                {language === 'ar' ? 'تسجيل الدخول بـ Google' : 'Continue with Google'}
              </>
            )}
          </button>

          {/* Sign Up Link */}
          <p className="mt-6 text-center text-sm text-gray-600 dark:text-gray-400">
            {language === 'ar' ? 'ليس لديك حساب؟ ' : "Don't have an account? "}
            <Link href="/auth/register" className="font-medium text-primary-600 hover:text-primary-500">
              {language === 'ar' ? 'إنشاء حساب جديد' : 'Sign up'}
            </Link>
          </p>
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
                <PlayIcon className="w-24 h-24 mx-auto mb-6 opacity-80" />
                <h3 className="text-3xl font-bold mb-4">
                  {language === 'ar' ? 'أنتج فيديوهات رائعة' : 'Create Amazing Videos'}
                </h3>
                <p className="text-xl opacity-90">
                  {language === 'ar' 
                    ? 'حول صورك إلى فيديوهات متحركة بالذكاء الاصطناعي'
                    : 'Transform your images into animated videos with AI'
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