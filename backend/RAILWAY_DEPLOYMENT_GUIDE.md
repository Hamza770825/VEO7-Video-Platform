# دليل نشر Backend على Railway

## 📋 المتطلبات المسبقة
- حساب على [Railway](https://railway.app)
- حساب GitHub
- مشروع Backend جاهز

## 🚀 خطوات النشر

### 1. إنشاء حساب Railway
1. اذهب إلى [railway.app](https://railway.app)
2. سجل الدخول باستخدام GitHub
3. اربط حسابك بـ GitHub

### 2. نشر المشروع
1. اضغط على "New Project"
2. اختر "Deploy from GitHub repo"
3. اختر مستودع `VEO7-Video-Platform`
4. اختر مجلد `backend` كـ Root Directory

### 3. إعداد متغيرات البيئة
أضف المتغيرات التالية في Railway Dashboard:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Database
DATABASE_URL=your_database_url

# PayPal Configuration
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
PAYPAL_MODE=sandbox  # أو live للإنتاج

# App Configuration
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=https://your-frontend-domain.vercel.app

# File Upload
MAX_FILE_SIZE=50000000
UPLOAD_DIR=/tmp/uploads
```

### 4. إعداد Domain
1. في Railway Dashboard، اذهب إلى Settings
2. اختر "Domains"
3. أضف domain مخصص أو استخدم الـ subdomain المجاني

### 5. التحقق من النشر
- تحقق من أن الخدمة تعمل: `https://your-backend-url.railway.app/health`
- تحقق من API docs: `https://your-backend-url.railway.app/docs`

## 🔧 ملفات النشر المُنشأة

### `railway.json`
ملف إعداد Railway الأساسي

### `Procfile`
يحدد كيفية تشغيل التطبيق

### `nixpacks.toml`
إعدادات البناء والتشغيل

## 🌐 ربط Frontend بـ Backend

بعد نشر Backend، احصل على الـ URL وأضفه في Frontend:

```env
# في frontend/.env.local
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
```

## 📊 مراقبة الأداء
- استخدم Railway Dashboard لمراقبة الـ logs
- تحقق من استخدام الموارد
- راقب الأخطاء والتحذيرات

## 🔒 الأمان
- تأكد من إعداد CORS بشكل صحيح
- استخدم HTTPS فقط
- احم متغيرات البيئة الحساسة

## 🆘 استكشاف الأخطاء

### مشكلة في البناء
```bash
# تحقق من logs البناء في Railway Dashboard
```

### مشكلة في التشغيل
```bash
# تحقق من logs التشغيل
# تأكد من متغيرات البيئة
```

### مشكلة في الاتصال
```bash
# تحقق من CORS settings
# تأكد من أن PORT متغير صحيح
```

## 📞 الدعم
- [Railway Documentation](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [GitHub Issues](https://github.com/your-repo/issues)

---
تم إنشاء هذا الدليل بواسطة VEO7 AI Assistant 🤖