'use client'

import React from 'react'
import Link from 'next/link'
import { ArrowLeftIcon, ArrowRightIcon } from '@heroicons/react/24/outline'
import { useLanguage } from '../../app/providers'
import BackButton from './BackButton'
import LanguageSwitcher from './LanguageSwitcher'
import ThemeSwitcher from './ThemeSwitcher'

interface PageLayoutProps {
  children: React.ReactNode
  title: string
  description?: string
  showBackButton?: boolean
  backHref?: string
  className?: string
  headerClassName?: string
}

export default function PageLayout({
  children,
  title,
  description,
  showBackButton = true,
  backHref = '/',
  className = '',
  headerClassName = ''
}: PageLayoutProps) {
  const { language, isRTL } = useLanguage()

  return (
    <div className={`min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-blue-900 ${isRTL ? 'rtl' : 'ltr'} ${className}`}>
      {/* Header */}
      <div className={`relative z-10 ${headerClassName}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-between mb-8">
            {showBackButton && (
              <BackButton href={backHref} />
            )}
            
            <div className="flex items-center space-x-4">
              <LanguageSwitcher />
              <ThemeSwitcher />
            </div>
          </div>
          
          {/* Page Title */}
          <div className="text-center mb-16">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-4">
              <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                {title}
              </span>
            </h1>
            {description && (
              <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
                {description}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="relative z-0">
        {children}
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 dark:bg-gray-950 text-white py-12 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
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
                <li><Link href="/#features" className="hover:text-white transition-colors">{language === 'ar' ? 'المميزات' : 'Features'}</Link></li>
                <li><Link href="/#pricing" className="hover:text-white transition-colors">{language === 'ar' ? 'الأسعار' : 'Pricing'}</Link></li>
                <li><Link href="/dashboard" className="hover:text-white transition-colors">{language === 'ar' ? 'لوحة التحكم' : 'Dashboard'}</Link></li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">
                {language === 'ar' ? 'الشركة' : 'Company'}
              </h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/about" className="hover:text-white transition-colors">{language === 'ar' ? 'حول' : 'About'}</Link></li>
                <li><Link href="/contact" className="hover:text-white transition-colors">{language === 'ar' ? 'اتصل بنا' : 'Contact'}</Link></li>
                <li><Link href="/privacy" className="hover:text-white transition-colors">{language === 'ar' ? 'الخصوصية' : 'Privacy'}</Link></li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">
                {language === 'ar' ? 'الدعم' : 'Support'}
              </h3>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/help" className="hover:text-white transition-colors">{language === 'ar' ? 'مركز المساعدة' : 'Help Center'}</Link></li>
                <li><Link href="/docs" className="hover:text-white transition-colors">{language === 'ar' ? 'الوثائق' : 'Documentation'}</Link></li>
                <li><Link href="/contact" className="hover:text-white transition-colors">{language === 'ar' ? 'الدعم الفني' : 'Support'}</Link></li>
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