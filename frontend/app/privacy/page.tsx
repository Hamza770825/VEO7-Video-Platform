'use client';

import { motion } from 'framer-motion';

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="bg-white rounded-2xl shadow-xl p-8 md:p-12"
        >
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              سياسة الخصوصية
            </h1>
            <p className="text-lg text-gray-600">
              نحن نحترم خصوصيتك ونلتزم بحماية بياناتك الشخصية
            </p>
          </div>

          <div className="space-y-8">
            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                1. المعلومات التي نجمعها
              </h2>
              <div className="text-gray-700 space-y-3">
                <p>نقوم بجمع المعلومات التالية:</p>
                <ul className="list-disc list-inside space-y-2 mr-6">
                  <li>المعلومات الشخصية مثل الاسم والبريد الإلكتروني</li>
                  <li>معلومات الاستخدام والتفاعل مع المنصة</li>
                  <li>البيانات التقنية مثل عنوان IP ونوع المتصفح</li>
                  <li>الملفات والمحتوى الذي تقوم برفعه</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                2. كيفية استخدام المعلومات
              </h2>
              <div className="text-gray-700 space-y-3">
                <p>نستخدم المعلومات المجمعة للأغراض التالية:</p>
                <ul className="list-disc list-inside space-y-2 mr-6">
                  <li>تقديم وتحسين خدماتنا</li>
                  <li>إنشاء ومعالجة مقاطع الفيديو</li>
                  <li>التواصل معك بشأن حسابك والخدمات</li>
                  <li>تحليل الاستخدام لتحسين المنصة</li>
                  <li>ضمان الأمان ومنع الاحتيال</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                3. مشاركة المعلومات
              </h2>
              <div className="text-gray-700 space-y-3">
                <p>لا نقوم ببيع أو تأجير معلوماتك الشخصية لأطراف ثالثة. قد نشارك المعلومات في الحالات التالية:</p>
                <ul className="list-disc list-inside space-y-2 mr-6">
                  <li>مع مقدمي الخدمات الموثوقين لتشغيل المنصة</li>
                  <li>عند الحاجة للامتثال للقوانين</li>
                  <li>لحماية حقوقنا وحقوق المستخدمين</li>
                  <li>في حالة دمج أو استحواذ الشركة</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                4. أمان البيانات
              </h2>
              <div className="text-gray-700 space-y-3">
                <p>نتخذ تدابير أمنية صارمة لحماية بياناتك:</p>
                <ul className="list-disc list-inside space-y-2 mr-6">
                  <li>تشفير البيانات أثناء النقل والتخزين</li>
                  <li>الوصول المحدود للبيانات الشخصية</li>
                  <li>مراقبة أمنية مستمرة</li>
                  <li>نسخ احتياطية آمنة</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                5. حقوقك
              </h2>
              <div className="text-gray-700 space-y-3">
                <p>لديك الحقوق التالية فيما يتعلق ببياناتك:</p>
                <ul className="list-disc list-inside space-y-2 mr-6">
                  <li>الوصول إلى بياناتك الشخصية</li>
                  <li>تصحيح البيانات غير الصحيحة</li>
                  <li>حذف بياناتك الشخصية</li>
                  <li>تقييد معالجة البيانات</li>
                  <li>نقل البيانات</li>
                  <li>الاعتراض على المعالجة</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                6. ملفات تعريف الارتباط
              </h2>
              <div className="text-gray-700 space-y-3">
                <p>نستخدم ملفات تعريف الارتباط (Cookies) لتحسين تجربتك:</p>
                <ul className="list-disc list-inside space-y-2 mr-6">
                  <li>ملفات تعريف ضرورية لتشغيل الموقع</li>
                  <li>ملفات تحليلية لفهم الاستخدام</li>
                  <li>ملفات وظيفية لحفظ التفضيلات</li>
                  <li>يمكنك إدارة ملفات تعريف الارتباط من متصفحك</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                7. الاحتفاظ بالبيانات
              </h2>
              <div className="text-gray-700 space-y-3">
                <p>نحتفظ ببياناتك للمدة اللازمة لتقديم الخدمات أو حسب ما يتطلبه القانون. يمكنك طلب حذف بياناتك في أي وقت.</p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                8. التحديثات على السياسة
              </h2>
              <div className="text-gray-700 space-y-3">
                <p>قد نقوم بتحديث هذه السياسة من وقت لآخر. سنقوم بإشعارك بأي تغييرات مهمة عبر البريد الإلكتروني أو إشعار على المنصة.</p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                9. التواصل معنا
              </h2>
              <div className="text-gray-700 space-y-3">
                <p>إذا كان لديك أي أسئلة حول سياسة الخصوصية، يمكنك التواصل معنا:</p>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p><strong>البريد الإلكتروني:</strong> privacy@veo7.com</p>
                  <p><strong>الهاتف:</strong> +966 11 123 4567</p>
                  <p><strong>العنوان:</strong> الرياض، المملكة العربية السعودية</p>
                </div>
              </div>
            </section>
          </div>

          <div className="mt-12 pt-8 border-t border-gray-200 text-center">
            <p className="text-sm text-gray-500">
              آخر تحديث: {new Date().toLocaleDateString('ar-SA')}
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}