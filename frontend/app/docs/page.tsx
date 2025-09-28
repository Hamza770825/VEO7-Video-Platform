import React from 'react';
import BackButton from '@/components/ui/BackButton';

export default function DocsPage() {
  const sections = [
    {
      title: "البدء السريع",
      icon: "🚀",
      items: [
        { title: "إنشاء حساب جديد", href: "#account" },
        { title: "إعداد مشروعك الأول", href: "#first-project" },
        { title: "رفع الصور والنصوص", href: "#upload" },
        { title: "إنشاء أول فيديو", href: "#first-video" }
      ]
    },
    {
      title: "واجهة برمجة التطبيقات",
      icon: "🔧",
      items: [
        { title: "المصادقة والتوثيق", href: "#auth" },
        { title: "إنشاء الفيديوهات", href: "#video-api" },
        { title: "خدمات الترجمة", href: "#translation-api" },
        { title: "إدارة الملفات", href: "#files-api" }
      ]
    },
    {
      title: "الميزات المتقدمة",
      icon: "⚡",
      items: [
        { title: "تخصيص الأصوات", href: "#voice-customization" },
        { title: "إعدادات الجودة", href: "#quality-settings" },
        { title: "التحكم في السرعة", href: "#speed-control" },
        { title: "الترجمة المتعددة", href: "#multi-translation" }
      ]
    },
    {
      title: "استكشاف الأخطاء",
      icon: "🔍",
      items: [
        { title: "مشاكل شائعة", href: "#common-issues" },
        { title: "رموز الأخطاء", href: "#error-codes" },
        { title: "تحسين الأداء", href: "#performance" },
        { title: "الدعم الفني", href: "#support" }
      ]
    }
  ];

  const quickGuides = [
    {
      title: "إنشاء فيديو من النص",
      description: "تعلم كيفية تحويل النصوص إلى فيديوهات احترافية",
      time: "5 دقائق",
      difficulty: "مبتدئ"
    },
    {
      title: "استخدام API للترجمة",
      description: "دليل شامل لاستخدام خدمات الترجمة عبر API",
      time: "10 دقائق",
      difficulty: "متوسط"
    },
    {
      title: "تخصيص الأصوات",
      description: "كيفية اختيار وتخصيص الأصوات لفيديوهاتك",
      time: "7 دقائق",
      difficulty: "مبتدئ"
    },
    {
      title: "التكامل مع التطبيقات",
      description: "دمج VEO7 مع تطبيقاتك الحالية",
      time: "15 دقائق",
      difficulty: "متقدم"
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-6">
            <BackButton href="/" />
          </div>
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              مركز التوثيق
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              دليل شامل لاستخدام منصة VEO7 وجميع ميزاتها
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar Navigation */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm border p-6 sticky top-8">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">الأقسام</h2>
              <nav className="space-y-4">
                {sections.map((section, index) => (
                  <div key={index}>
                    <div className="flex items-center text-gray-900 font-medium mb-2">
                      <span className="mr-2">{section.icon}</span>
                      {section.title}
                    </div>
                    <ul className="space-y-1 mr-6">
                      {section.items.map((item, itemIndex) => (
                        <li key={itemIndex}>
                          <a
                            href={item.href}
                            className="text-gray-600 hover:text-blue-600 text-sm block py-1 transition duration-200"
                          >
                            {item.title}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </nav>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {/* Search Bar */}
            <div className="bg-white rounded-lg shadow-sm border p-6 mb-8">
              <div className="relative">
                <input
                  type="text"
                  placeholder="ابحث في التوثيق..."
                  className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                  <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Quick Start Guides */}
            <div className="bg-white rounded-lg shadow-sm border p-6 mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">أدلة البدء السريع</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {quickGuides.map((guide, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition duration-200">
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">{guide.title}</h3>
                    <p className="text-gray-600 mb-4">{guide.description}</p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4 space-x-reverse">
                        <span className="text-sm text-gray-500">⏱️ {guide.time}</span>
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          guide.difficulty === 'مبتدئ' ? 'bg-green-100 text-green-800' :
                          guide.difficulty === 'متوسط' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {guide.difficulty}
                        </span>
                      </div>
                      <button className="text-blue-600 hover:text-blue-700 font-medium">
                        ابدأ →
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* API Reference */}
            <div className="bg-white rounded-lg shadow-sm border p-6 mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">مرجع API</h2>
              <div className="space-y-6">
                <div className="border-r-4 border-blue-500 pr-4">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">POST /api/generate-video</h3>
                  <p className="text-gray-600 mb-4">إنشاء فيديو جديد من النص والصورة</p>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <pre className="text-sm text-gray-800 overflow-x-auto">
{`{
  "text": "النص المراد تحويله لفيديو",
  "language": "ar",
  "voice_speed": 1.0,
  "image_file": "base64_encoded_image"
}`}
                    </pre>
                  </div>
                </div>

                <div className="border-r-4 border-green-500 pr-4">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">POST /api/translate</h3>
                  <p className="text-gray-600 mb-4">ترجمة النصوص بين اللغات المختلفة</p>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <pre className="text-sm text-gray-800 overflow-x-auto">
{`{
  "text": "Hello World",
  "source_language": "en",
  "target_language": "ar"
}`}
                    </pre>
                  </div>
                </div>

                <div className="border-r-4 border-purple-500 pr-4">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">GET /api/languages</h3>
                  <p className="text-gray-600 mb-4">الحصول على قائمة اللغات المدعومة</p>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <pre className="text-sm text-gray-800 overflow-x-auto">
{`{
  "languages": [
    {"code": "ar", "name": "العربية"},
    {"code": "en", "name": "English"},
    {"code": "fr", "name": "Français"}
  ]
}`}
                    </pre>
                  </div>
                </div>
              </div>
            </div>

            {/* Code Examples */}
            <div className="bg-white rounded-lg shadow-sm border p-6 mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">أمثلة الكود</h2>
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">JavaScript / Node.js</h3>
                  <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                    <pre className="text-green-400 text-sm">
{`const response = await fetch('https://api.veo7.com/api/generate-video', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    text: 'مرحباً بكم في VEO7',
    language: 'ar',
    voice_speed: 1.0
  })
});

const result = await response.json();
console.log(result);`}
                    </pre>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Python</h3>
                  <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
                    <pre className="text-green-400 text-sm">
{`import requests

url = "https://api.veo7.com/api/generate-video"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "text": "مرحباً بكم في VEO7",
    "language": "ar",
    "voice_speed": 1.0
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
print(result)`}
                    </pre>
                  </div>
                </div>
              </div>
            </div>

            {/* FAQ Section */}
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">الأسئلة الشائعة</h2>
              <div className="space-y-4">
                <div className="border-b border-gray-200 pb-4">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">ما هي الحدود اليومية لاستخدام API؟</h3>
                  <p className="text-gray-600">تختلف الحدود حسب نوع الاشتراك. الحساب المجاني يسمح بـ 100 طلب يومياً، بينما الحسابات المدفوعة تتيح حدود أعلى.</p>
                </div>
                <div className="border-b border-gray-200 pb-4">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">ما هي صيغ الصور المدعومة؟</h3>
                  <p className="text-gray-600">ندعم صيغ JPG، PNG، WebP، وSVG بحد أقصى 10MB لكل صورة.</p>
                </div>
                <div className="border-b border-gray-200 pb-4">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">كم من الوقت يستغرق إنشاء الفيديو؟</h3>
                  <p className="text-gray-600">عادة ما يستغرق إنشاء الفيديو بين 30 ثانية إلى 3 دقائق حسب طول النص وتعقيد المحتوى.</p>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">هل يمكنني تخصيص الأصوات؟</h3>
                  <p className="text-gray-600">نعم، نوفر مجموعة متنوعة من الأصوات الطبيعية بلغات مختلفة مع إمكانية التحكم في السرعة والنبرة.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}