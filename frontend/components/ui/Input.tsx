'use client'

import { forwardRef, InputHTMLAttributes, useState } from 'react'
import { motion } from 'framer-motion'
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline'
import { cn } from '@/utils/cn'

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helperText?: string
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  variant?: 'default' | 'filled' | 'outlined'
  size?: 'sm' | 'md' | 'lg'
  fullWidth?: boolean
}

const Input = forwardRef<HTMLInputElement, InputProps>(
  ({
    className,
    type,
    label,
    error,
    helperText,
    leftIcon,
    rightIcon,
    variant = 'default',
    size = 'md',
    fullWidth = false,
    disabled,
    ...props
  }, ref) => {
    const [showPassword, setShowPassword] = useState(false)
    const [isFocused, setIsFocused] = useState(false)

    const isPassword = type === 'password'
    const inputType = isPassword && showPassword ? 'text' : type

    const baseClasses = [
      'transition-all duration-200',
      'focus:outline-none',
      'disabled:opacity-50 disabled:cursor-not-allowed',
    ]

    const variantClasses = {
      default: [
        'border border-gray-300 dark:border-gray-600',
        'bg-white dark:bg-gray-800',
        'focus:border-primary-500 dark:focus:border-primary-400',
        'focus:ring-2 focus:ring-primary-500/20',
      ],
      filled: [
        'border-0',
        'bg-gray-100 dark:bg-gray-700',
        'focus:bg-white dark:focus:bg-gray-800',
        'focus:ring-2 focus:ring-primary-500/20',
      ],
      outlined: [
        'border-2 border-gray-300 dark:border-gray-600',
        'bg-transparent',
        'focus:border-primary-500 dark:focus:border-primary-400',
      ],
    }

    const sizeClasses = {
      sm: 'px-3 py-2 text-sm',
      md: 'px-4 py-3 text-base',
      lg: 'px-5 py-4 text-lg',
    }

    const iconSizeClasses = {
      sm: 'w-4 h-4',
      md: 'w-5 h-5',
      lg: 'w-6 h-6',
    }

    const inputClasses = cn(
      baseClasses,
      variantClasses[variant],
      sizeClasses[size],
      'rounded-lg',
      leftIcon && 'pl-10',
      (rightIcon || isPassword) && 'pr-10',
      error && 'border-red-500 focus:border-red-500 focus:ring-red-500/20',
      fullWidth && 'w-full',
      className
    )

    const labelClasses = cn(
      'block text-sm font-medium mb-2',
      error ? 'text-red-600 dark:text-red-400' : 'text-gray-700 dark:text-gray-300',
      disabled && 'opacity-50'
    )

    const helperTextClasses = cn(
      'mt-2 text-sm',
      error ? 'text-red-600 dark:text-red-400' : 'text-gray-500 dark:text-gray-400'
    )

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        {label && (
          <motion.label
            className={labelClasses}
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            {label}
          </motion.label>
        )}

        <div className="relative">
          {leftIcon && (
            <div className={cn(
              'absolute left-3 top-1/2 transform -translate-y-1/2',
              'text-gray-400 dark:text-gray-500',
              isFocused && 'text-primary-500 dark:text-primary-400'
            )}>
              <div className={iconSizeClasses[size]}>
                {leftIcon}
              </div>
            </div>
          )}

          <motion.input
            ref={ref}
            type={inputType}
            className={inputClasses}
            disabled={disabled}
            onFocus={(e) => {
              setIsFocused(true)
              props.onFocus?.(e)
            }}
            onBlur={(e) => {
              setIsFocused(false)
              props.onBlur?.(e)
            }}
            whileFocus={{ scale: 1.01 }}
            transition={{ type: 'spring', stiffness: 400, damping: 17 }}
            {...props}
          />

          {(rightIcon || isPassword) && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
              {isPassword ? (
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className={cn(
                    'text-gray-400 dark:text-gray-500',
                    'hover:text-gray-600 dark:hover:text-gray-300',
                    'focus:outline-none focus:text-primary-500',
                    'transition-colors duration-200'
                  )}
                  tabIndex={-1}
                >
                  <div className={iconSizeClasses[size]}>
                    {showPassword ? <EyeSlashIcon /> : <EyeIcon />}
                  </div>
                </button>
              ) : (
                <div className={cn(
                  'text-gray-400 dark:text-gray-500',
                  isFocused && 'text-primary-500 dark:text-primary-400'
                )}>
                  <div className={iconSizeClasses[size]}>
                    {rightIcon}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {(error || helperText) && (
          <motion.p
            className={helperTextClasses}
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            {error || helperText}
          </motion.p>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'

export { Input }