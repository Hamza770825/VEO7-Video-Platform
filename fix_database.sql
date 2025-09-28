-- ===================================================================
-- VEO7 Video Platform - Professional Database Setup
-- ===================================================================

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

-- إنشاء جدول التعليقات
CREATE TABLE IF NOT EXISTS public.comments (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    video_id UUID REFERENCES public.videos(id) ON DELETE CASCADE,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    parent_id UUID REFERENCES public.comments(id) ON DELETE CASCADE,
    like_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- إنشاء جدول الإعجابات
CREATE TABLE IF NOT EXISTS public.likes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    video_id UUID REFERENCES public.videos(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, video_id)
);

-- إنشاء جدول المتابعة
CREATE TABLE IF NOT EXISTS public.follows (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    follower_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    following_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(follower_id, following_id)
);

-- إنشاء جدول قوائم التشغيل
CREATE TABLE IF NOT EXISTS public.playlists (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    visibility VARCHAR(20) DEFAULT 'private',
    thumbnail_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- إنشاء جدول عناصر قوائم التشغيل
CREATE TABLE IF NOT EXISTS public.playlist_items (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    playlist_id UUID REFERENCES public.playlists(id) ON DELETE CASCADE,
    video_id UUID REFERENCES public.videos(id) ON DELETE CASCADE,
    position INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(playlist_id, video_id)
);

-- إنشاء فهارس للأداء
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_users_verification_token ON public.users(verification_token);
CREATE INDEX IF NOT EXISTS idx_users_reset_token ON public.users(reset_token);

CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON public.profiles(user_id);

CREATE INDEX IF NOT EXISTS idx_videos_user_id ON public.videos(user_id);
CREATE INDEX IF NOT EXISTS idx_videos_status ON public.videos(status);
CREATE INDEX IF NOT EXISTS idx_videos_visibility ON public.videos(visibility);
CREATE INDEX IF NOT EXISTS idx_videos_created_at ON public.videos(created_at);

CREATE INDEX IF NOT EXISTS idx_user_stats_user_id ON public.user_stats(user_id);

CREATE INDEX IF NOT EXISTS idx_comments_video_id ON public.comments(video_id);
CREATE INDEX IF NOT EXISTS idx_comments_user_id ON public.comments(user_id);
CREATE INDEX IF NOT EXISTS idx_comments_parent_id ON public.comments(parent_id);

CREATE INDEX IF NOT EXISTS idx_likes_user_id ON public.likes(user_id);
CREATE INDEX IF NOT EXISTS idx_likes_video_id ON public.likes(video_id);

CREATE INDEX IF NOT EXISTS idx_follows_follower_id ON public.follows(follower_id);
CREATE INDEX IF NOT EXISTS idx_follows_following_id ON public.follows(following_id);

CREATE INDEX IF NOT EXISTS idx_playlists_user_id ON public.playlists(user_id);
CREATE INDEX IF NOT EXISTS idx_playlist_items_playlist_id ON public.playlist_items(playlist_id);
CREATE INDEX IF NOT EXISTS idx_playlist_items_video_id ON public.playlist_items(video_id);

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

CREATE TRIGGER update_comments_updated_at BEFORE UPDATE ON public.comments
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_playlists_updated_at BEFORE UPDATE ON public.playlists
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
        'storage_used', COALESCE(SUM(v.file_size), 0),
        'followers_count', (
            SELECT COUNT(*) FROM public.follows 
            WHERE following_id = user_uuid
        ),
        'following_count', (
            SELECT COUNT(*) FROM public.follows 
            WHERE follower_id = user_uuid
        )
    )
    INTO result
    FROM public.videos v
    WHERE v.user_id = user_uuid;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- إنشاء دالة للبحث في الفيديوهات
