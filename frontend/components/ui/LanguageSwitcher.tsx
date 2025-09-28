'use client'

import { useState, useRef, useEffect } from 'react'
import { LanguageIcon, ChevronDownIcon } from '@heroicons/react/24/outline'
import { useLanguage } from '@/app/providers'

interface LanguageSwitcherProps {
  variant?: 'default' | 'minimal' | 'icon-only'
  className?: string
}

export default function LanguageSwitcher({ variant = 'default', className = '' }: LanguageSwitcherProps) {
  const { language, setLanguage, isRTL } = useLanguage()
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])

  const languages = [
    { code: 'en', name: 'English', nativeName: 'English', flag: '🇺🇸', dir: 'ltr' },
    { code: 'ar', name: 'Arabic', nativeName: 'العربية', flag: '🇸🇦', dir: 'rtl' }
  ]

  const currentLanguage = languages.find(lang => lang.code === language)

  const handleLanguageChange = (langCode: 'en' | 'ar') => {
    setLanguage(langCode)
    setIsOpen(false)
  }

  if (variant === 'icon-only') {
    return (
      <div className={`relative ${className}`} ref={dropdownRef}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="group relative p-3 text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-all duration-300 rounded-xl hover:bg-gradient-to-r hover:from-primary-50 hover:to-secondary-50 dark:hover:from-primary-900/20 dark:hover:to-secondary-900/20 hover:shadow-lg hover:scale-105"
          aria-label={language === 'ar' ? 'تغيير اللغة' : 'Change language'}
        >
          <LanguageIcon className="w-5 h-5 transition-transform duration-300 group-hover:rotate-12" />
          <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-primary-500 to-secondary-500 opacity-0 group-hover:opacity-10 transition-opacity duration-300"></div>
        </button>
        
        {isOpen && (
          <div className={`absolute top-full mt-3 w-56 bg-white/95 dark:bg-gray-800/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-gray-200/50 dark:border-gray-700/50 z-50 overflow-hidden transform transition-all duration-300 ${isRTL ? 'right-0' : 'left-0'}`}>
            <div className="p-2">
              {languages.map((lang, index) => (
                <button
                  key={lang.code}
                  onClick={() => handleLanguageChange(lang.code as 'en' | 'ar')}
                  className={`w-full px-4 py-3 rounded-xl transition-all duration-300 flex items-center ${lang.dir === 'rtl' ? 'flex-row-reverse' : 'flex-row'} ${lang.dir === 'rtl' ? 'space-x-reverse space-x-3' : 'space-x-3'} group ${
                    language === lang.code 
                      ? 'bg-gradient-to-r from-primary-500 to-secondary-500 text-white shadow-lg transform scale-105' 
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-primary-50 hover:to-secondary-50 dark:hover:from-primary-900/20 dark:hover:to-secondary-900/20 hover:scale-102'
                  }`}
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  <span className="text-xl transition-transform duration-300 group-hover:scale-110">{lang.flag}</span>
                  <div className={`flex flex-col ${lang.dir === 'rtl' ? 'items-end' : 'items-start'}`}>
                    <span className="font-semibold text-sm">{lang.nativeName}</span>
                    <span className="text-xs opacity-75">{lang.name}</span>
                  </div>
                  {language === lang.code && (
                    <div className="ml-auto">
                      <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                    </div>
                  )}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    )
  }

  if (variant === 'minimal') {
    return (
      <div className={`relative ${className}`} ref={dropdownRef}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className={`group flex items-center ${isRTL ? 'flex-row-reverse space-x-reverse' : ''} space-x-2 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-all duration-300 rounded-xl hover:bg-gradient-to-r hover:from-primary-50 hover:to-secondary-50 dark:hover:from-primary-900/20 dark:hover:to-secondary-900/20 hover:shadow-md hover:scale-105`}
        >
          <span className="text-lg transition-transform duration-300 group-hover:scale-110">{currentLanguage?.flag}</span>
          <span className="font-bold">{currentLanguage?.code.toUpperCase()}</span>
          <ChevronDownIcon className={`w-4 h-4 transition-all duration-300 ${isOpen ? 'rotate-180 text-primary-500' : 'group-hover:text-primary-500'}`} />
        </button>
        
        {isOpen && (
          <div className={`absolute top-full mt-3 w-56 bg-white/95 dark:bg-gray-800/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-gray-200/50 dark:border-gray-700/50 z-50 overflow-hidden transform transition-all duration-300 ${isRTL ? 'right-0' : 'left-0'}`}>
            <div className="p-2">
              {languages.map((lang, index) => (
                <button
                  key={lang.code}
                  onClick={() => handleLanguageChange(lang.code as 'en' | 'ar')}
                  className={`w-full px-4 py-3 rounded-xl transition-all duration-300 flex items-center ${lang.dir === 'rtl' ? 'flex-row-reverse' : 'flex-row'} ${lang.dir === 'rtl' ? 'space-x-reverse space-x-3' : 'space-x-3'} group ${
                    language === lang.code 
                      ? 'bg-gradient-to-r from-primary-500 to-secondary-500 text-white shadow-lg transform scale-105' 
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-primary-50 hover:to-secondary-50 dark:hover:from-primary-900/20 dark:hover:to-secondary-900/20 hover:scale-102'
                  }`}
                  style={{ animationDelay: `${index * 50}ms` }}
                >
                  <span className="text-xl transition-transform duration-300 group-hover:scale-110">{lang.flag}</span>
                  <div className={`flex flex-col ${lang.dir === 'rtl' ? 'items-end' : 'items-start'}`}>
                    <span className="font-semibold text-sm">{lang.nativeName}</span>
                    <span className="text-xs opacity-75">{lang.name}</span>
                  </div>
                  {language === lang.code && (
                    <div className="ml-auto">
                      <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                    </div>
                  )}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    )
  }

  return (
    <div className={`relative ${className}`} ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`group flex items-center ${isRTL ? 'flex-row-reverse space-x-reverse' : ''} space-x-3 px-6 py-3 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-gray-300/50 dark:border-gray-600/50 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 hover:bg-gradient-to-r hover:from-primary-50 hover:to-secondary-50 dark:hover:from-primary-900/20 dark:hover:to-secondary-900/20 hover:scale-105 hover:border-primary-300 dark:hover:border-primary-600`}
      >
        <LanguageIcon className="w-5 h-5 text-gray-500 dark:text-gray-400 group-hover:text-primary-500 transition-all duration-300 group-hover:rotate-12" />
        <span className="text-xl transition-transform duration-300 group-hover:scale-110">{currentLanguage?.flag}</span>
        <div className={`flex flex-col ${isRTL ? 'items-end' : 'items-start'}`}>
          <span className="font-bold text-gray-700 dark:text-gray-300 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-300">{currentLanguage?.nativeName}</span>
          <span className="text-xs text-gray-500 dark:text-gray-400">{currentLanguage?.name}</span>
        </div>
        <ChevronDownIcon className={`w-4 h-4 text-gray-500 dark:text-gray-400 group-hover:text-primary-500 transition-all duration-300 ${isOpen ? 'rotate-180' : ''}`} />
      </button>
      
      {isOpen && (
        <div className={`absolute top-full mt-3 w-full min-w-64 bg-white/95 dark:bg-gray-800/95 backdrop-blur-xl rounded-2xl shadow-2xl border border-gray-200/50 dark:border-gray-700/50 z-50 overflow-hidden transform transition-all duration-300`}>
          <div className="p-2">
            {languages.map((lang, index) => (
              <button
                key={lang.code}
                onClick={() => handleLanguageChange(lang.code as 'en' | 'ar')}
                className={`w-full px-4 py-4 rounded-xl transition-all duration-300 flex items-center ${lang.dir === 'rtl' ? 'flex-row-reverse' : 'flex-row'} ${lang.dir === 'rtl' ? 'space-x-reverse space-x-3' : 'space-x-3'} group ${
                  language === lang.code 
                    ? 'bg-gradient-to-r from-primary-500 to-secondary-500 text-white shadow-lg transform scale-105' 
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gradient-to-r hover:from-primary-50 hover:to-secondary-50 dark:hover:from-primary-900/20 dark:hover:to-secondary-900/20 hover:scale-102'
                }`}
                style={{ animationDelay: `${index * 50}ms` }}
              >
                <span className="text-2xl transition-transform duration-300 group-hover:scale-110">{lang.flag}</span>
                <div className={`flex flex-col ${lang.dir === 'rtl' ? 'items-end' : 'items-start'}`}>
                  <span className="font-bold text-base">{lang.nativeName}</span>
                  <span className="text-sm opacity-75">{lang.name}</span>
                </div>
                {language === lang.code && (
                  <div className="ml-auto">
                    <div className="w-3 h-3 bg-white rounded-full animate-pulse shadow-lg"></div>
                  </div>
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}