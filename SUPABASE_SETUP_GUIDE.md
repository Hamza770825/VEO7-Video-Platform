# VEO7 Video Platform - Supabase Setup Guide

## نظرة عامة
هذا الدليل يشرح كيفية إعداد قاعدة بيانات Supabase للمشروع مع جميع الجداول والسياسات المطلوبة.

## الخطوات المطلوبة

### 1. إنشاء مشروع Supabase جديد
1. اذهب إلى [Supabase Dashboard](https://supabase.com/dashboard)
2. انقر على "New Project"
3. اختر Organization أو أنشئ واحدة جديدة
4. أدخل اسم المشروع: `VEO7-Video-Platform`
5. أدخل كلمة مرور قوية لقاعدة البيانات
6. اختر المنطقة الأقرب لك
7. انقر على "Create new project"

### 2. الحصول على مفاتيح API

بعد إنشاء المشروع، اذهب إلى **Settings > API**:

```
Project URL: https://your-project-id.supabase.co
anon public key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
service_role key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

⚠️ **مهم**: احفظ هذه المفاتيح في مكان آمن!

### 3. إعداد قاعدة البيانات

اذهب إلى **SQL Editor** في Supabase Dashboard وقم بتشغيل الكود التالي:

```sql
-- إنشاء جدول المستخدمين
CREATE TABLE IF NOT EXISTS public.users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    reset_token VARCHAR(255),
    reset_token_expires TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- إنشاء جدول الملفات الشخصية
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    full_name VARCHAR(255),
    avatar_url TEXT,
    bio TEXT,
    website VARCHAR(255),
    location VARCHAR(255),
    birth_date DATE,
    phone VARCHAR(20),
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- إنشاء جدول الفيديوهات
CREATE TABLE IF NOT EXISTS public.videos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    video_url TEXT,
    thumbnail_url TEXT,
    duration INTEGER,
    file_size BIGINT,
    status VARCHAR(50) DEFAULT 'processing',
    visibility VARCHAR(20) DEFAULT 'private',
    tags TEXT[],
    metadata JSONB DEFAULT '{}',
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- إنشاء جدول إحصائيات المستخدمين
CREATE TABLE IF NOT EXISTS public.user_stats (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE UNIQUE,
    total_videos INTEGER DEFAULT 0,
    total_views INTEGER DEFAULT 0,
    total_likes INTEGER DEFAULT 0,
    total_storage_used BIGINT DEFAULT 0,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- إنشاء فهارس للأداء
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON public.profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_videos_user_id ON public.videos(user_id);
CREATE INDEX IF NOT EXISTS idx_videos_status ON public.videos(status);
CREATE INDEX IF NOT EXISTS idx_user_stats_user_id ON public.user_stats(user_id);

-- إنشاء triggers لتحديث updated_at تلقائياً
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_videos_updated_at BEFORE UPDATE ON public.videos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_stats_updated_at BEFORE UPDATE ON public.user_stats
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- إنشاء دالة لإحصائيات المستخدم
CREATE OR REPLACE FUNCTION get_user_dashboard_stats(user_uuid UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'total_videos', COALESCE(COUNT(v.id), 0),
        'total_views', COALESCE(SUM(v.view_count), 0),
        'total_likes', COALESCE(SUM(v.like_count), 0),
        'storage_used', COALESCE(SUM(v.file_size), 0)
    )
    INTO result
    FROM public.videos v
    WHERE v.user_id = user_uuid;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 4. إعداد Row Level Security (RLS)

```sql
-- تفعيل RLS على جميع الجداول
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.videos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_stats ENABLE ROW LEVEL SECURITY;

-- سياسات الأمان للمستخدمين
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);

-- سياسات الأمان للملفات الشخصية
CREATE POLICY "Users can view own profile" ON public.profiles
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile" ON public.profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = user_id);

-- سياسات الأمان للفيديوهات
CREATE POLICY "Users can view own videos" ON public.videos
    FOR SELECT USING (auth.uid() = user_id OR visibility = 'public');

CREATE POLICY "Users can insert own videos" ON public.videos
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own videos" ON public.videos
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own videos" ON public.videos
    FOR DELETE USING (auth.uid() = user_id);

-- سياسات الأمان للإحصائيات
CREATE POLICY "Users can view own stats" ON public.user_stats
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own stats" ON public.user_stats
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own stats" ON public.user_stats
    FOR UPDATE USING (auth.uid() = user_id);
```

### 5. إعداد المصادقة

اذهب إلى **Authentication > Settings**:

#### Email Templates
1. **Confirm signup**: قم بتخصيص رسالة التحقق
2. **Reset password**: قم بتخصيص رسالة إعادة تعيين كلمة المرور
3. **Magic Link**: قم بتخصيص رسالة الرابط السحري

#### Site URL
```
Site URL: http://localhost:3000
Additional redirect URLs: 
- http://localhost:3000/auth/callback
- https://yourdomain.com/auth/callback
```

#### Email Auth
- ✅ Enable email confirmations
- ✅ Enable email change confirmations
- ✅ Secure email change

### 6. إعداد Storage (اختياري للفيديوهات)

اذهب إلى **Storage** وأنشئ bucket جديد:

```
Bucket name: videos
Public: false (للأمان)
```

ثم أضف سياسات الأمان:

```sql
-- سياسة للرفع
CREATE POLICY "Users can upload own videos" ON storage.objects
    FOR INSERT WITH CHECK (bucket_id = 'videos' AND auth.uid()::text = (storage.foldername(name))[1]);

-- سياسة للعرض
CREATE POLICY "Users can view own videos" ON storage.objects
    FOR SELECT USING (bucket_id = 'videos' AND auth.uid()::text = (storage.foldername(name))[1]);

-- سياسة للحذف
CREATE POLICY "Users can delete own videos" ON storage.objects
    FOR DELETE USING (bucket_id = 'videos' AND auth.uid()::text = (storage.foldername(name))[1]);
```

### 7. تحديث متغيرات البيئة

قم بتحديث ملف `.env` في مجلد `backend`:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-role-key-here

# Database Configuration
DATABASE_URL=postgresql://postgres:your-db-password@db.your-project-id.supabase.co:5432/postgres

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# JWT Configuration
SECRET_KEY=your-super-secret-jwt-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration (اختياري)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

وملف `.env.local` في مجلد `frontend`:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
```

### 8. اختبار الإعداد

بعد تحديث متغيرات البيئة، قم بإعادة تشغيل الخوادم:

```bash
# في مجلد backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# في مجلد frontend
npm run dev
```

ثم قم بتشغيل اختبار المصادقة:

```bash
python test_authentication.py
```

### 9. التحقق من الإعداد

يجب أن ترى:
- ✅ اتصال ناجح بقاعدة البيانات
- ✅ تسجيل مستخدمين جدد
- ✅ إرسال رسائل التحقق
- ✅ تسجيل الدخول والخروج
- ✅ تحديث الملفات الشخصية

### 🔧 استكشاف الأخطاء

#### خطأ في الاتصال
- تحقق من صحة SUPABASE_URL و SUPABASE_ANON_KEY
- تأكد من أن المشروع نشط في Supabase

#### خطأ في المصادقة
- تحقق من إعدادات Site URL
- تأكد من تفعيل Email confirmations

#### خطأ في قاعدة البيانات
- تحقق من تشغيل جميع SQL scripts
- تأكد من إعداد RLS policies بشكل صحيح

### 📞 الدعم

إذا واجهت أي مشاكل:
1. راجع [Supabase Documentation](https://supabase.com/docs)
2. تحقق من سجلات الأخطاء في Dashboard
3. تأكد من صحة جميع متغيرات البيئة

---

🎉 **بعد إكمال هذه الخطوات، ستحصل على نظام احترافي كامل!**