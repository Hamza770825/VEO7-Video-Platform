'use client'

import { SunIcon, MoonIcon } from '@heroicons/react/24/outline'
import { useTheme } from '@/app/providers'
import { useLanguage } from '@/app/providers'

interface ThemeSwitcherProps {
  variant?: 'default' | 'minimal' | 'icon-only'
  className?: string
}

export default function ThemeSwitcher({ variant = 'default', className = '' }: ThemeSwitcherProps) {
  const { theme, toggleTheme } = useTheme()
  const { language, isRTL } = useLanguage()

  const isDark = theme === 'dark'

  if (variant === 'icon-only') {
    return (
      <button
        onClick={toggleTheme}
        className={`group relative p-3 text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-all duration-500 rounded-xl hover:bg-gradient-to-r hover:from-primary-50 hover:to-secondary-50 dark:hover:from-primary-900/20 dark:hover:to-secondary-900/20 hover:shadow-lg hover:scale-105 ${className}`}
        aria-label={language === 'ar' ? (isDark ? 'تفعيل الوضع النهاري' : 'تفعيل الوضع الليلي') : (isDark ? 'Switch to light mode' : 'Switch to dark mode')}
      >
        <div className="relative">
          {isDark ? (
            <SunIcon className="w-5 h-5 transition-all duration-500 group-hover:rotate-180 group-hover:scale-110 text-yellow-500 group-hover:text-yellow-400" />
          ) : (
            <MoonIcon className="w-5 h-5 transition-all duration-500 group-hover:rotate-12 group-hover:scale-110 text-blue-600 group-hover:text-blue-500" />
          )}
          
          {/* Glow effect */}
          <div className={`absolute inset-0 rounded-full transition-all duration-500 ${
            isDark 
              ? 'bg-yellow-400 opacity-0 group-hover:opacity-20 blur-sm' 
              : 'bg-blue-500 opacity-0 group-hover:opacity-20 blur-sm'
          }`}></div>
        </div>
        
        {/* Background gradient */}
        <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-primary-500 to-secondary-500 opacity-0 group-hover:opacity-10 transition-opacity duration-500"></div>
      </button>
    )
  }

  if (variant === 'minimal') {
    return (
      <button
        onClick={toggleTheme}
        className={`group flex items-center ${isRTL ? 'flex-row-reverse space-x-reverse' : ''} space-x-2 px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 transition-all duration-500 rounded-xl hover:bg-gradient-to-r hover:from-primary-50 hover:to-secondary-50 dark:hover:from-primary-900/20 dark:hover:to-secondary-900/20 hover:shadow-md hover:scale-105 ${className}`}
        aria-label={language === 'ar' ? (isDark ? 'تفعيل الوضع النهاري' : 'تفعيل الوضع الليلي') : (isDark ? 'Switch to light mode' : 'Switch to dark mode')}
      >
        <div className="relative">
          {isDark ? (
            <SunIcon className="w-4 h-4 transition-all duration-500 group-hover:rotate-180 group-hover:scale-110 text-yellow-500 group-hover:text-yellow-400" />
          ) : (
            <MoonIcon className="w-4 h-4 transition-all duration-500 group-hover:rotate-12 group-hover:scale-110 text-blue-600 group-hover:text-blue-500" />
          )}
          
          {/* Glow effect */}
          <div className={`absolute inset-0 rounded-full transition-all duration-500 ${
            isDark 
              ? 'bg-yellow-400 opacity-0 group-hover:opacity-30 blur-sm' 
              : 'bg-blue-500 opacity-0 group-hover:opacity-30 blur-sm'
          }`}></div>
        </div>
        
        <span className="font-bold transition-all duration-300 group-hover:scale-105">
          {language === 'ar' ? (isDark ? 'نهاري' : 'ليلي') : (isDark ? 'Light' : 'Dark')}
        </span>
      </button>
    )
  }

  return (
    <button
      onClick={toggleTheme}
      className={`group flex items-center ${isRTL ? 'flex-row-reverse space-x-reverse' : ''} space-x-3 px-6 py-3 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border border-gray-300/50 dark:border-gray-600/50 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-500 hover:bg-gradient-to-r hover:from-primary-50 hover:to-secondary-50 dark:hover:from-primary-900/20 dark:hover:to-secondary-900/20 hover:scale-105 hover:border-primary-300 dark:hover:border-primary-600 ${className}`}
      aria-label={language === 'ar' ? (isDark ? 'تفعيل الوضع النهاري' : 'تفعيل الوضع الليلي') : (isDark ? 'Switch to light mode' : 'Switch to dark mode')}
    >
      <div className="relative">
        {isDark ? (
          <SunIcon className="w-6 h-6 transition-all duration-500 group-hover:rotate-180 group-hover:scale-110 text-yellow-500 group-hover:text-yellow-400" />
        ) : (
          <MoonIcon className="w-6 h-6 transition-all duration-500 group-hover:rotate-12 group-hover:scale-110 text-blue-600 group-hover:text-blue-500" />
        )}
        
        {/* Glow effect */}
        <div className={`absolute inset-0 rounded-full transition-all duration-500 ${
          isDark 
            ? 'bg-yellow-400 opacity-0 group-hover:opacity-40 blur-md' 
            : 'bg-blue-500 opacity-0 group-hover:opacity-40 blur-md'
        }`}></div>
      </div>
      
      <div className={`flex flex-col ${isRTL ? 'items-end' : 'items-start'}`}>
        <span className="font-bold text-gray-700 dark:text-gray-300 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-all duration-300 group-hover:scale-105">
          {language === 'ar' ? (isDark ? 'الوضع النهاري' : 'الوضع الليلي') : (isDark ? 'Light Mode' : 'Dark Mode')}
        </span>
        <span className="text-xs text-gray-500 dark:text-gray-400 transition-all duration-300">
          {language === 'ar' ? (isDark ? 'تفعيل الإضاءة' : 'تفعيل الظلام') : (isDark ? 'Bright theme' : 'Dark theme')}
        </span>
      </div>
      
      {/* Animated indicator */}
      <div className={`ml-auto w-12 h-6 rounded-full relative transition-all duration-500 ${
        isDark 
          ? 'bg-gradient-to-r from-yellow-400 to-orange-500 shadow-lg shadow-yellow-500/30' 
          : 'bg-gradient-to-r from-blue-500 to-purple-600 shadow-lg shadow-blue-500/30'
      }`}>
        <div className={`absolute top-1 w-4 h-4 bg-white rounded-full shadow-md transition-all duration-500 transform ${
          isDark ? 'translate-x-7' : 'translate-x-1'
        }`}></div>
      </div>
    </button>
  )
}