'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion, AnimatePresence } from 'framer-motion'
import { toast } from 'react-hot-toast'
import {
  CloudArrowUpIcon,
  PhotoIcon,
  XMarkIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline'

interface FileUploadProps {
  onFileSelect: (file: File) => void
  onFileRemove: () => void
  selectedFile: File | null
  filePreview: string | null
  acceptedTypes?: Record<string, string[]>
  maxSize?: number // in bytes
  className?: string
  language?: 'ar' | 'en'
}

const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  onFileRemove,
  selectedFile,
  filePreview,
  acceptedTypes = {
    'image/*': ['.jpeg', '.jpg', '.png', '.webp', '.gif']
  },
  maxSize = 10 * 1024 * 1024, // 10MB default
  className = '',
  language = 'ar'
}) => {
  const [uploadProgress, setUploadProgress] = useState(0)
  const [isUploading, setIsUploading] = useState(false)

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileTypeIcon = (file: File) => {
    if (file.type.startsWith('image/')) {
      return <PhotoIcon className="w-8 h-8 text-blue-500" />
    }
    return <PhotoIcon className="w-8 h-8 text-gray-500" />
  }

  const onDrop = useCallback((acceptedFiles: File[], rejectedFiles: any[]) => {
    if (rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0]
      if (rejection.errors[0]?.code === 'file-too-large') {
        toast.error(
          language === 'ar' 
            ? `حجم الملف كبير جداً (الحد الأقصى ${formatFileSize(maxSize)})`
            : `File size too large (max ${formatFileSize(maxSize)})`
        )
      } else if (rejection.errors[0]?.code === 'file-invalid-type') {
        toast.error(
          language === 'ar' 
            ? 'نوع الملف غير مدعوم'
            : 'File type not supported'
        )
      }
      return
    }

    const file = acceptedFiles[0]
    if (file) {
      setIsUploading(true)
      setUploadProgress(0)

      // Simulate upload progress
      const interval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval)
            setIsUploading(false)
            onFileSelect(file)
            toast.success(
              language === 'ar' 
                ? 'تم رفع الملف بنجاح'
                : 'File uploaded successfully'
            )
            return 100
          }
          return prev + 10
        })
      }, 100)
    }
  }, [onFileSelect, maxSize, language])

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: acceptedTypes,
    multiple: false,
    maxSize
  })

  const handleRemoveFile = () => {
    setUploadProgress(0)
    setIsUploading(false)
    onFileRemove()
  }

  return (
    <div className={`w-full ${className}`}>
      <AnimatePresence mode="wait">
        {!selectedFile ? (
          <motion.div
            key="upload-area"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            {...getRootProps()}
            className={`
              relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer
              transition-all duration-300 ease-in-out
              ${isDragActive && !isDragReject 
                ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
                : isDragReject 
                ? 'border-red-500 bg-red-50 dark:bg-red-900/20'
                : 'border-gray-300 dark:border-gray-600 hover:border-blue-400 dark:hover:border-blue-500'
              }
              ${isUploading ? 'pointer-events-none' : ''}
            `}
          >
            <input {...getInputProps()} />
            
            <div className="flex flex-col items-center space-y-4">
              <motion.div
                animate={isDragActive ? { scale: 1.1 } : { scale: 1 }}
                transition={{ duration: 0.2 }}
                className={`
                  p-4 rounded-full
                  ${isDragActive && !isDragReject 
                    ? 'bg-blue-100 dark:bg-blue-900/30' 
                    : isDragReject 
                    ? 'bg-red-100 dark:bg-red-900/30'
                    : 'bg-gray-100 dark:bg-gray-800'
                  }
                `}
              >
                {isDragReject ? (
                  <ExclamationTriangleIcon className="w-8 h-8 text-red-500" />
                ) : (
                  <CloudArrowUpIcon 
                    className={`w-8 h-8 ${
                      isDragActive ? 'text-blue-500' : 'text-gray-400'
                    }`} 
                  />
                )}
              </motion.div>

              <div className="space-y-2">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {language === 'ar' 
                    ? isDragActive 
                      ? 'اتركه هنا...' 
                      : 'اسحب وأفلت الملف هنا'
                    : isDragActive 
                      ? 'Drop it here...' 
                      : 'Drag & drop your file here'
                  }
                </h3>
                
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {language === 'ar' 
                    ? 'أو انقر للاختيار من جهازك'
                    : 'or click to select from your device'
                  }
                </p>

                <p className="text-xs text-gray-400 dark:text-gray-500">
                  {language === 'ar' 
                    ? `الحد الأقصى: ${formatFileSize(maxSize)}`
                    : `Max size: ${formatFileSize(maxSize)}`
                  }
                </p>
              </div>

              {/* Upload Progress */}
              {isUploading && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="w-full max-w-xs"
                >
                  <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
                    <span>
                      {language === 'ar' ? 'جاري الرفع...' : 'Uploading...'}
                    </span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <motion.div
                      className="bg-blue-500 h-2 rounded-full"
                      initial={{ width: 0 }}
                      animate={{ width: `${uploadProgress}%` }}
                      transition={{ duration: 0.1 }}
                    />
                  </div>
                </motion.div>
              )}
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="file-preview"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="relative border-2 border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20 rounded-xl p-6"
          >
            <div className="flex items-start space-x-4 rtl:space-x-reverse">
              <div className="flex-shrink-0">
                {filePreview ? (
                  <div className="relative">
                    <img
                      src={filePreview}
                      alt="Preview"
                      className="w-16 h-16 object-cover rounded-lg"
                    />
                    <div className="absolute -top-2 -right-2 bg-green-500 rounded-full p-1">
                      <CheckCircleIcon className="w-4 h-4 text-white" />
                    </div>
                  </div>
                ) : (
                  <div className="w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-lg flex items-center justify-center">
                    {getFileTypeIcon(selectedFile)}
                  </div>
                )}
              </div>

              <div className="flex-1 min-w-0">
                <h4 className="text-sm font-medium text-gray-900 dark:text-white truncate">
                  {selectedFile.name}
                </h4>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {formatFileSize(selectedFile.size)}
                </p>
                <div className="flex items-center mt-2">
                  <CheckCircleIcon className="w-4 h-4 text-green-500 mr-2" />
                  <span className="text-sm text-green-600 dark:text-green-400">
                    {language === 'ar' ? 'تم الرفع بنجاح' : 'Upload successful'}
                  </span>
                </div>
              </div>

              <button
                onClick={handleRemoveFile}
                className="flex-shrink-0 p-2 text-gray-400 hover:text-red-500 transition-colors duration-200"
                title={language === 'ar' ? 'إزالة الملف' : 'Remove file'}
              >
                <XMarkIcon className="w-5 h-5" />
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default FileUpload