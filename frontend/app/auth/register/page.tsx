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
  UserIcon,
  PlayIcon,
  CheckIcon
} from '@heroicons/react/24/outline'
import { useLanguage } from '../../providers'
import { useAuth } from '../../../contexts/AuthContext'

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 }
}

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [isGoogleLoading, setIsGoogleLoading] = useState(false)
  const [acceptTerms, setAcceptTerms] = useState(false)
  
  const router = useRouter()
  const { signUp, signInWithGoogle } = useAuth()
  const { language, isRTL } = useLanguage()

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const validateForm = () => {
    if (!formData.fullName.trim()) {
      toast.error(language === 'ar' ? 'الاسم الكامل مطلوب' : 'Full name is required')
      return false
    }

    if (!formData.email.trim()) {
      toast.error(language === 'ar' ? 'البريد الإلكتروني مطلوب' : 'Email is required')
      return false
    }

    if (formData.password.length < 6) {
      toast.error(language === 'ar' ? 'كلمة المرور يجب أن تكون 6 أحرف على الأقل' : 'Password must be at least 6 characters')
      return false
    }

    if (formData.password !== formData.confirmPassword) {
      toast.error(language === 'ar' ? 'كلمات المرور غير متطابقة' : 'Passwords do not match')
      return false
    }

    if (!acceptTerms) {
      toast.error(language === 'ar' ? 'يجب الموافقة على الشروط والأحكام' : 'You must accept the terms and conditions')
      return false
    }

    return true
  }

  const handleEmailRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateForm()) return

    setIsLoading(true)

    try {
      const result = await signUp(formData.email, formData.password, formData.fullName)
      
      if (!result.success) {
        if (result.error?.includes('already registered')) {
          toast.error(
            language === 'ar' 
              ? 'هذا البريد الإلكتروني مسجل بالفعل'
              : 'This email is already registered'
          )
        } else {
          toast.error(
            language === 'ar' 
              ? 'فشل في إنشاء الحساب. حاول مرة أخرى.'
              : 'Failed to create account. Please try again.'
          )
        }
        return
      }
      
      // حفظ البريد الإلكتروني في localStorage للاستخدام في صفحة التحقق
      localStorage.setItem('verification_email', formData.email)
      
      toast.success(
         language === 'ar' 
           ? 'تم إنشاء الحساب بنجاح! تحقق من بريدك الإلكتروني.'
           : 'Account created successfully! Please check your email.'
       )
       router.push('/auth/verify-email')
     } catch (error: any) {
       toast.error(
         language === 'ar' 
           ? 'حدث خطأ غير متوقع. حاول مرة أخرى.'
           : 'An unexpected error occurred. Please try again.'
       )
     } finally {
      setIsLoading(false)
    }
  }

  const handleGoogleRegister = async () => {
    setIsGoogleLoading(true)

    try {
      await signInWithGoogle()
    } catch (error) {
      toast.error(
        language === 'ar' 
          ? 'فشل التسجيل بـ Google. حاول مرة أخرى.'
          : 'Google registration failed. Please try again.'
      )
    } finally {
      setIsGoogleLoading(false)
    }
  }

  const passwordStrength = (password: string) => {
    let strength = 0
    if (password.length >= 6) strength++
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++
    if (password.match(/\d/)) strength++
    if (password.match(/[^a-zA-Z\d]/)) strength++
    return strength
  }

  const getPasswordStrengthText = (strength: number) => {
    if (language === 'ar') {
      switch (strength) {
        case 0: return 'ضعيف جداً'
        case 1: return 'ضعيف'
        case 2: return 'متوسط'
        case 3: return 'قوي'
        case 4: return 'قوي جداً'
        default: return ''
      }
    } else {
      switch (strength) {
        case 0: return 'Very Weak'
        case 1: return 'Weak'
        case 2: return 'Fair'
        case 3: return 'Strong'
        case 4: return 'Very Strong'
        default: return ''
      }
    }
  }

  const getPasswordStrengthColor = (strength: number) => {
    switch (strength) {
      case 0: return 'bg-red-500'
      case 1: return 'bg-red-400'
      case 2: return 'bg-yellow-500'
      case 3: return 'bg-green-500'
      case 4: return 'bg-green-600'
      default: return 'bg-gray-300'
    }
  }

  const currentPasswordStrength = passwordStrength(formData.password)

  return (
    <div className={`min-h-screen flex ${isRTL ? 'rtl' : 'ltr'} relative overflow-hidden`}>
      {/* Professional Background Effects */}
      <div className="fixed inset-0 -z-10">
        <div className="absolute inset-0 bg-gradient-space opacity-25 animate-aurora"></div>
        <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-gradient-sunset rounded-full blur-3xl opacity-15 animate-float"></div>
        <div className="absolute bottom-1/4 left-1/4 w-80 h-80 bg-gradient-ocean rounded-full blur-3xl opacity-15 animate-levitate"></div>
        <div className="absolute inset-0 bg-gray-50/85 dark:bg-gray-900/85 backdrop-blur-sm"></div>
      </div>

      {/* Creative Floating Elements */}
      <div className="fixed inset-0 -z-5 pointer-events-none">
        {[...Array(18)].map((_, i) => (
          <div
            key={i}
            className={`absolute w-1 h-1 bg-gradient-to-r from-secondary-400 to-primary-400 rounded-full opacity-25 animate-cosmic-drift`}
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 10}s`,
              animationDuration: `${15 + Math.random() * 10}s`
            }}
          />
        ))}
      </div>

      {/* Left Side - Image/Illustration */}
      <div className="hidden lg:block relative w-0 flex-1 z-10">
        <div className="absolute inset-0 bg-gradient-to-br from-secondary-600 to-primary-600">
          <div className="absolute inset-0 bg-black/20"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center text-white p-8">
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8, delay: 0.2 }}
              >
                <div className="w-24 h-24 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-6">
                  <PlayIcon className="w-12 h-12" />
                </div>
                <h3 className="text-3xl font-bold mb-4">
                  {language === 'ar' ? 'انضم إلى VEO7' : 'Join VEO7'}
                </h3>
                <p className="text-xl opacity-90 mb-8">
                  {language === 'ar' 
                    ? 'ابدأ رحلتك في إنتاج فيديوهات احترافية'
                    : 'Start your journey in professional video creation'
                  }
                </p>
                
                {/* Features List */}
                <div className="text-left space-y-3">
                  {[
                    language === 'ar' ? 'تحريك الصور بالذكاء الاصطناعي' : 'AI-powered image animation',
                    language === 'ar' ? 'تحويل النص إلى صوت' : 'Text-to-speech conversion',
                    language === 'ar' ? 'جودة احترافية' : 'Professional quality output',
                    language === 'ar' ? 'دعم متعدد اللغات' : 'Multi-language support'
                  ].map((feature, index) => (
                    <motion.div
                      key={index}
                      className="flex items-center space-x-3"
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
                    >
                      <CheckIcon className="w-5 h-5 text-green-300" />
                      <span>{feature}</span>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Form */}
      <div className="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-20 xl:px-24 relative z-10">
        <motion.div
          className="mx-auto w-full max-w-sm lg:w-96 relative"
          initial="initial"
          animate="animate"
          variants={fadeInUp}
        >
          {/* Professional Form Background */}
          <div className="absolute inset-0 bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl rounded-3xl shadow-2xl shadow-primary-500/10 border border-gray-200/50 dark:border-gray-700/50 -z-10"></div>
          <div className="absolute inset-0 bg-gradient-to-br from-primary-50/50 to-secondary-50/50 dark:from-primary-900/20 dark:to-secondary-900/20 rounded-3xl -z-10"></div>
          
          <div className="relative p-8">
            {/* Logo */}
            <motion.div 
              className="flex items-center justify-center mb-8"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <Link href="/" className="flex items-center space-x-2 group">
                <motion.div 
                  className="w-10 h-10 bg-gradient-space rounded-lg flex items-center justify-center shadow-lg group-hover:shadow-xl group-hover:shadow-primary-500/50 transition-all duration-300"
                  whileHover={{ scale: 1.1, rotate: 5 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <PlayIcon className="w-6 h-6 text-white group-hover:animate-pulse" />
                </motion.div>
                <motion.span 
                  className="text-2xl font-bold bg-gradient-space bg-clip-text text-transparent group-hover:animate-shimmer"
                  whileHover={{ scale: 1.05 }}
                >
                  VEO7
                </motion.span>
              </Link>
            </motion.div>

          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
              {language === 'ar' ? 'إنشاء حساب جديد' : 'Create your account'}
            </h2>
            <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
              {language === 'ar' 
                ? 'ابدأ رحلتك في إنتاج الفيديوهات'
                : 'Start your video creation journey'
              }
            </p>
          </div>

          <form className="space-y-6" onSubmit={handleEmailRegister}>
            {/* Full Name Field */}
            <div>
              <label htmlFor="fullName" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {language === 'ar' ? 'الاسم الكامل' : 'Full Name'}
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <UserIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="fullName"
                  name="fullName"
                  type="text"
                  autoComplete="name"
                  required
                  value={formData.fullName}
                  onChange={handleInputChange}
                  className="input-primary pl-10"
                  placeholder={language === 'ar' ? 'أدخل اسمك الكامل' : 'Enter your full name'}
                />
              </div>
            </div>

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
                  value={formData.email}
                  onChange={handleInputChange}
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
                  autoComplete="new-password"
                  required
                  value={formData.password}
                  onChange={handleInputChange}
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
              
              {/* Password Strength Indicator */}
              {formData.password && (
                <div className="mt-2">
                  <div className="flex space-x-1 mb-1">
                    {[...Array(4)].map((_, i) => (
                      <div
                        key={i}
                        className={`h-1 flex-1 rounded ${
                          i < currentPasswordStrength 
                            ? getPasswordStrengthColor(currentPasswordStrength)
                            : 'bg-gray-300'
                        }`}
                      />
                    ))}
                  </div>
                  <p className="text-xs text-gray-600">
                    {language === 'ar' ? 'قوة كلمة المرور: ' : 'Password strength: '}
                    <span className={`font-medium ${
                      currentPasswordStrength >= 3 ? 'text-green-600' : 
                      currentPasswordStrength >= 2 ? 'text-yellow-600' : 'text-red-600'
                    }`}>
                      {getPasswordStrengthText(currentPasswordStrength)}
                    </span>
                  </p>
                </div>
              )}
            </div>

            {/* Confirm Password Field */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                {language === 'ar' ? 'تأكيد كلمة المرور' : 'Confirm Password'}
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <LockClosedIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  autoComplete="new-password"
                  required
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  className="input-primary pl-10 pr-10"
                  placeholder={language === 'ar' ? 'أعد إدخال كلمة المرور' : 'Confirm your password'}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                >
                  {showConfirmPassword ? (
                    <EyeSlashIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  ) : (
                    <EyeIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
                  )}
                </button>
              </div>
            </div>

            {/* Terms and Conditions */}
            <div className="flex items-center">
              <input
                id="accept-terms"
                name="accept-terms"
                type="checkbox"
                checked={acceptTerms}
                onChange={(e) => setAcceptTerms(e.target.checked)}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <label htmlFor="accept-terms" className="ml-2 block text-sm text-gray-900 dark:text-gray-300">
                {language === 'ar' ? (
                  <>
                    أوافق على{' '}
                    <Link href="/terms" className="text-primary-600 hover:text-primary-500">
                      الشروط والأحكام
                    </Link>
                    {' '}و{' '}
                    <Link href="/privacy" className="text-primary-600 hover:text-primary-500">
                      سياسة الخصوصية
                    </Link>
                  </>
                ) : (
                  <>
                    I agree to the{' '}
                    <Link href="/terms" className="text-primary-600 hover:text-primary-500">
                      Terms and Conditions
                    </Link>
                    {' '}and{' '}
                    <Link href="/privacy" className="text-primary-600 hover:text-primary-500">
                      Privacy Policy
                    </Link>
                  </>
                )}
              </label>
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
                language === 'ar' ? 'إنشاء الحساب' : 'Create Account'
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

          {/* Google Register */}
          <button
            type="button"
            onClick={handleGoogleRegister}
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
                {language === 'ar' ? 'التسجيل بـ Google' : 'Sign up with Google'}
              </>
            )}
          </button>

          {/* Sign In Link */}
          <p className="mt-6 text-center text-sm text-gray-600 dark:text-gray-400">
            {language === 'ar' ? 'لديك حساب بالفعل؟ ' : 'Already have an account? '}
            <Link href="/auth/login" className="font-medium text-primary-600 hover:text-primary-500">
              {language === 'ar' ? 'تسجيل الدخول' : 'Sign in'}
            </Link>
          </p>
          </div>
        </motion.div>
      </div>
    </div>
  )
}