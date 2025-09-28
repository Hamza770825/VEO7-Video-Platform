'use client'

import { useRouter } from 'next/navigation'
import { ArrowLeftIcon, ArrowRightIcon } from '@heroicons/react/24/outline'
import { useLanguage } from '../../app/providers'

interface BackButtonProps {
  href?: string
  text?: string
  className?: string
  variant?: 'default' | 'ghost' | 'minimal'
}

export default function BackButton({ 
  href, 
  text, 
  className = '', 
  variant = 'default' 
}: BackButtonProps) {
  const router = useRouter()
  const { language, isRTL } = useLanguage()

  const handleBack = () => {
    if (href) {
      router.push(href)
    } else {
      router.back()
    }
  }

  const defaultText = language === 'ar' ? 'رجوع' : 'Back'
  const displayText = text || defaultText

  const baseClasses = 'flex items-center space-x-2 transition-colors duration-200'
  
  const variantClasses = {
    default: 'btn-ghost',
    ghost: 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white',
    minimal: 'text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
  }

  return (
    <button
      onClick={handleBack}
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
    >
      {isRTL ? (
        <>
          <ArrowRightIcon className="w-4 h-4 ml-2" />
          <span>{displayText}</span>
        </>
      ) : (
        <>
          <ArrowLeftIcon className="w-4 h-4 mr-2" />
          <span>{displayText}</span>
        </>
      )}
    </button>
  )
}