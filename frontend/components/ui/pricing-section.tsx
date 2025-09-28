'use client'

import { motion } from 'framer-motion'
import { CheckIcon, StarIcon, SparklesIcon } from '@heroicons/react/24/solid'
import { XMarkIcon } from '@heroicons/react/24/outline'

interface PricingSectionProps {
  language: string
  isRTL: boolean
  session?: any
}

export default function PricingSection({ language, isRTL, session }: PricingSectionProps) {
  const plans = [
    {
      name: language === 'ar' ? 'مجاني' : 'Free',
      price: '0',
      period: language === 'ar' ? 'مجاناً للأبد' : 'Forever Free',
      description: language === 'ar' ? 'مثالي للمبتدئين والاستخدام الشخصي' : 'Perfect for beginners and personal use',
      features: [
        language === 'ar' ? '5 فيديوهات شهرياً' : '5 videos per month',
        language === 'ar' ? 'جودة HD (720p)' : 'HD Quality (720p)',
        language === 'ar' ? '10 أصوات مختلفة' : '10 different voices',
        language === 'ar' ? 'دعم 5 لغات' : '5 languages support',
        language === 'ar' ? 'تخزين 1 جيجا' : '1GB storage',
        language === 'ar' ? 'علامة مائية' : 'Watermark included'
      ],
      notIncluded: [
        language === 'ar' ? 'جودة 4K' : '4K Quality',
        language === 'ar' ? 'دعم أولوية' : 'Priority Support',
        language === 'ar' ? 'تصدير بدون علامة مائية' : 'No watermark export'
      ],
      buttonText: language === 'ar' ? 'ابدأ مجاناً' : 'Start Free',
      popular: false,
      color: 'from-gray-500 to-gray-600',
      bgColor: 'from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-900'
    },
    {
      name: language === 'ar' ? 'احترافي' : 'Pro',
      price: '29',
      period: language === 'ar' ? 'شهرياً' : 'per month',
      description: language === 'ar' ? 'للمحترفين ومنشئي المحتوى' : 'For professionals and content creators',
      features: [
        language === 'ar' ? 'فيديوهات غير محدودة' : 'Unlimited videos',
        language === 'ar' ? 'جودة 4K فائقة' : '4K Ultra Quality',
        language === 'ar' ? '50+ صوت طبيعي' : '50+ natural voices',
        language === 'ar' ? 'دعم 50+ لغة' : '50+ languages support',
        language === 'ar' ? 'تخزين 100 جيجا' : '100GB storage',
        language === 'ar' ? 'بدون علامة مائية' : 'No watermark',
        language === 'ar' ? 'تصدير سريع' : 'Fast export',
        language === 'ar' ? 'دعم أولوية' : 'Priority support'
      ],
      notIncluded: [
        language === 'ar' ? 'API متقدم' : 'Advanced API',
        language === 'ar' ? 'تخصيص كامل' : 'Full customization'
      ],
      buttonText: language === 'ar' ? 'اشترك الآن' : 'Subscribe Now',
      popular: true,
      color: 'from-blue-500 to-purple-600',
      bgColor: 'from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20'
    },
    {
      name: language === 'ar' ? 'للشركات' : 'Enterprise',
      price: '99',
      period: language === 'ar' ? 'شهرياً' : 'per month',
      description: language === 'ar' ? 'للشركات والفرق الكبيرة' : 'For companies and large teams',
      features: [
        language === 'ar' ? 'كل ميزات الخطة الاحترافية' : 'All Pro features',
        language === 'ar' ? 'API متقدم' : 'Advanced API',
        language === 'ar' ? 'تخصيص كامل' : 'Full customization',
        language === 'ar' ? 'تخزين غير محدود' : 'Unlimited storage',
        language === 'ar' ? 'فرق متعددة' : 'Multiple teams',
        language === 'ar' ? 'تحليلات متقدمة' : 'Advanced analytics',
        language === 'ar' ? 'دعم مخصص 24/7' : 'Dedicated 24/7 support',
        language === 'ar' ? 'تدريب مخصص' : 'Custom training'
      ],
      notIncluded: [],
      buttonText: language === 'ar' ? 'تواصل معنا' : 'Contact Us',
      popular: false,
      color: 'from-purple-500 to-pink-600',
      bgColor: 'from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20'
    }
  ]

  const faqs = [
    {
      question: language === 'ar' ? 'هل يمكنني تغيير خطتي في أي وقت؟' : 'Can I change my plan anytime?',
      answer: language === 'ar' 
        ? 'نعم، يمكنك ترقية أو تخفيض خطتك في أي وقت. التغييرات ستطبق في دورة الفوترة التالية.'
        : 'Yes, you can upgrade or downgrade your plan anytime. Changes will apply in the next billing cycle.'
    },
    {
      question: language === 'ar' ? 'هل هناك ضمان استرداد الأموال؟' : 'Is there a money-back guarantee?',
      answer: language === 'ar'
        ? 'نعم، نوفر ضمان استرداد الأموال لمدة 30 يوماً لجميع الخطط المدفوعة.'
        : 'Yes, we offer a 30-day money-back guarantee for all paid plans.'
    },
    {
      question: language === 'ar' ? 'ما هي طرق الدفع المتاحة؟' : 'What payment methods are available?',
      answer: language === 'ar'
        ? 'نقبل جميع البطاقات الائتمانية الرئيسية، PayPal، والتحويل البنكي للشركات.'
        : 'We accept all major credit cards, PayPal, and bank transfers for enterprises.'
    }
  ]

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
            className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-purple-100 to-pink-100 dark:from-purple-900 dark:to-pink-900 text-purple-800 dark:text-purple-200 text-sm font-medium mb-4"
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
          >
            <SparklesIcon className="w-4 h-4 mr-2" />
            {language === 'ar' ? 'خطط الأسعار' : 'Pricing Plans'}
          </motion.div>
          
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 dark:text-white mb-4">
            {language === 'ar' ? 'اختر الخطة المناسبة لك' : 'Choose the Right Plan for You'}
          </h2>
          
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            {language === 'ar'
              ? 'خطط مرنة تناسب جميع الاحتياجات، من المبتدئين إلى الشركات الكبيرة'
              : 'Flexible plans that suit all needs, from beginners to large enterprises'
            }
          </p>
        </motion.div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          {plans.map((plan, index) => (
            <motion.div
              key={index}
              className={`relative ${plan.popular ? 'md:scale-105 z-10' : ''}`}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
            >
              {/* Popular Badge */}
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 z-20">
                  <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-4 py-2 rounded-full text-sm font-medium flex items-center">
                    <StarIcon className="w-4 h-4 mr-1" />
                    {language === 'ar' ? 'الأكثر شعبية' : 'Most Popular'}
                  </div>
                </div>
              )}

              {/* Card */}
              <div className={`relative bg-white dark:bg-gray-800 rounded-2xl p-8 h-full border-2 ${
                plan.popular 
                  ? 'border-blue-500 shadow-2xl' 
                  : 'border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600'
              } transition-all duration-300 hover:shadow-xl`}>
                
                {/* Header */}
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                    {plan.name}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-4">
                    {plan.description}
                  </p>
                  <div className="flex items-baseline justify-center">
                    <span className="text-5xl font-bold text-gray-900 dark:text-white">
                      ${plan.price}
                    </span>
                    <span className="text-gray-500 dark:text-gray-400 ml-2">
                      {plan.period}
                    </span>
                  </div>
                </div>

                {/* Features */}
                <div className="mb-8">
                  <ul className="space-y-3">
                    {plan.features.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-center">
                        <CheckIcon className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" />
                        <span className="text-gray-700 dark:text-gray-300">
                          {feature}
                        </span>
                      </li>
                    ))}
                    {plan.notIncluded.map((feature, featureIndex) => (
                      <li key={featureIndex} className="flex items-center opacity-50">
                        <XMarkIcon className="w-5 h-5 text-gray-400 mr-3 flex-shrink-0" />
                        <span className="text-gray-500 dark:text-gray-400">
                          {feature}
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* CTA Button */}
                <motion.button
                  className={`w-full py-3 px-6 rounded-xl font-semibold transition-all duration-300 ${
                    plan.popular
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  {plan.buttonText}
                </motion.button>
              </div>
            </motion.div>
          ))}
        </div>

        {/* FAQ Section */}
        <motion.div
          className="max-w-3xl mx-auto"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: 0.4 }}
        >
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white text-center mb-8">
            {language === 'ar' ? 'الأسئلة الشائعة' : 'Frequently Asked Questions'}
          </h3>
          
          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <motion.div
                key={index}
                className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.1 * index }}
              >
                <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
                  {faq.question}
                </h4>
                <p className="text-gray-600 dark:text-gray-300">
                  {faq.answer}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>

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
              {language === 'ar' ? 'لا تزال غير متأكد؟' : 'Still not sure?'}
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              {language === 'ar'
                ? 'جرب النسخة المجانية أو تواصل معنا للحصول على استشارة مخصصة'
                : 'Try the free version or contact us for a personalized consultation'
              }
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.button
                className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300 shadow-lg hover:shadow-xl"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {language === 'ar' ? 'جرب مجاناً' : 'Try Free'}
              </motion.button>
              <motion.button
                className="border-2 border-blue-600 text-blue-600 dark:text-blue-400 px-8 py-3 rounded-xl font-semibold hover:bg-blue-600 hover:text-white transition-all duration-300"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {language === 'ar' ? 'تواصل معنا' : 'Contact Us'}
              </motion.button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}