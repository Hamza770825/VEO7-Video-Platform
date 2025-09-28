import React from 'react';
import BackButton from '@/components/ui/BackButton';

export default function HelpPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-100 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <BackButton href="/" />
        </div>
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            مركز المساعدة
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            ابحث عن إجابات لأسئلتك الشائعة أو تعلم كيفية استخدام منصة VEO7 بفعالية
          </p>
        </div>

        {/* Search Bar */}
        <div className="max-w-2xl mx-auto mb-12">
          <div className="relative">
            <input
              type="text"
              placeholder="ابحث عن مساعدة..."
              className="w-full px-6 py-4 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent pl-12"
            />
            <svg className="absolute left-4 top-1/2 transform -translate-y-1/2 w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>

        {/* Quick Links */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
          <div className="bg-white rounded-lg shadow-lg p-6 text-center hover:shadow-xl transition duration-200">
            <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">دليل البداية</h3>
            <p className="text-gray-600 text-sm">تعلم أساسيات استخدام المنصة</p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 text-center hover:shadow-xl transition duration-200">
            <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">إنشاء الفيديو</h3>
            <p className="text-gray-600 text-sm">كيفية إنشاء فيديو احترافي</p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 text-center hover:shadow-xl transition duration-200">
            <div className="w-16 h-16 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">الإعدادات</h3>
            <p className="text-gray-600 text-sm">تخصيص حسابك وتفضيلاتك</p>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6 text-center hover:shadow-xl transition duration-200">
            <div className="w-16 h-16 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192L5.636 18.364M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">حل المشاكل</h3>
            <p className="text-gray-600 text-sm">إصلاح المشاكل الشائعة</p>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">الأسئلة الشائعة</h2>
          
          <div className="space-y-6">
            <div className="border-b border-gray-200 pb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">كيف يمكنني إنشاء فيديو جديد؟</h3>
              <p className="text-gray-600">
                لإنشاء فيديو جديد، انتقل إلى صفحة "إنشاء" من القائمة الرئيسية، ثم أدخل النص الذي تريد تحويله إلى فيديو، 
                اختر اللغة والصوت المفضل، وارفع الصورة إذا كنت تريد. اضغط على "إنشاء الفيديو" وانتظر حتى تكتمل المعالجة.
              </p>
            </div>

            <div className="border-b border-gray-200 pb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">ما هي اللغات المدعومة؟</h3>
              <p className="text-gray-600">
                نحن ندعم أكثر من 50 لغة بما في ذلك العربية، الإنجليزية، الفرنسية، الإسبانية، الألمانية، اليابانية، 
                الصينية، والعديد من اللغات الأخرى. يمكنك رؤية القائمة الكاملة في صفحة إنشاء الفيديو.
              </p>
            </div>

            <div className="border-b border-gray-200 pb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">كم من الوقت يستغرق إنشاء الفيديو؟</h3>
              <p className="text-gray-600">
                عادة ما يستغرق إنشاء الفيديو بين 30 ثانية إلى 3 دقائق، اعتماداً على طول النص وتعقيد المعالجة المطلوبة. 
                ستتلقى إشعاراً عند اكتمال الفيديو.
              </p>
            </div>

            <div className="border-b border-gray-200 pb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">هل يمكنني تحميل الفيديوهات؟</h3>
              <p className="text-gray-600">
                نعم، يمكنك تحميل جميع الفيديوهات التي تنشئها بجودة عالية. انتقل إلى لوحة التحكم الخاصة بك واضغط على 
                زر "تحميل" بجانب أي فيديو تريد حفظه على جهازك.
              </p>
            </div>

            <div className="border-b border-gray-200 pb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">ما هي أنواع الملفات المدعومة للصور؟</h3>
              <p className="text-gray-600">
                نحن ندعم معظم أنواع ملفات الصور الشائعة بما في ذلك JPG، PNG، GIF، WebP، وBMP. 
                الحد الأقصى لحجم الملف هو 10 ميجابايت.
              </p>
            </div>

            <div className="pb-6">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">كيف يمكنني إلغاء اشتراكي؟</h3>
              <p className="text-gray-600">
                يمكنك إلغاء اشتراكك في أي وقت من خلال الانتقال إلى إعدادات الحساب ثم "إدارة الاشتراك". 
                ستحتفظ بالوصول إلى الميزات المدفوعة حتى نهاية فترة الفوترة الحالية.
              </p>
            </div>
          </div>
        </div>

        {/* Contact Support */}
        <div className="bg-blue-50 rounded-lg p-8 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">لم تجد ما تبحث عنه؟</h2>
          <p className="text-gray-600 mb-6">
            فريق الدعم الفني لدينا جاهز لمساعدتك في أي وقت
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition duration-200">
              تواصل مع الدعم
            </button>
            <button className="bg-white text-blue-600 border border-blue-600 px-6 py-3 rounded-lg hover:bg-blue-50 transition duration-200">
              إرسال تذكرة دعم
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}