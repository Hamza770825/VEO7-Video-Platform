# 🚀 دليل إعداد Supabase لمشروع VEO7

## 📋 الخطوات المطلوبة:

### 1. إنشاء حساب Supabase
1. انتقل إلى [supabase.com](https://supabase.com)
2. اضغط على "Start your project"
3. سجل دخولك باستخدام GitHub أو Google

### 2. إنشاء مشروع جديد
1. اضغط على "New Project"
2. اختر Organization أو أنشئ واحدة جديدة
3. أدخل تفاصيل المشروع:
   - **Name**: VEO7-Video-Platform
   - **Database Password**: كلمة مرور قوية (احفظها!)
   - **Region**: اختر أقرب منطقة لك
4. اضغط "Create new project"

### 3. الحصول على مفاتيح API
1. انتظر حتى ينتهي إعداد المشروع (2-3 دقائق)
2. انتقل إلى **Settings** → **API**
3. انسخ المفاتيح التالية:

#### للـ Backend (.env):
```env
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_ANON_KEY=your_anon_public_key_here
SUPABASE_SERVICE_KEY=your_service_role_key_here
```

#### للـ Frontend (.env.local):
```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project-ref.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_public_key_here
```

### 4. إعداد قاعدة البيانات
1. انتقل إلى **SQL Editor**
2. قم بتشغيل الاستعلامات التالية:

```sql
-- إنشاء جدول المستخدمين
CREATE TABLE IF NOT EXISTS public.users (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- إنشاء جدول الفيديوهات
CREATE TABLE IF NOT EXISTS public.videos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    video_url TEXT NOT NULL,
    thumbnail_url TEXT,
    language TEXT DEFAULT 'ar',
    duration INTEGER,
    file_size BIGINT,
    status TEXT DEFAULT 'completed',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- إعداد Row Level Security
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.videos ENABLE ROW LEVEL SECURITY;

-- سياسات الأمان للمستخدمين
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);

-- سياسات الأمان للفيديوهات
CREATE POLICY "Users can view own videos" ON public.videos
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own videos" ON public.videos
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own videos" ON public.videos
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own videos" ON public.videos
    FOR DELETE USING (auth.uid() = user_id);
```

### 5. إعداد Storage
1. انتقل إلى **Storage**
2. أنشئ bucket جديد باسم `videos`
3. اجعله public للقراءة
4. أنشئ bucket آخر باسم `images` للصور

### 6. إعداد Authentication
1. انتقل إلى **Authentication** → **Settings**
2. فعّل **Email** provider
3. لتفعيل Google OAuth:
   - انتقل إلى **Providers**
   - فعّل **Google**
   - أدخل Google Client ID و Secret

### 7. تحديث ملفات البيئة
1. في `backend/.env` - استبدل القيم التجريبية بالمفاتيح الحقيقية
2. في `frontend/.env.local` - استبدل القيم التجريبية بالمفاتيح الحقيقية

### 8. اختبار الاتصال
```bash
# في مجلد Backend
cd backend
python -c "from database import supabase_client; print('✅ Supabase connected successfully!' if supabase_client else '❌ Connection failed')"

# في مجلد Frontend
cd frontend
npm run dev
```

## 🔒 ملاحظات أمنية مهمة:
- **لا تشارك** مفتاح `service_role` أبداً
- استخدم `anon` key فقط في Frontend
- احتفظ بنسخة احتياطية من كلمة مرور قاعدة البيانات
- فعّل 2FA على حساب Supabase

## 📞 الدعم:
إذا واجهت أي مشاكل، راجع [وثائق Supabase](https://supabase.com/docs) أو اتصل بالدعم.