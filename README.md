# VEO7 Video Platform 🎬

<div align="center">

![VEO7 Logo](https://via.placeholder.com/200x80/6366f1/ffffff?text=VEO7)

**منصة إنشاء الفيديوهات الناطقة بالذكاء الاصطناعي**

*A revolutionary AI-powered talking video creation platform*

[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)

</div>

## 🌟 المميزات الرئيسية

### 🎯 إنشاء الفيديوهات
- **تحويل النص إلى كلام** - دعم متعدد اللغات مع أصوات ذكورية وأنثوية
- **تحريك الوجوه** - تقنية AI متقدمة لتحريك الصور الثابتة
- **جودة عالية** - خيارات متعددة للجودة (منخفضة، متوسطة، عالية)
- **معاينة فورية** - مشاهدة النتيجة قبل التصدير النهائي

### 🤖 ميزات الذكاء الاصطناعي المتقدمة ✨ **جديد!**
- **SadTalker** - تحريك الوجوه بتقنية متطورة لإنشاء فيديوهات ناطقة واقعية
- **Wav2Lip** - مزامنة حركة الشفاه مع الصوت بدقة عالية
- **Real-ESRGAN** - تحسين جودة الصور بالذكاء الاصطناعي (4x upscaling)
- **AI Studio** - استوديو متكامل لجميع أدوات الذكاء الاصطناعي
- **معالجة GPU** - دعم CUDA للمعالجة السريعة
- **إدارة النماذج** - تحميل وإدارة نماذج AI تلقائياً

### 🌐 دعم متعدد اللغات
- **العربية** - دعم كامل للغة العربية مع RTL
- **الإنجليزية** - واجهة وأصوات إنجليزية
- **لغات إضافية** - الإسبانية، الفرنسية، الألمانية، وأكثر

### 🎨 واجهة مستخدم حديثة ✨ **جديد!**
- **تصميم متجاوب** - يعمل على جميع الأجهزة
- **الوضع المظلم** - تبديل سلس بين الأوضاع
- **رسوم متحركة متقدمة** - تجربة مستخدم سلسة مع Framer Motion
- **تأثيرات احترافية** - خلفيات متدرجة وتأثيرات بصرية مذهلة
- **تفاعلات متطورة** - hover effects وانتقالات سلسة
- **تأثيرات الجسيمات** - عناصر عائمة وتأثيرات ضوئية
- **إمكانية الوصول** - متوافق مع معايير الوصول WCAG

### 🔐 المصادقة والأمان
- **مصادقة Supabase** - نظام مصادقة آمن ومتقدم
- **Google OAuth** - تسجيل دخول سريع بحساب Google
- **حماية البيانات** - تشفير شامل للبيانات الحساسة
- **إدارة الجلسات** - تتبع آمن لجلسات المستخدمين

## 🏗️ البنية التقنية

### Frontend (Next.js 14)
```
frontend/
├── app/                    # App Router (Next.js 14)
│   ├── auth/              # صفحات المصادقة
│   ├── dashboard/         # لوحة التحكم
│   ├── create/            # إنشاء الفيديوهات
│   └── layout.tsx         # التخطيط الرئيسي
├── components/            # المكونات القابلة للإعادة
│   └── ui/               # مكونات واجهة المستخدم
├── utils/                # الأدوات المساعدة
│   ├── supabase.ts       # تكوين Supabase
│   └── api.ts            # عميل API
└── styles/               # ملفات التنسيق
```

### Backend (FastAPI)
```
backend/
├── main.py               # نقطة دخول التطبيق
├── database.py           # تكوين قاعدة البيانات
├── services/             # خدمات المعالجة
│   ├── audio_service.py  # خدمة الصوت
│   ├── video_service.py  # خدمة الفيديو
│   └── translation_service.py # خدمة الترجمة
├── database/             # ملفات قاعدة البيانات
│   ├── schema.sql        # هيكل قاعدة البيانات
│   └── seed.sql          # بيانات التجربة
└── requirements.txt      # متطلبات Python
```

## ✨ التحسينات الاحترافية الجديدة

### 🎨 تأثيرات بصرية متقدمة
- **خلفيات متدرجة متحركة** - تأثيرات Aurora، Cyberpunk، Holographic
- **عناصر عائمة** - جسيمات ضوئية مع حركة كونية
- **تأثيرات الضبابية** - backdrop-blur وتدرجات الشفافية
- **رسوم متحركة سلسة** - استخدام Framer Motion للحركات المتقدمة

### 🖱️ تفاعلات متطورة
- **تأثيرات Hover** - تكبير، دوران، توهج للعناصر التفاعلية
- **انتقالات سلسة** - تحولات ناعمة بين الحالات
- **تأثيرات التركيز** - تحسينات بصرية للوصولية
- **رسوم متحركة للتحميل** - مؤشرات تحميل جذابة

### 🎯 تحسينات الصفحات
- **لوحة التحكم** - تدرجات Space مع تأثيرات متحركة
- **إنشاء الفيديو** - خلفيات طبيعية (Forest, Ice, Gold)
- **تسجيل الدخول** - تدرجات عصرية (Cyberpunk, Neon, Electric)
- **التسجيل** - تدرجات متنوعة (Space, Sunset, Ocean)

### 📱 تحسينات الأداء
- **تحسين GPU** - استخدام hardware acceleration
- **تحميل تدريجي** - lazy loading للتأثيرات الثقيلة
- **إدارة الذاكرة** - تنظيف فعال للموارد
- **تجاوب محسن** - تأثيرات متكيفة مع حجم الشاشة

> 📖 **للمزيد من التفاصيل**: راجع [دليل التحسينات الاحترافية](./PROFESSIONAL_UI_ENHANCEMENTS.md) و [التقرير التقني](./TECHNICAL_IMPLEMENTATION_REPORT.md)

## 🚀 التثبيت والتشغيل

### المتطلبات الأساسية
- **Node.js** 18+ 
- **Python** 3.11+
- **PostgreSQL** 14+
- **FFmpeg** (لمعالجة الفيديو)
- **حساب Supabase**

### 1. استنساخ المشروع
```bash
git clone https://github.com/your-username/VEO7-Video-Platform.git
cd VEO7-Video-Platform
```

### 2. إعداد Backend
```bash
cd backend

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate     # Windows

# تثبيت المتطلبات
pip install -r requirements.txt

# نسخ ملف البيئة
cp .env.example .env
# قم بتحرير .env وإضافة المتغيرات المطلوبة

# تشغيل الخادم
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. إعداد Frontend
```bash
cd frontend

# تثبيت المتطلبات
npm install

# نسخ ملف البيئة
cp .env.example .env.local
# قم بتحرير .env.local وإضافة المتغيرات المطلوبة

# تشغيل الخادم
npm run dev
```

### 4. إعداد قاعدة البيانات
```sql
-- في Supabase SQL Editor
-- تشغيل ملف schema.sql
\i backend/database/schema.sql

-- تشغيل ملف seed.sql (اختياري للبيانات التجريبية)
\i backend/database/seed.sql
```

## 🔧 التكوين

### متغيرات البيئة - Backend
```env
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_key

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/veo7

# Security
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage
UPLOAD_DIR=./uploads
OUTPUT_DIR=./outputs
MAX_FILE_SIZE=104857600

# External APIs (اختياري)
OPENAI_API_KEY=your_openai_key
GOOGLE_CLOUD_API_KEY=your_google_key
```

### متغيرات البيئة - Frontend
```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key

# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# App Configuration
NEXT_PUBLIC_APP_NAME=VEO7
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Feature Flags
NEXT_PUBLIC_GOOGLE_AUTH_ENABLED=true
NEXT_PUBLIC_ANALYTICS_ENABLED=false
```

## 🐳 Docker

### تشغيل Backend بـ Docker
```bash
cd backend
docker build -t veo7-backend .
docker run -p 8000:8000 --env-file .env veo7-backend
```

### Docker Compose (قريباً)
```bash
docker-compose up -d
```

## 📊 قاعدة البيانات

### الجداول الرئيسية
- **user_profiles** - ملفات المستخدمين الشخصية
- **videos** - بيانات الفيديوهات والإعدادات
- **video_processing_logs** - سجلات معالجة الفيديو
- **video_views** - إحصائيات المشاهدة
- **system_settings** - إعدادات النظام

### العلاقات
```mermaid
erDiagram
    user_profiles ||--o{ videos : creates
    videos ||--o{ video_processing_logs : has
    videos ||--o{ video_views : receives
    user_profiles ||--o{ user_sessions : has
```

## 🎨 التصميم والواجهة

### نظام الألوان
```css
:root {
  --primary: #6366f1;      /* البنفسجي الأساسي */
  --secondary: #8b5cf6;    /* البنفسجي الثانوي */
  --accent: #06b6d4;       /* الأزرق المميز */
  --success: #10b981;      /* الأخضر */
  --warning: #f59e0b;      /* الأصفر */
  --danger: #ef4444;       /* الأحمر */
}
```

### الخطوط
- **Inter** - الخط الأساسي للواجهة
- **Noto Sans Arabic** - دعم اللغة العربية
- **JetBrains Mono** - الكود والنصوص التقنية

## 🔌 API Documentation

### نقاط النهاية الرئيسية

#### المصادقة
```http
POST /api/auth/login
POST /api/auth/register
POST /api/auth/logout
GET  /api/auth/me
```

#### الفيديوهات
```http
GET    /api/videos              # قائمة الفيديوهات
POST   /api/videos/create       # إنشاء فيديو جديد
GET    /api/videos/{id}         # تفاصيل فيديو
PUT    /api/videos/{id}         # تحديث فيديو
DELETE /api/videos/{id}         # حذف فيديو
GET    /api/videos/{id}/status  # حالة المعالجة
```

#### الصوت
```http
POST /api/audio/generate        # توليد صوت من نص
POST /api/audio/upload          # رفع ملف صوتي
```

#### الترجمة
```http
POST /api/translation/translate # ترجمة النص
POST /api/translation/detect    # اكتشاف اللغة
GET  /api/translation/languages # اللغات المدعومة
```

## 🧪 الاختبار

### تشغيل الاختبارات
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### اختبارات التكامل
```bash
# End-to-end tests
npm run test:e2e
```

## 📈 الأداء والتحسين

### تحسينات Frontend
- **Code Splitting** - تقسيم الكود لتحميل أسرع
- **Image Optimization** - تحسين الصور تلقائياً
- **Caching** - تخزين مؤقت ذكي
- **Bundle Analysis** - تحليل حجم الحزم

### تحسينات Backend
- **Async Processing** - معالجة غير متزامنة
- **Database Indexing** - فهرسة محسنة
- **Caching Layer** - طبقة تخزين مؤقت
- **Rate Limiting** - تحديد معدل الطلبات

## 🔒 الأمان

### إجراءات الحماية
- **JWT Authentication** - مصادقة آمنة
- **Rate Limiting** - منع الهجمات
- **Input Validation** - التحقق من المدخلات
- **CORS Configuration** - تكوين CORS آمن
- **SQL Injection Prevention** - منع حقن SQL

## 🌍 النشر

### Vercel (Frontend)
```bash
npm run build
vercel --prod
```

### Railway/Heroku (Backend)
```bash
# إعداد متغيرات البيئة
# رفع الكود
git push heroku main
```

### Supabase (Database)
- إنشاء مشروع جديد
- تشغيل ملفات SQL
- تكوين Storage buckets

## 🤝 المساهمة

نرحب بمساهماتكم! يرجى اتباع الخطوات التالية:

1. **Fork** المشروع
2. إنشاء **branch** جديد (`git checkout -b feature/amazing-feature`)
3. **Commit** التغييرات (`git commit -m 'Add amazing feature'`)
4. **Push** إلى البرانش (`git push origin feature/amazing-feature`)
5. فتح **Pull Request**

### إرشادات المساهمة
- اتبع معايير الكود الموجودة
- أضف اختبارات للميزات الجديدة
- حدث التوثيق عند الحاجة
- استخدم رسائل commit واضحة

## 📝 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

## 👥 الفريق

- **المطور الرئيسي** - [اسمك](https://github.com/yourusername)
- **مصمم UI/UX** - [اسم المصمم](https://github.com/designer)
- **مطور Backend** - [اسم المطور](https://github.com/backend-dev)

## 📞 التواصل والدعم

- **البريد الإلكتروني**: support@veo7.com
- **Discord**: [رابط الخادم](https://discord.gg/veo7)
- **Twitter**: [@VEO7Platform](https://twitter.com/VEO7Platform)
- **Documentation**: [docs.veo7.com](https://docs.veo7.com)

## 🗺️ خارطة الطريق

### الإصدار 1.0 ✅
- [x] إنشاء الفيديوهات الأساسية
- [x] دعم متعدد اللغات
- [x] واجهة مستخدم حديثة
- [x] نظام المصادقة

### الإصدار 1.1 🚧
- [ ] تحسين جودة الصوت
- [ ] إضافة المزيد من الأصوات
- [ ] تحسين الأداء
- [ ] إضافة Analytics

### الإصدار 2.0 📋
- [ ] API عامة
- [ ] تطبيق الجوال
- [ ] معالجة الدفعات
- [ ] أصوات مخصصة

---

<div align="center">

**صنع بـ ❤️ في المملكة العربية السعودية**

*Made with ❤️ in Saudi Arabia*

</div>

## 🚀 المميزات الرئيسية

- **تحريك الصور**: تحويل الصور الثابتة إلى فيديوهات متحركة باستخدام AI
- **توليد الصوت**: تحويل النص إلى كلام بجودة عالية ودعم متعدد اللغات
- **واجهة احترافية**: تصميم حديث وسهل الاستخدام شبيه بـ veo2.org
- **مصادقة آمنة**: نظام تسجيل دخول متقدم عبر Supabase
- **تخزين سحابي**: حفظ ومشاركة الفيديوهات عبر Supabase Storage
- **لوحة تحكم**: إدارة شاملة للمشاريع والفيديوهات

## 🛠️ التقنيات المستخدمة

### Backend
- **FastAPI**: إطار عمل Python سريع وحديث
- **gTTS**: تحويل النص إلى كلام
- **SadTalker/Wav2Lip**: تحريك الصور بالصوت
- **Deep Translator**: دعم الترجمة متعددة اللغات
- **Supabase**: قاعدة البيانات والمصادقة

### Frontend
- **Next.js 14**: إطار عمل React متقدم
- **TailwindCSS**: تصميم سريع ومرن
- **Framer Motion**: رسوم متحركة سلسة
- **React Player**: مشغل فيديو متقدم
- **React Dropzone**: رفع الملفات بسهولة

### DevOps & Deployment
- **Docker**: حاويات للتطبيق
- **Vercel**: نشر Frontend
- **Render/Railway**: نشر Backend
- **Supabase**: قاعدة البيانات والتخزين

## 📁 هيكل المشروع

```
VEO7-Video-Platform/
├── backend/                 # خدمات Backend
│   ├── main.py             # تطبيق FastAPI الرئيسي
│   ├── services/           # خدمات الصوت والفيديو
│   ├── database.py         # اتصال Supabase
│   ├── requirements.txt    # متطلبات Python
│   └── Dockerfile         # حاوية Docker للـ Backend
├── frontend/               # تطبيق Next.js
│   ├── pages/             # صفحات التطبيق
│   ├── components/        # مكونات React
│   ├── public/           # الملفات العامة
│   ├── utils/            # دوال مساعدة
│   ├── package.json      # متطلبات Node.js
│   └── Dockerfile       # حاوية Docker للـ Frontend
├── docker-compose.yml    # تشغيل المشروع كاملاً
├── check.py             # فحص المتطلبات
└── README.md           # هذا الملف
```

## 🚀 التشغيل السريع

### 1. تحضير البيئة

```bash
# استنساخ المشروع
git clone <repository-url>
cd VEO7-Video-Platform

# تفعيل البيئة الافتراضية
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# فحص المتطلبات
python check.py
```

### 2. إعداد Backend

```bash
cd backend
pip install -r requirements.txt

# إعداد متغيرات البيئة
cp .env.example .env
# قم بتعديل ملف .env بمعلومات Supabase

# تشغيل الخادم
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. إعداد Frontend

```bash
cd frontend
npm install

# إعداد متغيرات البيئة
cp .env.local.example .env.local
# قم بتعديل ملف .env.local

# تشغيل التطبيق
npm run dev
```

### 4. التشغيل باستخدام Docker

```bash
# تشغيل المشروع كاملاً
docker-compose up --build

# الوصول للتطبيق
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🔧 إعداد Supabase

1. إنشاء مشروع جديد على [Supabase](https://supabase.com)
2. الحصول على URL و API Key
3. إعداد Authentication (Email/Password + Google OAuth)
4. إنشاء Storage Bucket للفيديوهات
5. تحديث متغيرات البيئة

## 📱 الاستخدام

1. **التسجيل/تسجيل الدخول**: إنشاء حساب أو تسجيل الدخول
2. **رفع الصورة**: اختيار صورة الوجه المراد تحريكها
3. **كتابة النص**: إدخال النص المراد تحويله لصوت
4. **اختيار اللغة**: تحديد لغة الصوت
5. **إنتاج الفيديو**: معالجة وإنتاج الفيديو النهائي
6. **المشاهدة والتحميل**: عرض النتيجة وتحميلها

## 🌐 النشر

### Frontend (Vercel)
```bash
# ربط المشروع بـ Vercel
vercel

# نشر تلقائي عند كل push
git push origin main
```

### Backend (Render/Railway)
```bash
# إعداد متغيرات البيئة على المنصة
# رفع الكود ونشره
```

## 🔮 التطوير المستقبلي

- [ ] نظام اشتراكات مدفوعة
- [ ] مولد صور بـ Stable Diffusion
- [ ] ربط Google AdSense
- [ ] دعم فيديوهات أطول
- [ ] تأثيرات بصرية متقدمة
- [ ] API للمطورين

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف [LICENSE](LICENSE) للتفاصيل.

## 🤝 المساهمة

نرحب بالمساهمات! يرجى قراءة [CONTRIBUTING.md](CONTRIBUTING.md) للتفاصيل.

## 📞 الدعم

- 📧 البريد الإلكتروني: support@veo7.com
- 💬 Discord: [رابط الخادم]
- 📚 التوثيق: [رابط التوثيق]

---

صُنع بـ ❤️ لمجتمع المطورين العرب