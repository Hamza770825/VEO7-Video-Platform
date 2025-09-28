import React from 'react';

export default function StatusPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            حالة النظام
          </h1>
          <p className="text-xl text-gray-600">
            تحقق من حالة جميع خدمات منصة VEO7 في الوقت الفعلي
          </p>
        </div>

        {/* Overall Status */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900">الحالة العامة</h2>
              <p className="text-gray-600">جميع الأنظمة تعمل بشكل طبيعي</p>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-green-500 rounded-full mr-2"></div>
              <span className="text-green-600 font-semibold">متاح</span>
            </div>
          </div>
        </div>

        {/* Services Status */}
        <div className="space-y-4 mb-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">خدمة إنشاء الفيديو</h3>
                <p className="text-gray-600">معالجة وإنتاج الفيديوهات</p>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <span className="text-green-600 font-medium">متاح</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">خدمة الترجمة</h3>
                <p className="text-gray-600">ترجمة النصوص متعددة اللغات</p>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <span className="text-green-600 font-medium">متاح</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">خدمة تحويل النص إلى صوت</h3>
                <p className="text-gray-600">إنتاج الأصوات الطبيعية</p>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <span className="text-green-600 font-medium">متاح</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">خدمة معالجة الصور</h3>
                <p className="text-gray-600">تحسين وتعديل الصور</p>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <span className="text-green-600 font-medium">متاح</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">قاعدة البيانات</h3>
                <p className="text-gray-600">تخزين واسترجاع البيانات</p>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <span className="text-green-600 font-medium">متاح</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">نظام المصادقة</h3>
                <p className="text-gray-600">تسجيل الدخول وإدارة الحسابات</p>
              </div>
              <div className="flex items-center">
                <div className="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
                <span className="text-yellow-600 font-medium">صيانة مجدولة</span>
              </div>
            </div>
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">مقاييس الأداء</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">99.9%</div>
              <div className="text-gray-600">وقت التشغيل</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">1.2s</div>
              <div className="text-gray-600">متوسط وقت الاستجابة</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600 mb-2">45s</div>
              <div className="text-gray-600">متوسط وقت إنتاج الفيديو</div>
            </div>
          </div>
        </div>

        {/* Recent Incidents */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">الأحداث الأخيرة</h2>
          <div className="space-y-4">
            <div className="flex items-start">
              <div className="w-3 h-3 bg-green-500 rounded-full mt-2 mr-3"></div>
              <div>
                <div className="font-semibold text-gray-900">تم حل مشكلة بطء الترجمة</div>
                <div className="text-gray-600 text-sm">منذ 2 ساعة - تم إصلاح مشكلة كانت تسبب بطء في خدمة الترجمة</div>
              </div>
            </div>
            <div className="flex items-start">
              <div className="w-3 h-3 bg-yellow-500 rounded-full mt-2 mr-3"></div>
              <div>
                <div className="font-semibold text-gray-900">صيانة مجدولة لنظام المصادقة</div>
                <div className="text-gray-600 text-sm">منذ 6 ساعات - صيانة روتينية لتحسين الأداء</div>
              </div>
            </div>
            <div className="flex items-start">
              <div className="w-3 h-3 bg-green-500 rounded-full mt-2 mr-3"></div>
              <div>
                <div className="font-semibold text-gray-900">تحديث خدمة إنشاء الفيديو</div>
                <div className="text-gray-600 text-sm">منذ يوم واحد - تحسينات على سرعة المعالجة</div>
              </div>
            </div>
          </div>
        </div>

        {/* Subscribe to Updates */}
        <div className="bg-blue-50 rounded-lg p-6 text-center">
          <h2 className="text-xl font-bold text-gray-900 mb-4">اشترك في التحديثات</h2>
          <p className="text-gray-600 mb-4">احصل على إشعارات فورية عند حدوث أي تغييرات في حالة النظام</p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center max-w-md mx-auto">
            <input
              type="email"
              placeholder="بريدك الإلكتروني"
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition duration-200">
              اشترك
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}