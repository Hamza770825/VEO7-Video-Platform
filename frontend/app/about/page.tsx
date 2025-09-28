import React from 'react';
import PageLayout from '@/components/ui/PageLayout';
import { useLanguage } from '../providers';

export default function AboutPage() {
  const { language } = useLanguage();
  
  return (
    <PageLayout 
      title={language === 'ar' ? 'عن منصة VEO7' : 'About VEO7'}
      description={language === 'ar' ? 'نحن نؤمن بقوة الذكاء الاصطناعي في تحويل الأفكار إلى فيديوهات احترافية' : 'We believe in the power of AI to transform ideas into professional videos'}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center mb-16">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-6">رؤيتنا</h2>
            <p className="text-lg text-gray-600 mb-6">
              نسعى لجعل إنتاج المحتوى المرئي متاحاً للجميع من خلال تقنيات الذكاء الاصطناعي المتقدمة. 
              نؤمن أن كل شخص يستحق أن يكون لديه القدرة على إنشاء فيديوهات احترافية بسهولة وسرعة.
            </p>
            <p className="text-lg text-gray-600">
              منصة VEO7 تجمع بين أحدث تقنيات الذكاء الاصطناعي وسهولة الاستخدام لتوفر تجربة 
              فريدة في إنشاء المحتوى المرئي.
            </p>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-8">
            <div className="text-center">
              <div className="w-20 h-20 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">الابتكار</h3>
              <p className="text-gray-600">
                نستخدم أحدث التقنيات لتوفير حلول مبتكرة ومتطورة
              </p>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          <div className="text-center">
            <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">فريق متخصص</h3>
            <p className="text-gray-600">
              فريق من الخبراء في الذكاء الاصطناعي وتطوير البرمجيات
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">جودة عالية</h3>
            <p className="text-gray-600">
              نضمن أعلى مستويات الجودة في جميع الفيديوهات المنتجة
            </p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">شغف بالتميز</h3>
            <p className="text-gray-600">
              نحن متحمسون لتقديم أفضل تجربة ممكنة لعملائنا
            </p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-8 mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-6 text-center">قصتنا</h2>
          <div className="max-w-4xl mx-auto">
            <p className="text-lg text-gray-600 mb-6">
              بدأت رحلة VEO7 من فكرة بسيطة: جعل إنتاج الفيديوهات الاحترافية متاحاً للجميع. 
              لاحظنا أن العديد من الأشخاص والشركات يواجهون صعوبات في إنشاء محتوى مرئي عالي الجودة 
              بسبب التكلفة العالية والتعقيد التقني.
            </p>
            <p className="text-lg text-gray-600 mb-6">
              قررنا استخدام قوة الذكاء الاصطناعي لحل هذه المشكلة. بعد سنوات من البحث والتطوير، 
              أطلقنا منصة VEO7 التي تجمع بين أحدث تقنيات الذكاء الاصطناعي وواجهة مستخدم بديهية 
              لتوفر تجربة سلسة في إنشاء الفيديوهات.
            </p>
            <p className="text-lg text-gray-600">
              اليوم، نفخر بخدمة آلاف المستخدمين حول العالم، من المبدعين الفرديين إلى الشركات الكبرى، 
              جميعهم يثقون في VEO7 لإنتاج محتوى مرئي استثنائي.
            </p>
          </div>
        </div>

        <div className="text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-8">انضم إلى رحلتنا</h2>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            كن جزءاً من مستقبل إنتاج المحتوى المرئي واكتشف كيف يمكن للذكاء الاصطناعي أن يحول أفكارك إلى واقع
          </p>
          <button className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition duration-200">
            ابدأ رحلتك معنا
          </button>
        </div>
      </div>
    </PageLayout>
  );
}