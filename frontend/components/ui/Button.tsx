'use client'

import { forwardRef, ButtonHTMLAttributes } from 'react'
import { motion } from 'framer-motion'
import { cn } from '@/utils/cn'

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg' | 'xl'
  loading?: boolean
  icon?: React.ReactNode
  iconPosition?: 'left' | 'right'
  fullWidth?: boolean
  rounded?: boolean
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({
    className,
    variant = 'primary',
    size = 'md',
    loading = false,
    icon,
    iconPosition = 'left',
    fullWidth = false,
    rounded = false,
    disabled,
    children,
    ...props
  }, ref) => {
    const baseClasses = [
      'inline-flex items-center justify-center font-medium transition-all duration-200',
      'focus:outline-none focus:ring-2 focus:ring-offset-2',
      'disabled:opacity-50 disabled:cursor-not-allowed',
      'relative overflow-hidden',
    ]

    const variantClasses = {
      primary: [
        'bg-gradient-to-r from-primary-600 to-primary-700',
        'hover:from-primary-700 hover:to-primary-800',
        'text-white shadow-lg hover:shadow-xl',
        'focus:ring-primary-500',
      ],
      secondary: [
        'bg-gradient-to-r from-secondary-600 to-secondary-700',
        'hover:from-secondary-700 hover:to-secondary-800',
        'text-white shadow-lg hover:shadow-xl',
        'focus:ring-secondary-500',
      ],
      outline: [
        'border-2 border-gray-300 dark:border-gray-600',
        'hover:border-primary-500 dark:hover:border-primary-400',
        'text-gray-700 dark:text-gray-300',
        'hover:text-primary-600 dark:hover:text-primary-400',
        'focus:ring-primary-500',
        'bg-transparent hover:bg-primary-50 dark:hover:bg-primary-900/20',
      ],
      ghost: [
        'text-gray-700 dark:text-gray-300',
        'hover:text-primary-600 dark:hover:text-primary-400',
        'hover:bg-primary-50 dark:hover:bg-primary-900/20',
        'focus:ring-primary-500',
      ],
      danger: [
        'bg-gradient-to-r from-red-600 to-red-700',
        'hover:from-red-700 hover:to-red-800',
        'text-white shadow-lg hover:shadow-xl',
        'focus:ring-red-500',
      ],
    }

    const sizeClasses = {
      sm: 'px-3 py-1.5 text-sm gap-1.5',
      md: 'px-4 py-2 text-sm gap-2',
      lg: 'px-6 py-3 text-base gap-2.5',
      xl: 'px-8 py-4 text-lg gap-3',
    }

    const roundedClasses = {
      sm: rounded ? 'rounded-full' : 'rounded-md',
      md: rounded ? 'rounded-full' : 'rounded-lg',
      lg: rounded ? 'rounded-full' : 'rounded-xl',
      xl: rounded ? 'rounded-full' : 'rounded-2xl',
    }

    const classes = cn(
      baseClasses,
      variantClasses[variant],
      sizeClasses[size],
      roundedClasses[size],
      fullWidth && 'w-full',
      className
    )

    const LoadingSpinner = () => (
      <motion.div
        className="w-4 h-4 border-2 border-current border-t-transparent rounded-full"
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
      />
    )

    const buttonContent = (
      <>
        {loading && <LoadingSpinner />}
        {!loading && icon && iconPosition === 'left' && icon}
        {children && (
          <span className={loading ? 'opacity-0' : 'opacity-100'}>
            {children}
          </span>
        )}
        {!loading && icon && iconPosition === 'right' && icon}
      </>
    )

    return (
      <motion.button
        ref={ref}
        className={classes}
        disabled={disabled || loading}
        whileHover={{ scale: disabled || loading ? 1 : 1.02 }}
        whileTap={{ scale: disabled || loading ? 1 : 0.98 }}
        transition={{ type: 'spring', stiffness: 400, damping: 17 }}
        {...props}
      >
        {/* Ripple effect */}
        <motion.div
          className="absolute inset-0 bg-white/20 rounded-inherit"
          initial={{ scale: 0, opacity: 0 }}
          whileTap={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.2 }}
        />
        
        {/* Content */}
        <span className="relative z-10 flex items-center justify-center gap-inherit">
          {buttonContent}
        </span>
      </motion.button>
    )
  }
)

Button.displayName = 'Button'

export { Button }