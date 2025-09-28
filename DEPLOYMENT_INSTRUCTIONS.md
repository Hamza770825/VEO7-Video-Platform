# 🚀 دليل نشر VEO7 Video Platform

## خطوات نشر الموقع على Vercel

### 1. إعداد الحساب
1. اذهب إلى: https://vercel.com
2. سجل الدخول باستخدام GitHub أو Google
3. اربط حسابك بـ GitHub

### 2. نشر Frontend على Vercel

#### الطريقة الأولى: من خلال الموقع
1. اضغط "New Project" في Vercel Dashboard
2. اختر "Import Git Repository"
3. اختر مجلد `frontend` من مشروعك
4. اضبط الإعدادات:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

#### الطريقة الثانية: من خلال CLI
```bash
cd frontend
vercel login
vercel --prod
```

### 3. إعداد متغيرات البيئة في Vercel

في Vercel Dashboard > Project Settings > Environment Variables:

```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_key
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
NEXT_PUBLIC_APP_URL=https://your-project.vercel.app
```

### 4. نشر Backend على Railway

1. اذهب إلى: https://railway.app
2. سجل الدخول وأنشئ مشروع جديد
3. اربط مجلد `backend`
4. اضبط متغيرات البيئة

### 5. تحديث PayPal Webhook

بعد الحصول على الدومين، حدث PayPal Webhook URL إلى:
```
https://your-project.vercel.app/api/paypal/webhook
```

## الدومين النهائي

ستحصل على دومين مثل:
- **Frontend**: `https://veo7-video-platform.vercel.app`
- **Backend**: `https://veo7-backend.railway.app`

## ملاحظات مهمة

1. **SSL**: Vercel يوفر SSL مجاني تلقائياً
2. **Custom Domain**: يمكنك ربط دومين مخصص لاحقاً
3. **Environment Variables**: تأكد من إعداد جميع المتغيرات المطلوبة
4. **CORS**: تأكد من إعداد CORS في Backend للدومين الجديد

## استكشاف الأخطاء

### مشكلة Build
```bash
# تحقق من الأخطاء محلياً
npm run build
```

### مشكلة Environment Variables
- تأكد من إعداد جميع المتغيرات في Vercel Dashboard
- أعد النشر بعد تحديث المتغيرات

### مشكلة API Connection
- تحقق من NEXT_PUBLIC_API_URL
- تأكد من تشغيل Backend على Railway