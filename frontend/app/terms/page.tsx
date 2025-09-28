import React from 'react';

export default function TermsPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              شروط الخدمة
            </h1>
            <p className="text-lg text-gray-600">
              آخر تحديث: 15 يناير 2024
            </p>
          </div>

          <div className="prose prose-lg max-w-none text-right">
            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">1. قبول الشروط</h2>
              <p className="text-gray-700 leading-relaxed mb-4">
                بوصولك واستخدامك لمنصة VEO7، فإنك توافق على الالتزام بهذه الشروط والأحكام. 
                إذا كنت لا توافق على أي من هذه الشروط، يرجى عدم استخدام خدماتنا.
              </p>
              <p className="text-gray-700 leading-relaxed">
                نحتفظ بالحق في تعديل هذه الشروط في أي وقت، وسيتم إشعارك بأي تغييرات جوهرية 
                عبر البريد الإلكتروني أو من خلال إشعار على المنصة.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">2. وصف الخدمة</h2>
              <p className="text-gray-700 leading-relaxed mb-4">
                VEO7 هي منصة لإنتاج المحتوى المرئي والصوتي باستخدام تقنيات الذكاء الاصطناعي. 
                تشمل خدماتنا:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 mr-6">
                <li>تحويل النصوص إلى فيديوهات</li>
                <li>خدمات الترجمة الآلية</li>
                <li>تحويل النص إلى كلام</li>
                <li>معالجة وتحرير الصور</li>
                <li>واجهات برمجة التطبيقات (APIs)</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">3. حساب المستخدم</h2>
              <p className="text-gray-700 leading-relaxed mb-4">
                لاستخدام خدماتنا، يجب عليك إنشاء حساب وتقديم معلومات دقيقة وكاملة. 
                أنت مسؤول عن:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 mr-6">
                <li>الحفاظ على سرية كلمة المرور الخاصة بك</li>
                <li>جميع الأنشطة التي تحدث تحت حسابك</li>
                <li>إشعارنا فوراً بأي استخدام غير مصرح به لحسابك</li>
                <li>تحديث معلومات حسابك للحفاظ على دقتها</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">4. الاستخدام المقبول</h2>
              <p className="text-gray-700 leading-relaxed mb-4">
                يجب عليك استخدام خدماتنا بطريقة قانونية ومسؤولة. يُحظر عليك:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 mr-6">
                <li>إنشاء محتوى مسيء أو غير قانوني أو ضار</li>
                <li>انتهاك حقوق الطبع والنشر أو الملكية الفكرية</li>
                <li>استخدام الخدمة لأغراض احتيالية أو خادعة</li>
                <li>محاولة اختراق أو تعطيل أنظمتنا</li>
                <li>إنشاء حسابات متعددة لتجاوز القيود</li>
                <li>استخدام الخدمة لإنشاء محتوى يحرض على العنف أو الكراهية</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">5. الملكية الفكرية</h2>
              <p className="text-gray-700 leading-relaxed mb-4">
                تحتفظ VEO7 بجميع الحقوق في منصتها وتقنياتها. بالنسبة للمحتوى الذي تنشئه:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 mr-6">
                <li>تحتفظ بملكية المحتوى الأصلي الذي تقدمه</li>
                <li>تمنحنا ترخيصاً لمعالجة وتحسين المحتوى</li>
                <li>تضمن أن لديك الحق في استخدام جميع المواد المقدمة</li>
                <li>تتحمل المسؤولية عن أي انتهاك لحقوق الطبع والنشر</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">6. الدفع والفوترة</h2>
              <p className="text-gray-700 leading-relaxed mb-4">
                بالنسبة للخدمات المدفوعة:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 mr-6">
                <li>الرسوم مستحقة الدفع مقدماً</li>
                <li>لا نقدم استردادات إلا في حالات استثنائية</li>
                <li>قد نغير الأسعار مع إشعار مسبق 30 يوماً</li>
                <li>التأخير في الدفع قد يؤدي إلى تعليق الخدمة</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">7. الخصوصية وحماية البيانات</h2>
              <p className="text-gray-700 leading-relaxed mb-4">
                نحن ملتزمون بحماية خصوصيتك. يرجى مراجعة سياسة الخصوصية الخاصة بنا 
                لفهم كيفية جمع واستخدام وحماية معلوماتك الشخصية.
              </p>
              <p className="text-gray-700 leading-relaxed">
                نستخدم تشفير SSL ومعايير أمان عالية لحماية بياناتك، ولا نشارك 
                معلوماتك الشخصية مع أطراف ثالثة دون موافقتك.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">8. إخلاء المسؤولية</h2>
              <p className="text-gray-700 leading-relaxed mb-4">
                تُقدم خدماتنا "كما هي" دون أي ضمانات صريحة أو ضمنية. نحن لا نضمن:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 mr-6">
                <li>التوفر المستمر للخدمة دون انقطاع</li>
                <li>دقة أو اكتمال المحتوى المُنتج</li>
                <li>خلو الخدمة من الأخطاء أو الفيروسات</li>
                <li>ملاءمة الخدمة لاحتياجاتك الخاصة</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">9. تحديد المسؤولية</h2>
              <p className="text-gray-700 leading-relaxed">
                في أي حال من الأحوال، لن تتجاوز مسؤوليتنا تجاهك المبلغ الذي دفعته 
                لنا خلال الـ 12 شهراً السابقة للحادث. نحن غير مسؤولين عن أي أضرار 
                غير مباشرة أو عرضية أو خاصة أو تبعية.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">10. إنهاء الخدمة</h2>
              <p className="text-gray-700 leading-relaxed mb-4">
                يمكن لأي من الطرفين إنهاء هذه الاتفاقية في أي وقت. نحتفظ بالحق في:
              </p>
              <ul className="list-disc list-inside text-gray-700 space-y-2 mr-6">
                <li>تعليق أو إنهاء حسابك لانتهاك الشروط</li>
                <li>إزالة المحتوى الذي ينتهك سياساتنا</li>
                <li>تعديل أو إيقاف الخدمة مع إشعار مناسب</li>
              </ul>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">11. القانون المطبق</h2>
              <p className="text-gray-700 leading-relaxed">
                تخضع هذه الشروط للقوانين المعمول بها في دولة الإمارات العربية المتحدة. 
                أي نزاع ينشأ عن هذه الاتفاقية سيتم حله من خلال التحكيم أو المحاكم المختصة.
              </p>
            </section>

            <section className="mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">12. معلومات الاتصال</h2>
              <p className="text-gray-700 leading-relaxed mb-4">
                إذا كان لديك أي أسئلة حول هذه الشروط، يرجى التواصل معنا:
              </p>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-gray-700"><strong>البريد الإلكتروني:</strong> legal@veo7.com</p>
                <p className="text-gray-700"><strong>الهاتف:</strong> +971-4-123-4567</p>
                <p className="text-gray-700"><strong>العنوان:</strong> دبي، الإمارات العربية المتحدة</p>
              </div>
            </section>
          </div>

          <div className="mt-12 pt-8 border-t border-gray-200 text-center">
            <p className="text-gray-600">
              بالمتابعة في استخدام خدماتنا، فإنك تؤكد قراءتك وفهمك وموافقتك على هذه الشروط والأحكام.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}