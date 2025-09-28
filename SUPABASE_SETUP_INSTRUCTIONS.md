# تعليمات إعداد قاعدة البيانات في Supabase

## الخطوات المطلوبة لإصلاح قاعدة البيانات

### 1. الدخول إلى لوحة تحكم Supabase
- اذهب إلى: https://supabase.com/dashboard
- سجل الدخول إلى حسابك
- اختر مشروعك: `itzvdtudtpvhhtfhgkhn`

### 2. تطبيق إصلاح قاعدة البيانات
1. في لوحة التحكم، اذهب إلى **SQL Editor**
2. انسخ محتوى ملف `database_fix_complete.sql` بالكامل
3. الصق المحتوى في محرر SQL
4. اضغط على **Run** لتنفيذ الاستعلام

### 3. إعداد Storage Buckets
اذهب إلى **Storage** في لوحة التحكم وأنشئ المجلدات التالية:

#### إنشاء Bucket: `user-uploads`
```sql
-- في SQL Editor
INSERT INTO storage.buckets (id, name, public) VALUES ('user-uploads', 'user-uploads', true);
```

#### إنشاء Bucket: `generated-videos`
```sql
INSERT INTO storage.buckets (id, name, public) VALUES ('generated-videos', 'generated-videos', true);
```

#### إنشاء Bucket: `user-avatars`
```sql
INSERT INTO storage.buckets (id, name, public) VALUES ('user-avatars', 'user-avatars', true);
```

### 4. إعداد Storage Policies
```sql
-- سياسات user-uploads
CREATE POLICY "Users can upload their own files" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'user-uploads' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Users can view their own files" ON storage.objects
FOR SELECT USING (bucket_id = 'user-uploads' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Users can update their own files" ON storage.objects
FOR UPDATE USING (bucket_id = 'user-uploads' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Users can delete their own files" ON storage.objects
FOR DELETE USING (bucket_id = 'user-uploads' AND auth.uid()::text = (storage.foldername(name))[1]);

-- سياسات generated-videos
CREATE POLICY "Users can view their generated videos" ON storage.objects
FOR SELECT USING (bucket_id = 'generated-videos' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Service role can manage generated videos" ON storage.objects
FOR ALL USING (bucket_id = 'generated-videos' AND auth.role() = 'service_role');

-- سياسات user-avatars
CREATE POLICY "Users can upload their avatars" ON storage.objects
FOR INSERT WITH CHECK (bucket_id = 'user-avatars' AND auth.uid()::text = (storage.foldername(name))[1]);

CREATE POLICY "Anyone can view avatars" ON storage.objects
FOR SELECT USING (bucket_id = 'user-avatars');

CREATE POLICY "Users can update their avatars" ON storage.objects
FOR UPDATE USING (bucket_id = 'user-avatars' AND auth.uid()::text = (storage.foldername(name))[1]);
```

### 5. إعداد Authentication
1. اذهب إلى **Authentication** > **Settings**
2. تأكد من تفعيل **Email confirmations**
3. في **Email Templates**، تأكد من إعداد قوالب البريد الإلكتروني

### 6. إعداد Row Level Security (RLS)
تم تطبيق RLS تلقائياً في ملف `database_fix_complete.sql`

### 7. التحقق من الإعداد
بعد تطبيق جميع الخطوات، تحقق من:
- وجود جميع الجداول في **Table Editor**
- وجود Storage Buckets في **Storage**
- عمل Authentication في **Authentication**

### 8. اختبار الاتصال
بعد تطبيق الإصلاحات، أعد تشغيل الخادم الخلفي:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

ثم اختبر المسارات:
- `GET /api/health` - يجب أن يعيد 200 OK
- `GET /api/plans` - يجب أن يعيد قائمة الخطط

## ملاحظات مهمة
- تأكد من أن مفاتيح Supabase في ملف `.env` صحيحة
- تأكد من أن URL قاعدة البيانات صحيح
- في حالة وجود أخطاء، تحقق من logs في Supabase Dashboard

## الدعم
في حالة وجود مشاكل، تحقق من:
1. **Logs** في Supabase Dashboard
2. **API Logs** في لوحة التحكم
3. **Database** > **Logs** للاستعلامات