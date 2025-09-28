-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create custom types
CREATE TYPE video_status AS ENUM ('processing', 'completed', 'failed');
CREATE TYPE video_quality AS ENUM ('low', 'medium', 'high');
CREATE TYPE voice_type AS ENUM ('male', 'female');

-- User profiles table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    avatar_url TEXT,
    subscription_tier TEXT DEFAULT 'free' CHECK (subscription_tier IN ('free', 'pro', 'premium')),
    storage_used BIGINT DEFAULT 0,
    videos_created INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Videos table
CREATE TABLE IF NOT EXISTS videos (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    text_content TEXT NOT NULL,
    
    -- File URLs
    image_url TEXT,
    audio_url TEXT,
    video_url TEXT,
    thumbnail_url TEXT,
    
    -- Video metadata
    duration INTEGER DEFAULT 0, -- in seconds
    file_size BIGINT DEFAULT 0, -- in bytes
    views INTEGER DEFAULT 0,
    status video_status DEFAULT 'processing',
    
    -- Processing settings
    settings JSONB DEFAULT '{
        "quality": "medium",
        "speed": 1.0,
        "voice": "female",
        "language": "en"
    }'::jsonb,
    
    -- Processing metadata
    processing_started_at TIMESTAMP WITH TIME ZONE,
    processing_completed_at TIMESTAMP WITH TIME ZONE,
    processing_error TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Video processing logs table
CREATE TABLE IF NOT EXISTS video_processing_logs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE NOT NULL,
    step TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('started', 'completed', 'failed')),
    message TEXT,
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    error_details JSONB
);

-- User sessions table (for analytics)
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES user_profiles(id) ON DELETE CASCADE,
    session_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    session_end TIMESTAMP WITH TIME ZONE,
    ip_address INET,
    user_agent TEXT,
    device_info JSONB
);

-- Video views table (for analytics)
CREATE TABLE IF NOT EXISTS video_views (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    video_id UUID REFERENCES videos(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES user_profiles(id) ON DELETE SET NULL,
    ip_address INET,
    user_agent TEXT,
    watch_duration INTEGER DEFAULT 0, -- in seconds
    viewed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- System settings table
CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_videos_user_id ON videos(user_id);
CREATE INDEX IF NOT EXISTS idx_videos_status ON videos(status);
CREATE INDEX IF NOT EXISTS idx_videos_created_at ON videos(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_video_processing_logs_video_id ON video_processing_logs(video_id);
CREATE INDEX IF NOT EXISTS idx_video_views_video_id ON video_views(video_id);
CREATE INDEX IF NOT EXISTS idx_video_views_user_id ON video_views(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_user_profiles_updated_at 
    BEFORE UPDATE ON user_profiles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_videos_updated_at 
    BEFORE UPDATE ON videos 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to increment video views
CREATE OR REPLACE FUNCTION increment_video_views(video_id UUID)
RETURNS VOID AS $$
BEGIN
    UPDATE videos 
    SET views = views + 1 
    WHERE id = video_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to update user storage usage
CREATE OR REPLACE FUNCTION update_user_storage_usage(user_id UUID)
RETURNS VOID AS $$
BEGIN
    UPDATE user_profiles 
    SET storage_used = (
        SELECT COALESCE(SUM(file_size), 0) 
        FROM videos 
        WHERE videos.user_id = user_profiles.id
    )
    WHERE id = user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get user statistics
CREATE OR REPLACE FUNCTION get_user_stats(user_id UUID)
RETURNS TABLE (
    total_videos INTEGER,
    total_views INTEGER,
    total_duration INTEGER,
    storage_used BIGINT,
    videos_this_month INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::INTEGER as total_videos,
        COALESCE(SUM(v.views), 0)::INTEGER as total_views,
        COALESCE(SUM(v.duration), 0)::INTEGER as total_duration,
        COALESCE(up.storage_used, 0) as storage_used,
        COUNT(CASE WHEN v.created_at >= DATE_TRUNC('month', NOW()) THEN 1 END)::INTEGER as videos_this_month
    FROM user_profiles up
    LEFT JOIN videos v ON v.user_id = up.id
    WHERE up.id = get_user_stats.user_id
    GROUP BY up.storage_used;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Row Level Security (RLS) policies

-- Enable RLS on all tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE videos ENABLE ROW LEVEL SECURITY;
ALTER TABLE video_processing_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE video_views ENABLE ROW LEVEL SECURITY;

-- User profiles policies
CREATE POLICY "Users can view own profile" ON user_profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON user_profiles
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON user_profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

-- Videos policies
CREATE POLICY "Users can view own videos" ON videos
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own videos" ON videos
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own videos" ON videos
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own videos" ON videos
    FOR DELETE USING (auth.uid() = user_id);

-- Video processing logs policies
CREATE POLICY "Users can view own video logs" ON video_processing_logs
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM videos 
            WHERE videos.id = video_processing_logs.video_id 
            AND videos.user_id = auth.uid()
        )
    );

-- Video views policies (more permissive for analytics)
CREATE POLICY "Anyone can insert video views" ON video_views
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can view own video views" ON video_views
    FOR SELECT USING (
        auth.uid() = user_id OR 
        EXISTS (
            SELECT 1 FROM videos 
            WHERE videos.id = video_views.video_id 
            AND videos.user_id = auth.uid()
        )
    );

-- User sessions policies
CREATE POLICY "Users can view own sessions" ON user_sessions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own sessions" ON user_sessions
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Insert default system settings
INSERT INTO system_settings (key, value, description) VALUES
    ('max_video_duration', '300', 'Maximum video duration in seconds'),
    ('max_file_size', '104857600', 'Maximum file size in bytes (100MB)'),
    ('supported_languages', '["en", "ar", "es", "fr", "de", "it", "pt", "ru", "ja", "ko", "zh"]', 'Supported languages for TTS'),
    ('default_video_quality', '"medium"', 'Default video quality setting'),
    ('processing_timeout', '1800', 'Video processing timeout in seconds (30 minutes)')
ON CONFLICT (key) DO NOTHING;

-- Create a function to handle new user registration
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_profiles (id, email, full_name)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger to automatically create user profile on signup
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Create storage buckets (run these in Supabase dashboard or via API)
-- INSERT INTO storage.buckets (id, name, public) VALUES 
--     ('images', 'images', true),
--     ('audio', 'audio', true),
--     ('videos', 'videos', true),
--     ('thumbnails', 'thumbnails', true);

-- Storage policies (uncomment and run in Supabase dashboard)
-- CREATE POLICY "Users can upload own images" ON storage.objects
--     FOR INSERT WITH CHECK (bucket_id = 'images' AND auth.uid()::text = (storage.foldername(name))[1]);

-- CREATE POLICY "Users can view own images" ON storage.objects
--     FOR SELECT USING (bucket_id = 'images' AND auth.uid()::text = (storage.foldername(name))[1]);

-- CREATE POLICY "Users can delete own images" ON storage.objects
--     FOR DELETE USING (bucket_id = 'images' AND auth.uid()::text = (storage.foldername(name))[1]);

-- Similar policies for audio, videos, and thumbnails buckets...