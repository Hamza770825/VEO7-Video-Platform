'use client'

import { motion } from 'framer-motion'
import { 
  CameraIcon, 
  SpeakerWaveIcon, 
  SparklesIcon, 
  ClockIcon,
  GlobeAltIcon,
  ShieldCheckIcon,
  CloudArrowUpIcon,
  CpuChipIcon
} from '@heroicons/react/24/outline'

interface FeaturesShowcaseProps {
  language: string
  isRTL: boolean
}

export default function FeaturesShowcase({ language, isRTL }: FeaturesShowcaseProps) {
  const features = [
    {
      icon: CameraIcon,
      title: language === 'ar' ? 'تحريك الصور بالذكاء الاصطناعي' : 'AI-Powered Image Animation',
      description: language === 'ar' 
        ? 'تقنية متقدمة لتحريك الصور الثابتة وإضافة الحيوية والواقعية للوجوه والشخصيات'
        : 'Advanced technology to animate static images and add life and realism to faces and characters',
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20'
    },
    {
      icon: SpeakerWaveIcon,
      title: language === 'ar' ? 'تحويل النص إلى صوت طبيعي' : 'Natural Text-to-Speech',
      description: language === 'ar'
        ? 'أصوات طبيعية وواضحة بأكثر من 50 لغة مع تحكم كامل في السرعة والنبرة'
        : 'Natural, clear voices in 50+ languages with full control over speed and tone',
      color: 'from-purple-500 to-pink-500',
      bgColor: 'from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20'
    },
    {
      icon: SparklesIcon,
      title: language === 'ar' ? 'جودة احترافية 4K' : 'Professional 4K Quality',
      description: language === 'ar'
        ? 'فيديوهات عالية الدقة جاهزة للنشر على جميع المنصات الاجتماعية والمهنية'
        : 'High-resolution videos ready for publishing on all social and professional platforms',
      color: 'from-amber-500 to-orange-500',
      bgColor: 'from-amber-50 to-orange-50 dark:from-amber-900/20 dark:to-orange-900/20'
    },
    {
      icon: ClockIcon,
      title: language === 'ar' ? 'سرعة في الإنتاج' : 'Lightning Fast Production',
      description: language === 'ar'
        ? 'أنتج فيديوهاتك في دقائق معدودة بدلاً من ساعات من العمل اليدوي'
        : 'Produce your videos in minutes instead of hours of manual work',
      color: 'from-green-500 to-emerald-500',
      bgColor: 'from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20'
    },
    {
      icon: GlobeAltIcon,
      title: language === 'ar' ? 'دعم متعدد اللغات' : 'Multi-Language Support',
      description: language === 'ar'
        ? 'إنتاج محتوى بأكثر من 50 لغة مع ترجمة تلقائية وتحويل نص إلى صوت'
        : 'Create content in 50+ languages with automatic translation and text-to-speech',
      color: 'from-indigo-500 to-blue-500',
      bgColor: 'from-indigo-50 to-blue-50 dark:from-indigo-900/20 dark:to-blue-900/20'
    },
    {
      icon: ShieldCheckIcon,
      title: language === 'ar' ? 'أمان وخصوصية' : 'Security & Privacy',
      description: language === 'ar'
        ? 'حماية كاملة لبياناتك مع تشفير متقدم وعدم مشاركة المحتوى مع أطراف ثالثة'
        : 'Complete data protection with advanced encryption and no third-party content sharing',
      color: 'from-red-500 to-rose-500',
      bgColor: 'from-red-50 to-rose-50 dark:from-red-900/20 dark:to-rose-900/20'
    },
    {
      icon: CloudArrowUpIcon,
      title: language === 'ar' ? 'تخزين سحابي آمن' : 'Secure Cloud Storage',
      description: language === 'ar'
        ? 'احفظ وشارك فيديوهاتك بأمان مع إمكانية الوصول من أي مكان في العالم'
        : 'Save and share your videos securely with access from anywhere in the world',
      color: 'from-teal-500 to-cyan-500',
      bgColor: 'from-teal-50 to-cyan-50 dark:from-teal-900/20 dark:to-cyan-900/20'
    },
    {
      icon: CpuChipIcon,
      title: language === 'ar' ? 'معالجة ذكية متقدمة' : 'Advanced AI Processing',
      description: language === 'ar'
        ? 'خوارزميات ذكية متطورة لضمان أفضل جودة وأسرع معالجة للفيديوهات'
        : 'Sophisticated AI algorithms ensuring the best quality and fastest video processing',
      color: 'from-violet-500 to-purple-500',
      bgColor: 'from-violet-50 to-purple-50 dark:from-violet-900/20 dark:to-purple-900/20'
    }
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: 'easeOut'
      }
    }
  }

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto">
        {/* Section Header */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
        >
          <motion.div
            className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-blue-100 to-purple-100 dark:from-blue-900 dark:to-purple-900 text-blue-800 dark:text-blue-200 text-sm font-medium mb-4"
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
          >
            <SparklesIcon className="w-4 h-4 mr-2" />
            {language === 'ar' ? 'ميزات متقدمة' : 'Advanced Features'}
          </motion.div>
          
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            {language === 'ar' ? 'كل ما تحتاجه لإنتاج فيديوهات احترافية' : 'Everything You Need for Professional Videos'}
          </h2>
          
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            {language === 'ar'
              ? 'اكتشف مجموعة شاملة من الأدوات المتقدمة والميزات القوية التي تجعل من إنتاج الفيديو عملية سهلة وممتعة'
              : 'Discover a comprehensive suite of advanced tools and powerful features that make video production easy and enjoyable'
            }
          </p>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          className="grid md:grid-cols-2 lg:grid-cols-4 gap-6"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          {features.map((feature, index) => (
            <motion.div
              key={index}
              className="group relative"
              variants={itemVariants}
            >
              <div className={`absolute inset-0 bg-gradient-to-r ${feature.bgColor} rounded-2xl transform group-hover:scale-105 transition-transform duration-300`} />
              
              <div className="relative p-6 h-full">
                {/* Icon */}
                <div className={`w-12 h-12 bg-gradient-to-r ${feature.color} rounded-xl flex items-center justify-center mb-4 shadow-lg`}>
                  <feature.icon className="w-6 h-6 text-white" />
                </div>

                {/* Content */}
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 group-hover:text-gray-700 dark:group-hover:text-gray-200 transition-colors">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
                  {feature.description}
                </p>

                {/* Hover Effect */}
                <div className={`absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r ${feature.color} transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300 rounded-b-2xl`} />
              </div>
            </motion.div>
          ))}
        </motion.div>

        {/* Bottom CTA */}
        <motion.div
          className="text-center mt-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4 }}
        >
          <div className="inline-flex items-center justify-center space-x-4 text-sm text-gray-500 dark:text-gray-400">
            <div className="flex items-center">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2" />
              {language === 'ar' ? 'متاح 24/7' : 'Available 24/7'}
            </div>
            <div className="w-1 h-1 bg-gray-300 rounded-full" />
            <div className="flex items-center">
              <div className="w-2 h-2 bg-blue-500 rounded-full mr-2" />
              {language === 'ar' ? 'دعم فني مجاني' : 'Free Support'}
            </div>
            <div className="w-1 h-1 bg-gray-300 rounded-full" />
            <div className="flex items-center">
              <div className="w-2 h-2 bg-purple-500 rounded-full mr-2" />
              {language === 'ar' ? 'تحديثات مستمرة' : 'Regular Updates'}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}