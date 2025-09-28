-- VEO7 Video Platform Database Setup
-- تشغيل هذا الملف في Supabase SQL Editor

-- إنشاء جدول المستخدمين (يتم إنشاؤه تلقائياً بواسطة Supabase Auth)
-- لكن نحتاج إلى إضافة بعض الحقول الإضافية

-- إنشاء جدول ملفات تعريف المستخدمين
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    subscription_plan TEXT DEFAULT 'free' CHECK (subscription_plan IN ('free', 'pro', 'premium')),
    credits_remaining INTEGER DEFAULT 10,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- إنشاء جدول الفيديوهات
CREATE TABLE IF NOT EXISTS public.videos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'processing_audio', 'processing_video', 'completed', 'failed')),
    image_url TEXT,
    audio_url TEXT,
    video_url TEXT,
    duration INTEGER, -- in seconds
    file_size BIGINT, -- in bytes
    settings JSONB DEFAULT '{}',
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- إنشاء جدول إحصائيات المستخدمين
CREATE TABLE IF NOT EXISTS public.user_stats (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE NOT NULL,
    total_videos INTEGER DEFAULT 0,
    total_duration INTEGER DEFAULT 0, -- in seconds
    credits_used INTEGER DEFAULT 0,
    last_video_created TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- إنشاء فهارس لتحسين الأداء
CREATE INDEX IF NOT EXISTS idx_videos_user_id ON public.videos(user_id);
CREATE INDEX IF NOT EXISTS idx_videos_status ON public.videos(status);
CREATE INDEX IF NOT EXISTS idx_videos_created_at ON public.videos(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_user_stats_user_id ON public.user_stats(user_id);

-- إنشاء دالة لتحديث updated_at تلقائياً
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- إنشاء triggers لتحديث updated_at
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_videos_updated_at BEFORE UPDATE ON public.videos
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_stats_updated_at BEFORE UPDATE ON public.user_stats
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- إنشاء دالة لإنشاء ملف تعريف المستخدم تلقائياً عند التسجيل
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name)
    VALUES (NEW.id, NEW.email, NEW.raw_user_meta_data->>'full_name');
    
    INSERT INTO public.user_stats (user_id)
    VALUES (NEW.id);
    
    RETURN NEW;
END;
$$ language 'plpgsql' SECURITY DEFINER;

-- إنشاء trigger لإنشاء ملف تعريف المستخدم تلقائياً
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- إنشاء دالة لتحديث إحصائيات المستخدم عند إنشاء فيديو
CREATE OR REPLACE FUNCTION public.update_user_stats_on_video_create()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'completed' AND (OLD.status IS NULL OR OLD.status != 'completed') THEN
        UPDATE public.user_stats 
        SET 
            total_videos = total_videos + 1,
            total_duration = total_duration + COALESCE(NEW.duration, 0),
            credits_used = credits_used + 1,
            last_video_created = NOW()
        WHERE user_id = NEW.user_id;
        
        -- خصم رصيد من المستخدم
        UPDATE public.profiles 
        SET credits_remaining = GREATEST(credits_remaining - 1, 0)
        WHERE id = NEW.user_id;
    END IF;
    
    RETURN NEW;
END;
$$ language 'plpgsql' SECURITY DEFINER;

-- إنشاء trigger لتحديث الإحصائيات
CREATE TRIGGER on_video_completed
    AFTER INSERT OR UPDATE ON public.videos
    FOR EACH ROW EXECUTE FUNCTION public.update_user_stats_on_video_create();

-- تفعيل Row Level Security (RLS)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.videos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_stats ENABLE ROW LEVEL SECURITY;

-- إنشاء سياسات الأمان
-- سياسة ملفات تعريف المستخدمين
CREATE POLICY "Users can view own profile" ON public.profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id);

-- سياسة الفيديوهات
CREATE POLICY "Users can view own videos" ON public.videos
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own videos" ON public.videos
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own videos" ON public.videos
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own videos" ON public.videos
    FOR DELETE USING (auth.uid() = user_id);

-- سياسة إحصائيات المستخدمين
CREATE POLICY "Users can view own stats" ON public.user_stats
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update own stats" ON public.user_stats
    FOR UPDATE USING (auth.uid() = user_id);

-- إنشاء بعض البيانات التجريبية (اختيارية)
-- INSERT INTO public.profiles (id, email, full_name, subscription_plan, credits_remaining)
-- VALUES 
--     ('00000000-0000-0000-0000-000000000001', 'demo@veo7.com', 'Demo User', 'pro', 100);

-- إنشاء دالة للحصول على إحصائيات المستخدم
CREATE OR REPLACE FUNCTION public.get_user_dashboard_stats(user_uuid UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'total_videos', COALESCE(us.total_videos, 0),
        'total_duration', COALESCE(us.total_duration, 0),
        'credits_used', COALESCE(us.credits_used, 0),
        'credits_remaining', COALESCE(p.credits_remaining, 0),
        'subscription_plan', COALESCE(p.subscription_plan, 'free'),
        'last_video_created', us.last_video_created
    ) INTO result
    FROM public.user_stats us
    RIGHT JOIN public.profiles p ON p.id = user_uuid
    LEFT JOIN public.user_stats us2 ON us2.user_id = user_uuid
    WHERE p.id = user_uuid;
    
    RETURN result;
END;
$$ language 'plpgsql' SECURITY DEFINER;

-- منح الصلاحيات المطلوبة
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated;

-- إنشاء دالة لتنظيف الملفات القديمة (يمكن تشغيلها دورياً)
CREATE OR REPLACE FUNCTION public.cleanup_old_failed_videos()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM public.videos 
    WHERE status = 'failed' 
    AND created_at < NOW() - INTERVAL '7 days';
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ language 'plpgsql' SECURITY DEFINER;

-- رسالة تأكيد
SELECT 'VEO7 Database setup completed successfully!' as message;