CREATE OR REPLACE FUNCTION search_videos(search_term TEXT, limit_count INTEGER DEFAULT 20)
RETURNS TABLE (
    id UUID,
    title VARCHAR(255),
    description TEXT,
    thumbnail_url TEXT,
    duration INTEGER,
    view_count INTEGER,
    like_count INTEGER,
    user_id UUID,
    user_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        v.id,
        v.title,
        v.description,
        v.thumbnail_url,
        v.duration,
        v.view_count,
        v.like_count,
        v.user_id,
        p.full_name as user_name,
        v.created_at
    FROM public.videos v
    LEFT JOIN public.profiles p ON v.user_id = p.user_id
    WHERE 
        v.visibility = 'public' AND
        (v.title ILIKE '%' || search_term || '%' OR 
         v.description ILIKE '%' || search_term || '%' OR
         search_term = ANY(v.tags))
    ORDER BY v.created_at DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- إنشاء دالة لتحديث إحصائيات المستخدم
CREATE OR REPLACE FUNCTION update_user_stats()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO public.user_stats (user_id, total_videos, last_activity)
        VALUES (NEW.user_id, 1, NOW())
        ON CONFLICT (user_id) 
        DO UPDATE SET 
            total_videos = user_stats.total_videos + 1,
            last_activity = NOW();
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE public.user_stats 
        SET total_videos = GREATEST(total_videos - 1, 0),
            last_activity = NOW()
        WHERE user_id = OLD.user_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- إنشاء trigger لتحديث إحصائيات المستخدم عند إضافة/حذف فيديو
CREATE TRIGGER update_user_stats_on_video_change
    AFTER INSERT OR DELETE ON public.videos
    FOR EACH ROW EXECUTE FUNCTION update_user_stats();

-- تفعيل Row Level Security على جميع الجداول
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.videos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.comments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.likes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.follows ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.playlists ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.playlist_items ENABLE ROW LEVEL SECURITY;

-- سياسات الأمان للمستخدمين
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);

-- سياسات الأمان للملفات الشخصية
CREATE POLICY "Profiles are viewable by everyone" ON public.profiles
    FOR SELECT USING (true);

CREATE POLICY "Users can insert own profile" ON public.profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = user_id);

-- سياسات الأمان للفيديوهات
CREATE POLICY "Public videos are viewable by everyone" ON public.videos
    FOR SELECT USING (visibility = 'public' OR auth.uid() = user_id);

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

-- سياسات الأمان للتعليقات
CREATE POLICY "Comments are viewable by everyone" ON public.comments
    FOR SELECT USING (true);

CREATE POLICY "Authenticated users can insert comments" ON public.comments
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own comments" ON public.comments
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own comments" ON public.comments
    FOR DELETE USING (auth.uid() = user_id);

-- سياسات الأمان للإعجابات
CREATE POLICY "Likes are viewable by everyone" ON public.likes
    FOR SELECT USING (true);

CREATE POLICY "Authenticated users can manage likes" ON public.likes
    FOR ALL USING (auth.uid() = user_id);

-- سياسات الأمان للمتابعة
CREATE POLICY "Follows are viewable by everyone" ON public.follows
    FOR SELECT USING (true);

CREATE POLICY "Users can manage own follows" ON public.follows
    FOR ALL USING (auth.uid() = follower_id);

-- سياسات الأمان لقوائم التشغيل
CREATE POLICY "Public playlists are viewable by everyone" ON public.playlists
    FOR SELECT USING (visibility = 'public' OR auth.uid() = user_id);

CREATE POLICY "Users can manage own playlists" ON public.playlists
    FOR ALL USING (auth.uid() = user_id);

-- سياسات الأمان لعناصر قوائم التشغيل
CREATE POLICY "Playlist items follow playlist visibility" ON public.playlist_items
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM public.playlists p 
            WHERE p.id = playlist_id 
            AND (p.visibility = 'public' OR p.user_id = auth.uid())
        )
    );

CREATE POLICY "Users can manage own playlist items" ON public.playlist_items
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM public.playlists p 
            WHERE p.id = playlist_id 
            AND p.user_id = auth.uid()
        )
    );

-- إنشاء views مفيدة
CREATE OR REPLACE VIEW public.video_details AS
SELECT 
    v.*,
    p.full_name as user_name,
    p.avatar_url as user_avatar,
    (SELECT COUNT(*) FROM public.likes l WHERE l.video_id = v.id) as total_likes,
    (SELECT COUNT(*) FROM public.comments c WHERE c.video_id = v.id) as total_comments
