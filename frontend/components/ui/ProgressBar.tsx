'use client'

import { motion } from 'framer-motion'
import { cn } from '@/utils/cn'

export interface ProgressBarProps {
  progress: number // 0-100
  size?: 'sm' | 'md' | 'lg'
  variant?: 'default' | 'success' | 'warning' | 'danger'
  showPercentage?: boolean
  label?: string
  animated?: boolean
  striped?: boolean
  className?: string
}

const ProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  size = 'md',
  variant = 'default',
  showPercentage = true,
  label,
  animated = true,
  striped = false,
  className,
}) => {
  const clampedProgress = Math.min(Math.max(progress, 0), 100)

  const sizeClasses = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4',
  }

  const variantClasses = {
    default: 'bg-primary-500',
    success: 'bg-green-500',
    warning: 'bg-yellow-500',
    danger: 'bg-red-500',
  }

  const containerClasses = cn(
    'w-full bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden',
    sizeClasses[size],
    className
  )

  const barClasses = cn(
    'h-full transition-all duration-300 ease-out rounded-full',
    variantClasses[variant],
    striped && 'bg-stripes',
    animated && striped && 'animate-stripes'
  )

  return (
    <div className="w-full">
      {(label || showPercentage) && (
        <div className="flex justify-between items-center mb-2">
          {label && (
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {label}
            </span>
          )}
          {showPercentage && (
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
              {Math.round(clampedProgress)}%
            </span>
          )}
        </div>
      )}

      <div className={containerClasses}>
        <motion.div
          className={barClasses}
          initial={{ width: 0 }}
          animate={{ width: `${clampedProgress}%` }}
          transition={{
            duration: animated ? 0.5 : 0,
            ease: 'easeOut',
          }}
        >
          {/* Shine effect */}
          {animated && (
            <motion.div
              className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
              initial={{ x: '-100%' }}
              animate={{ x: '100%' }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                repeatDelay: 1,
                ease: 'easeInOut',
              }}
            />
          )}
        </motion.div>
      </div>
    </div>
  )
}

export { ProgressBar }