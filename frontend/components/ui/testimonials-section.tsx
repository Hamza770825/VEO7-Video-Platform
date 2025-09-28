'use client'

import { motion } from 'framer-motion'
import { StarIcon } from '@heroicons/react/24/solid'
import { PlayIcon } from '@heroicons/react/24/outline'
import Image from 'next/image'

interface TestimonialsSectionProps {
  language: string
  isRTL: boolean
}

export default function TestimonialsSection({ language, isRTL }: TestimonialsSectionProps) {
  const testimonials = [
    {
      id: 1,
      name: language === 'ar' ? 'أحمد محمد' : 'Ahmed Mohamed',
      role: language === 'ar' ? 'منشئ محتوى' : 'Content Creator',
      company: language === 'ar' ? 'يوتيوب' : 'YouTube',
      content: language === 'ar'
        ? 'VEO7 غيّر طريقة إنتاج المحتوى بالكامل. أصبح بإمكاني إنتاج فيديوهات احترافية في دقائق بدلاً من ساعات!'
        : 'VEO7 completely changed my content production process. I can now create professional videos in minutes instead of hours!',
      rating: 5,
      avatar: '/api/placeholder/64/64',
      videoThumbnail: '/api/placeholder/300/200',
      verified: true
    },
    {
      id: 2,
      name: language === 'ar' ? 'سارة أحمد' : 'Sarah Ahmed',
      role: language === 'ar' ? 'مديرة تسويق' : 'Marketing Manager',
      company: language === 'ar' ? 'شركة تقنية' : 'Tech Company',
      content: language === 'ar'
        ? 'الجودة مذهلة والسرعة لا تصدق. استخدمنا VEO7 لحملتنا الإعلانية وحققنا نتائج رائعة.'
        : 'Amazing quality and incredible speed. We used VEO7 for our advertising campaign and achieved fantastic results.',
      rating: 5,
      avatar: '/api/placeholder/64/64',
      videoThumbnail: '/api/placeholder/300/200',
      verified: true
    },
    {
      id: 3,
      name: language === 'ar' ? 'محمد علي' : 'Mohamed Ali',
      role: language === 'ar' ? 'مدرب أونلاين' : 'Online Trainer',
      company: language === 'ar' ? 'منصة تعليمية' : 'Educational Platform',
      content: language === 'ar'
        ? 'أداة رائعة لإنشاء محتوى تعليمي تفاعلي. طلابي يحبون الفيديوهات المتحركة التي أنتجها.'
        : 'Excellent tool for creating interactive educational content. My students love the animated videos I produce.',
      rating: 5,
      avatar: '/api/placeholder/64/64',
      videoThumbnail: '/api/placeholder/300/200',
      verified: true
    },
    {
      id: 4,
      name: language === 'ar' ? 'فاطمة حسن' : 'Fatima Hassan',
      role: language === 'ar' ? 'مصممة جرافيك' : 'Graphic Designer',
      company: language === 'ar' ? 'وكالة إبداعية' : 'Creative Agency',
      content: language === 'ar'
        ? 'كمصممة، أقدر الجودة العالية والتحكم الدقيق في التفاصيل. VEO7 يوفر كل ما أحتاجه.'
        : 'As a designer, I appreciate the high quality and precise control over details. VEO7 provides everything I need.',
      rating: 5,
      avatar: '/api/placeholder/64/64',
      videoThumbnail: '/api/placeholder/300/200',
      verified: true
    },
    {
      id: 5,
      name: language === 'ar' ? 'عمر خالد' : 'Omar Khaled',
      role: language === 'ar' ? 'رائد أعمال' : 'Entrepreneur',
      company: language === 'ar' ? 'ستارت أب' : 'Startup',
      content: language === 'ar'
        ? 'وفرت علينا آلاف الدولارات في إنتاج الفيديو. الآن نحن ننتج محتوى يومياً بتكلفة أقل.'
        : 'Saved us thousands of dollars in video production. Now we produce daily content at a lower cost.',
      rating: 5,
      avatar: '/api/placeholder/64/64',
      videoThumbnail: '/api/placeholder/300/200',
      verified: true
    },
    {
      id: 6,
      name: language === 'ar' ? 'ليلى محمود' : 'Layla Mahmoud',
      role: language === 'ar' ? 'مؤثرة رقمية' : 'Digital Influencer',
      company: language === 'ar' ? 'إنستغرام' : 'Instagram',
      content: language === 'ar'
        ? 'أحب سهولة الاستخدام والنتائج المذهلة. متابعيني يسألون دائماً عن سر جودة فيديوهاتي!'
        : 'I love the ease of use and amazing results. My followers always ask about the secret to my video quality!',
      rating: 5,
      avatar: '/api/placeholder/64/64',
      videoThumbnail: '/api/placeholder/300/200',
      verified: true
    }
  ]

  const stats = [
    {
      number: '50K+',
      label: language === 'ar' ? 'مستخدم نشط' : 'Active Users'
    },
    {
      number: '1M+',
      label: language === 'ar' ? 'فيديو منتج' : 'Videos Created'
    },
    {
      number: '99%',
      label: language === 'ar' ? 'رضا العملاء' : 'Customer Satisfaction'
    },
    {
      number: '24/7',
      label: language === 'ar' ? 'دعم فني' : 'Support'
    }
  ]

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-800">
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
            className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-green-100 to-blue-100 dark:from-green-900 dark:to-blue-900 text-green-800 dark:text-green-200 text-sm font-medium mb-4"
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
          >
            <StarIcon className="w-4 h-4 mr-2" />
            {language === 'ar' ? 'آراء العملاء' : 'Customer Reviews'}
          </motion.div>
          
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            {language === 'ar' ? 'ماذا يقول عملاؤنا؟' : 'What Our Customers Say?'}
          </h2>
          
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            {language === 'ar'
              ? 'اكتشف كيف ساعد VEO7 آلاف المبدعين في تحقيق أهدافهم وإنتاج محتوى استثنائي'
              : 'Discover how VEO7 has helped thousands of creators achieve their goals and produce exceptional content'
            }
          </p>
        </motion.div>

        {/* Stats */}
        <motion.div
          className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.3 }}
        >
          {stats.map((stat, index) => (
            <div key={index} className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                {stat.number}
              </div>
              <div className="text-gray-600 dark:text-gray-300 text-sm">
                {stat.label}
              </div>
            </div>
          ))}
        </motion.div>

        {/* Testimonials Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <motion.div
              key={testimonial.id}
              className="group relative"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
            >
              {/* Card */}
              <div className="bg-gray-50 dark:bg-gray-900 rounded-2xl p-6 h-full border border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600 transition-all duration-300 hover:shadow-xl">
                {/* Quote Icon */}
                <div className="flex justify-between items-start mb-4">
                  <svg className="w-8 h-8 text-blue-500 opacity-50" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"/>
                </svg>
                  <div className="flex">
                    {[...Array(testimonial.rating)].map((_, i) => (
                      <StarIcon key={i} className="w-4 h-4 text-yellow-400" />
                    ))}
                  </div>
                </div>

                {/* Content */}
                <p className="text-gray-700 dark:text-gray-300 mb-6 leading-relaxed">
                  "{testimonial.content}"
                </p>

                {/* Video Thumbnail */}
                <div className="relative mb-6 rounded-lg overflow-hidden group-hover:scale-105 transition-transform duration-300">
                  <div className="aspect-video bg-gradient-to-br from-blue-100 to-purple-100 dark:from-blue-900 dark:to-purple-900 flex items-center justify-center">
                    <div className="w-12 h-12 bg-white dark:bg-gray-800 rounded-full flex items-center justify-center shadow-lg">
                      <PlayIcon className="w-6 h-6 text-blue-600 dark:text-blue-400 ml-1" />
                    </div>
                  </div>
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all duration-300" />
                </div>

                {/* Author */}
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-semibold mr-4">
                    {testimonial.name.charAt(0)}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center">
                      <h4 className="font-semibold text-gray-900 dark:text-white">
                        {testimonial.name}
                      </h4>
                      {testimonial.verified && (
                        <div className="w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center ml-2">
                          <svg className="w-2.5 h-2.5 text-white" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                        </div>
                      )}
                    </div>
                    <p className="text-sm text-gray-500 dark:text-gray-400">
                      {testimonial.role} • {testimonial.company}
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Bottom CTA */}
        <motion.div
          className="text-center mt-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.6 }}
        >
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-2xl p-8">
            <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
              {language === 'ar' ? 'انضم إلى آلاف المبدعين الراضين' : 'Join Thousands of Satisfied Creators'}
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              {language === 'ar'
                ? 'ابدأ رحلتك في إنتاج فيديوهات احترافية اليوم'
                : 'Start your journey in professional video production today'
              }
            </p>
            <motion.button
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {language === 'ar' ? 'ابدأ مجاناً الآن' : 'Start Free Now'}
            </motion.button>
          </div>
        </motion.div>
      </div>
    </section>
  )
}