FROM public.videos v
LEFT JOIN public.profiles p ON v.user_id = p.user_id;

-- إنشاء view للمستخدمين مع إحصائياتهم
CREATE OR REPLACE VIEW public.user_profiles AS
SELECT 
    u.id,
    u.email,
    u.is_verified,
    u.created_at,
    p.full_name,
    p.avatar_url,
    p.bio,
    p.website,
    p.location,
    COALESCE(s.total_videos, 0) as total_videos,
    COALESCE(s.total_views, 0) as total_views,
    COALESCE(s.total_likes, 0) as total_likes,
    (SELECT COUNT(*) FROM public.follows f WHERE f.following_id = u.id) as followers_count,
    (SELECT COUNT(*) FROM public.follows f WHERE f.follower_id = u.id) as following_count
FROM public.users u
LEFT JOIN public.profiles p ON u.id = p.user_id
LEFT JOIN public.user_stats s ON u.id = s.user_id;

-- إنشاء دالة لتسجيل مشاهدة فيديو
CREATE OR REPLACE FUNCTION increment_video_views(video_uuid UUID)
RETURNS VOID AS $$
BEGIN
    UPDATE public.videos 
    SET view_count = view_count + 1 
    WHERE id = video_uuid;
    
    -- تحديث إحصائيات المستخدم
    UPDATE public.user_stats 
    SET total_views = total_views + 1,
        last_activity = NOW()
    WHERE user_id = (SELECT user_id FROM public.videos WHERE id = video_uuid);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- إنشاء دالة للحصول على الفيديوهات الشائعة
