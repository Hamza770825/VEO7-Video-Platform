# إعداد قاعدة البيانات - VEO7 Video Platform

## خطوات إعداد Supabase

### 1. إنشاء المشروع
- تم إنشاء المشروع بالفعل مع المفاتيح المقدمة
- Project URL: `https://itzvdtudtpvhhtfhgkhn.supabase.co`

### 2. إعداد قاعدة البيانات

#### الطريقة الأولى: استخدام SQL Editor في Supabase
1. اذهب إلى [Supabase Dashboard](https://supabase.com/dashboard)
2. اختر مشروعك
3. اذهب إلى **SQL Editor** من القائمة الجانبية
4. انسخ محتوى ملف `database_setup.sql` والصقه في المحرر
5. اضغط **Run** لتنفيذ الاستعلامات

#### الطريقة الثانية: استخدام psql (للمطورين المتقدمين)
```bash
# الاتصال بقاعدة البيانات
psql "postgresql://postgres:[YOUR-PASSWORD]@db.itzvdtudtpvhhtfhgkhn.supabase.co:5432/postgres"

# تنفيذ ملف الإعداد
\i database_setup.sql
```

### 3. التحقق من الإعداد

بعد تنفيذ ملف الإعداد، يجب أن تجد الجداول التالية في قاعدة البيانات:

#### الجداول الرئيسية:
- `public.profiles` - ملفات تعريف المستخدمين
- `public.videos` - بيانات الفيديوهات
- `public.user_stats` - إحصائيات المستخدمين

#### الفهارس:
- `idx_videos_user_id` - فهرس على user_id في جدول videos
- `idx_videos_status` - فهرس على status في جدول videos
- `idx_videos_created_at` - فهرس على created_at في جدول videos
- `idx_user_stats_user_id` - فهرس على user_id في جدول user_stats

#### الدوال والمحفزات:
- `update_updated_at_column()` - دالة تحديث updated_at تلقائياً
- `handle_new_user()` - دالة إنشاء ملف تعريف المستخدم تلقائياً
- `update_user_stats_on_video_create()` - دالة تحديث الإحصائيات
- `get_user_dashboard_stats()` - دالة الحصول على إحصائيات المستخدم
- `cleanup_old_failed_videos()` - دالة تنظيف الملفات القديمة

### 4. إعداد Authentication

#### تفعيل مقدمي الخدمة:
1. اذهب إلى **Authentication** > **Providers**
2. فعّل **Email** provider
3. اختياري: فعّل **Google**, **GitHub**, أو مقدمي خدمة آخرين

#### إعداد Email Templates:
1. اذهب إلى **Authentication** > **Email Templates**
2. خصص رسائل التأكيد وإعادة تعيين كلمة المرور

### 5. إعداد Storage (لرفع الملفات)

#### إنشاء Buckets:
1. اذهب إلى **Storage**
2. أنشئ bucket جديد باسم `videos`
3. أنشئ bucket جديد باسم `images`
4. أنشئ bucket جديد باسم `audio`

#### إعداد السياسات:
```sql
-- سياسة رفع الملفات للمستخدمين المسجلين
CREATE POLICY "Users can upload their own files" ON storage.objects
FOR INSERT WITH CHECK (auth.uid()::text = (storage.foldername(name))[1]);

-- سياسة عرض الملفات للمستخدمين المسجلين
CREATE POLICY "Users can view their own files" ON storage.objects
FOR SELECT USING (auth.uid()::text = (storage.foldername(name))[1]);

-- سياسة حذف الملفات للمستخدمين المسجلين
CREATE POLICY "Users can delete their own files" ON storage.objects
FOR DELETE USING (auth.uid()::text = (storage.foldername(name))[1]);
```

### 6. متغيرات البيئة

تأكد من أن ملفات البيئة تحتوي على المفاتيح الصحيحة:

#### Frontend (.env.local):
```
NEXT_PUBLIC_SUPABASE_URL=https://itzvdtudtpvhhtfhgkhn.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml0enZkdHVkdHB2aGh0Zmhna2huIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5NjgxNjYsImV4cCI6MjA3NDU0NDE2Nn0.aDWgY_WeXJvMeldWmU58i-4HGk5Vu_7g6pUjORgQTTU
```

#### Backend (.env):
```
SUPABASE_URL=https://itzvdtudtpvhhtfhgkhn.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml0enZkdHVkdHB2aGh0Zmhna2huIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5NjgxNjYsImV4cCI6MjA3NDU0NDE2Nn0.aDWgY_WeXJvMeldWmU58i-4HGk5Vu_7g6pUjORgQTTU
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml0enZkdHVkdHB2aGh0Zmhna2huIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODk2ODE2NiwiZXhwIjoyMDc0NTQ0MTY2fQ.j7BRNaSdFIK7tKjR0S4xuT1IYD_T2iX00yEx8uvSf2o
```

### 7. اختبار الاتصال

بعد إكمال الإعداد، يمكنك اختبار الاتصال من خلال:

1. تشغيل التطبيق: `npm run dev`
2. محاولة التسجيل كمستخدم جديد
3. التحقق من إنشاء البيانات في جداول قاعدة البيانات

### 8. استكشاف الأخطاء

#### مشاكل شائعة:
- **خطأ في الاتصال**: تأكد من صحة URL ومفاتيح API
- **خطأ في الصلاحيات**: تأكد من تفعيل RLS وإعداد السياسات
- **خطأ في إنشاء المستخدم**: تأكد من تنفيذ trigger `on_auth_user_created`

#### فحص السجلات:
1. اذهب إلى **Logs** في Supabase Dashboard
2. راجع سجلات **Database** و **Auth**
3. ابحث عن رسائل الخطأ وحلها

### 9. النسخ الاحتياطي

#### إنشاء نسخة احتياطية:
```bash
pg_dump "postgresql://postgres:[PASSWORD]@db.itzvdtudtpvhhtfhgkhn.supabase.co:5432/postgres" > backup.sql
```

#### استعادة النسخة الاحتياطية:
```bash
psql "postgresql://postgres:[PASSWORD]@db.itzvdtudtpvhhtfhgkhn.supabase.co:5432/postgres" < backup.sql
```

---

## ملاحظات مهمة

1. **الأمان**: لا تشارك مفاتيح `service_role` مع العامة
2. **الحدود**: راجع حدود الخطة المجانية في Supabase
3. **المراقبة**: راقب استخدام قاعدة البيانات والتخزين
4. **التحديثات**: احتفظ بنسخ احتياطية قبل التحديثات الكبيرة

للمساعدة الإضافية، راجع [وثائق Supabase](https://supabase.com/docs).