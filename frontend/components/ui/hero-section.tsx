'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { PlayIcon, SparklesIcon, ArrowRightIcon, CheckIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'
import Image from 'next/image'

interface HeroSectionProps {
  language: string
  isRTL: boolean
  session?: any
}

export default function HeroSection({ language, isRTL, session }: HeroSectionProps) {
  const [currentVideoIndex, setCurrentVideoIndex] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)

  const demoVideos = [
    {
      id: 1,
      title: language === 'ar' ? 'تحريك صورة شخصية' : 'Portrait Animation',
      thumbnail: '/demo/portrait-thumb.jpg',
      video: '/demo/portrait-demo.mp4'
    },
    {
      id: 2,
      title: language === 'ar' ? 'شخصية كرتونية' : 'Cartoon Character',
      thumbnail: '/demo/cartoon-thumb.jpg',
      video: '/demo/cartoon-demo.mp4'
    },
    {
      id: 3,
      title: language === 'ar' ? 'تحريك لوحة فنية' : 'Artistic Portrait',
      thumbnail: '/demo/art-thumb.jpg',
      video: '/demo/art-demo.mp4'
    }
  ]

  const features = [
    language === 'ar' ? 'تحريك الصور بالذكاء الاصطناعي' : 'AI-Powered Animation',
    language === 'ar' ? 'تحويل النص إلى صوت طبيعي' : 'Natural Text-to-Speech',
    language === 'ar' ? 'جودة 4K احترافية' : 'Professional 4K Quality',
    language === 'ar' ? 'أكثر من 50 لغة' : '50+ Languages Support'
  ]

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentVideoIndex((prev) => (prev + 1) % demoVideos.length)
    }, 5000)
    return () => clearInterval(interval)
  }, [demoVideos.length])

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-purple-900" />
      
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <motion.div
          className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-r from-blue-400 to-purple-600 rounded-full opacity-20 blur-3xl"
          animate={{
            scale: [1, 1.2, 1],
            rotate: [0, 180, 360],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "linear"
          }}
        />
        <motion.div
          className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-r from-purple-400 to-pink-600 rounded-full opacity-20 blur-3xl"
          animate={{
            scale: [1.2, 1, 1.2],
            rotate: [360, 180, 0],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: "linear"
          }}
        />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <motion.div
            className={`${isRTL ? 'lg:order-2' : ''}`}
            initial={{ opacity: 0, x: isRTL ? 50 : -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
          >
            {/* Badge */}
            <motion.div
              className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-blue-100 to-purple-100 dark:from-blue-900 dark:to-purple-900 text-blue-800 dark:text-blue-200 text-sm font-medium mb-6"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <SparklesIcon className="w-4 h-4 mr-2" />
              {language === 'ar' ? 'الجيل الجديد من إنتاج الفيديو' : 'Next-Gen Video Creation'}
            </motion.div>

            {/* Main Heading */}
            <motion.h1
              className="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              {language === 'ar' ? (
                <>
                  أنتج فيديوهات
                  <br />
                  <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                    احترافية بالذكاء الاصطناعي
                  </span>
                </>
              ) : (
                <>
                  Create Stunning
                  <br />
                  <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                    AI-Powered Videos
                  </span>
                </>
              )}
            </motion.h1>

            {/* Description */}
            <motion.p
              className="text-xl text-gray-600 dark:text-gray-300 mb-8 leading-relaxed"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              {language === 'ar'
                ? 'حول صورك الثابتة إلى فيديوهات متحركة مذهلة مع إضافة الصوت والتعليق الصوتي. تقنية متقدمة، نتائج احترافية، في دقائق معدودة.'
                : 'Transform static images into stunning animated videos with voice synthesis. Advanced AI technology delivers professional results in minutes, not hours.'
              }
            </motion.p>

            {/* Features List */}
            <motion.div
              className="grid grid-cols-2 gap-3 mb-8"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              {features.map((feature, index) => (
                <div key={index} className="flex items-center">
                  <CheckIcon className="w-5 h-5 text-green-500 mr-2 flex-shrink-0" />
                  <span className="text-gray-700 dark:text-gray-300 text-sm">{feature}</span>
                </div>
              ))}
            </motion.div>

            {/* CTA Buttons */}
            <motion.div
              className="flex flex-col sm:flex-row gap-4"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
            >
              <Link
                href={session ? "/dashboard" : "/auth/register"}
                className="group inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-white bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                {language === 'ar' ? 'ابدأ الإنتاج مجاناً' : 'Start Creating Free'}
                <ArrowRightIcon className={`w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform ${isRTL ? 'rotate-180' : ''}`} />
              </Link>
              
              <button
                onClick={() => setIsPlaying(true)}
                className="inline-flex items-center justify-center px-8 py-4 text-lg font-semibold text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 rounded-xl hover:border-blue-300 dark:hover:border-blue-600 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                <PlayIcon className="w-5 h-5 mr-2" />
                {language === 'ar' ? 'شاهد العرض التوضيحي' : 'Watch Demo'}
              </button>
            </motion.div>

            {/* Trust Indicators */}
            <motion.div
              className="flex items-center mt-8 pt-8 border-t border-gray-200 dark:border-gray-700"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
            >
              <div className="flex -space-x-2 mr-4">
                {[1, 2, 3, 4, 5].map((i) => (
                  <div
                    key={i}
                    className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-400 to-purple-500 border-2 border-white dark:border-gray-800"
                  />
                ))}
              </div>
              <div className="text-sm text-gray-600 dark:text-gray-400">
                {language === 'ar' ? 'انضم إلى أكثر من 10,000 منشئ محتوى' : 'Join 10,000+ content creators'}
              </div>
            </motion.div>
          </motion.div>

          {/* Right Content - Video Demo */}
          <motion.div
            className={`${isRTL ? 'lg:order-1' : ''}`}
            initial={{ opacity: 0, x: isRTL ? -50 : 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, ease: 'easeOut', delay: 0.2 }}
          >
            <div className="relative">
              {/* Main Video Container */}
              <div className="relative aspect-[4/3] rounded-2xl overflow-hidden shadow-2xl bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900">
                <AnimatePresence mode="wait">
                  <motion.div
                    key={currentVideoIndex}
                    className="absolute inset-0"
                    initial={{ opacity: 0, scale: 1.1 }}
                    animate={{ opacity: 1, scale: 1 }}
                    exit={{ opacity: 0, scale: 0.9 }}
                    transition={{ duration: 0.5 }}
                  >
                    <div className="w-full h-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                      <PlayIcon className="w-20 h-20 text-white opacity-80" />
                    </div>
                  </motion.div>
                </AnimatePresence>

                {/* Play Button Overlay */}
                <motion.button
                  className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-20 hover:bg-opacity-30 transition-all duration-200"
                  onClick={() => setIsPlaying(true)}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <div className="w-16 h-16 bg-white bg-opacity-90 rounded-full flex items-center justify-center shadow-lg">
                    <PlayIcon className="w-8 h-8 text-gray-800 ml-1" />
                  </div>
                </motion.button>
              </div>

              {/* Video Thumbnails */}
              <div className="flex justify-center mt-6 space-x-3">
                {demoVideos.map((video, index) => (
                  <motion.button
                    key={video.id}
                    className={`w-16 h-12 rounded-lg overflow-hidden border-2 transition-all duration-200 ${
                      index === currentVideoIndex
                        ? 'border-blue-500 shadow-lg'
                        : 'border-gray-200 dark:border-gray-700 hover:border-gray-300'
                    }`}
                    onClick={() => setCurrentVideoIndex(index)}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <div className="w-full h-full bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-700 dark:to-gray-800" />
                  </motion.button>
                ))}
              </div>

              {/* Floating Elements */}
              <motion.div
                className="absolute -top-4 -right-4 w-8 h-8 bg-yellow-400 rounded-full"
                animate={{
                  y: [0, -10, 0],
                  rotate: [0, 180, 360],
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
              <motion.div
                className="absolute -bottom-4 -left-4 w-6 h-6 bg-pink-400 rounded-full"
                animate={{
                  y: [0, 10, 0],
                  x: [0, 5, 0],
                }}
                transition={{
                  duration: 4,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
            </div>
          </motion.div>
        </div>
      </div>

      {/* Video Modal */}
      <AnimatePresence>
        {isPlaying && (
          <motion.div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-80"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setIsPlaying(false)}
          >
            <motion.div
              className="relative max-w-4xl w-full mx-4"
              initial={{ scale: 0.8, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.8, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="aspect-video rounded-xl overflow-hidden">
                <div className="w-full h-full bg-gray-900 flex items-center justify-center">
                  <PlayIcon className="w-20 h-20 text-white opacity-80" />
                </div>
              </div>
              <button
                className="absolute -top-12 right-0 text-white text-xl hover:text-gray-300"
                onClick={() => setIsPlaying(false)}
              >
                ✕
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  )
}