CREATE OR REPLACE FUNCTION get_trending_videos(limit_count INTEGER DEFAULT 10)
RETURNS TABLE (
    id UUID,
    title VARCHAR(255),
    description TEXT,
    thumbnail_url TEXT,
    duration INTEGER,
    view_count INTEGER,
    like_count INTEGER,
    user_id UUID,
    user_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        v.id,
        v.title,
        v.description,
        v.thumbnail_url,
        v.duration,
        v.view_count,
        v.like_count,
        v.user_id,
        p.full_name as user_name,
        v.created_at
    FROM public.videos v
    LEFT JOIN public.profiles p ON v.user_id = p.user_id
    WHERE v.visibility = 'public'
    ORDER BY 
        (v.view_count * 0.7 + v.like_count * 0.3) DESC,
        v.created_at DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- إنشاء دالة للحصول على توصيات الفيديوهات
CREATE OR REPLACE FUNCTION get_recommended_videos(user_uuid UUID, limit_count INTEGER DEFAULT 10)
RETURNS TABLE (
    id UUID,
    title VARCHAR(255),
    description TEXT,
    thumbnail_url TEXT,
    duration INTEGER,
    view_count INTEGER,
    like_count INTEGER,
    user_id UUID,
    user_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        v.id,
        v.title,
        v.description,
        v.thumbnail_url,
        v.duration,
        v.view_count,
        v.like_count,
        v.user_id,
        p.full_name as user_name,
        v.created_at
    FROM public.videos v
    LEFT JOIN public.profiles p ON v.user_id = p.user_id
    WHERE 
        v.visibility = 'public' 
        AND v.user_id != user_uuid
        AND v.user_id IN (
            SELECT following_id 
            FROM public.follows 
            WHERE follower_id = user_uuid
        )
    ORDER BY v.created_at DESC
    LIMIT limit_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- إنشاء دالة للبحث المتقدم
CREATE OR REPLACE FUNCTION advanced_search(
    search_term TEXT DEFAULT '',
    user_filter UUID DEFAULT NULL,
    duration_min INTEGER DEFAULT NULL,
    duration_max INTEGER DEFAULT NULL,
    sort_by TEXT DEFAULT 'created_at',
    sort_order TEXT DEFAULT 'DESC',
    limit_count INTEGER DEFAULT 20,
    offset_count INTEGER DEFAULT 0
)
RETURNS TABLE (
    id UUID,
    title VARCHAR(255),
    description TEXT,
    thumbnail_url TEXT,
    duration INTEGER,
    view_count INTEGER,
    like_count INTEGER,
    user_id UUID,
    user_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
DECLARE
    query_text TEXT;
BEGIN
    query_text := '
        SELECT 
            v.id,
            v.title,
            v.description,
            v.thumbnail_url,
            v.duration,
            v.view_count,
            v.like_count,
            v.user_id,
            p.full_name as user_name,
            v.created_at
        FROM public.videos v
        LEFT JOIN public.profiles p ON v.user_id = p.user_id
        WHERE v.visibility = ''public''';
    
    IF search_term != '' THEN
        query_text := query_text || ' AND (v.title ILIKE ''%' || search_term || '%'' OR v.description ILIKE ''%' || search_term || '%'')';
    END IF;
    
    IF user_filter IS NOT NULL THEN
        query_text := query_text || ' AND v.user_id = ''' || user_filter || '''';
    END IF;
    
    IF duration_min IS NOT NULL THEN
        query_text := query_text || ' AND v.duration >= ' || duration_min;
    END IF;
    
    IF duration_max IS NOT NULL THEN
        query_text := query_text || ' AND v.duration <= ' || duration_max;
    END IF;
    
    query_text := query_text || ' ORDER BY v.' || sort_by || ' ' || sort_order;
    query_text := query_text || ' LIMIT ' || limit_count || ' OFFSET ' || offset_count;
    
    RETURN QUERY EXECUTE query_text;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- إدراج بيانات تجريبية للاختبار (اختياري)
-- يمكن حذف هذا القسم في الإنتاج
/*
INSERT INTO public.users (id, email, password_hash, is_verified) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'admin@veo7.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VJWZp/K/K', true),
('550e8400-e29b-41d4-a716-446655440001', 'user@veo7.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VJWZp/K/K', true)
ON CONFLICT (email) DO NOTHING;

INSERT INTO public.profiles (user_id, full_name, bio) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'مدير النظام', 'مرحباً بكم في منصة VEO7'),
('550e8400-e29b-41d4-a716-446655440001', 'مستخدم تجريبي', 'مستخدم تجريبي للاختبار')
ON CONFLICT (user_id) DO NOTHING;
*/

-- إنشاء دالة للتنظيف الدوري
CREATE OR REPLACE FUNCTION cleanup_expired_tokens()
RETURNS VOID AS $$
BEGIN
    -- حذف tokens منتهية الصلاحية
    UPDATE public.users 
    SET reset_token = NULL, reset_token_expires = NULL
    WHERE reset_token_expires < NOW();
    
    -- حذف verification tokens للمستخدمين المؤكدين
    UPDATE public.users 
    SET verification_token = NULL
    WHERE is_verified = true AND verification_token IS NOT NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- إنشاء extension للبحث النصي المتقدم (اختياري)
-- CREATE EXTENSION IF NOT EXISTS pg_trgm;
-- CREATE INDEX IF NOT EXISTS idx_videos_title_trgm ON public.videos USING gin (title gin_trgm_ops);
-- CREATE INDEX IF NOT EXISTS idx_videos_description_trgm ON public.videos USING gin (description gin_trgm_ops);

COMMENT ON TABLE public.users IS 'جدول المستخدمين الرئيسي';
COMMENT ON TABLE public.profiles IS 'ملفات المستخدمين الشخصية';
COMMENT ON TABLE public.videos IS 'جدول الفيديوهات';
COMMENT ON TABLE public.user_stats IS 'إحصائيات المستخدمين';
COMMENT ON TABLE public.comments IS 'تعليقات الفيديوهات';
COMMENT ON TABLE public.likes IS 'إعجابات الفيديوهات';
COMMENT ON TABLE public.follows IS 'متابعة المستخدمين';
COMMENT ON TABLE public.playlists IS 'قوائم التشغيل';
COMMENT ON TABLE public.playlist_items IS 'عناصر قوائم التشغيل';

-- إنهاء الإعداد
SELECT 'Database setup completed successfully!' as status;