-- Seed data for development and testing
-- This file contains sample data to help with development and testing

-- Insert sample system settings (if not already exists)
INSERT INTO system_settings (key, value, description) VALUES
    ('maintenance_mode', 'false', 'Enable/disable maintenance mode'),
    ('registration_enabled', 'true', 'Enable/disable new user registration'),
    ('max_videos_per_user', '50', 'Maximum videos per user (free tier)'),
    ('max_videos_per_user_pro', '500', 'Maximum videos per user (pro tier)'),
    ('max_videos_per_user_premium', '-1', 'Maximum videos per user (premium tier, -1 = unlimited)'),
    ('video_processing_queue_limit', '10', 'Maximum videos in processing queue'),
    ('supported_image_formats', '["jpg", "jpeg", "png", "webp"]', 'Supported image formats'),
    ('supported_audio_formats', '["mp3", "wav", "ogg", "m4a"]', 'Supported audio formats'),
    ('tts_rate_limit', '100', 'TTS requests per hour per user'),
    ('storage_limit_free', '1073741824', 'Storage limit for free users (1GB)'),
    ('storage_limit_pro', '10737418240', 'Storage limit for pro users (10GB)'),
    ('storage_limit_premium', '107374182400', 'Storage limit for premium users (100GB)')
ON CONFLICT (key) DO UPDATE SET
    value = EXCLUDED.value,
    description = EXCLUDED.description,
    updated_at = NOW();

-- Sample video processing steps for reference
-- These would be used by the backend to track processing progress
INSERT INTO system_settings (key, value, description) VALUES
    ('video_processing_steps', '[
        {"step": "validation", "name": "Validating input files", "weight": 5},
        {"step": "image_processing", "name": "Processing face image", "weight": 15},
        {"step": "audio_generation", "name": "Generating speech audio", "weight": 25},
        {"step": "face_detection", "name": "Detecting face landmarks", "weight": 15},
        {"step": "video_synthesis", "name": "Synthesizing talking video", "weight": 30},
        {"step": "post_processing", "name": "Final video processing", "weight": 10}
    ]', 'Video processing steps with weights for progress calculation')
ON CONFLICT (key) DO NOTHING;

-- Sample language configurations
INSERT INTO system_settings (key, value, description) VALUES
    ('language_configs', '{
        "en": {"name": "English", "code": "en", "rtl": false, "tts_voices": ["male", "female"]},
        "ar": {"name": "العربية", "code": "ar", "rtl": true, "tts_voices": ["male", "female"]},
        "es": {"name": "Español", "code": "es", "rtl": false, "tts_voices": ["male", "female"]},
        "fr": {"name": "Français", "code": "fr", "rtl": false, "tts_voices": ["male", "female"]},
        "de": {"name": "Deutsch", "code": "de", "rtl": false, "tts_voices": ["male", "female"]},
        "it": {"name": "Italiano", "code": "it", "rtl": false, "tts_voices": ["male", "female"]},
        "pt": {"name": "Português", "code": "pt", "rtl": false, "tts_voices": ["male", "female"]},
        "ru": {"name": "Русский", "code": "ru", "rtl": false, "tts_voices": ["male", "female"]},
        "ja": {"name": "日本語", "code": "ja", "rtl": false, "tts_voices": ["male", "female"]},
        "ko": {"name": "한국어", "code": "ko", "rtl": false, "tts_voices": ["male", "female"]},
        "zh": {"name": "中文", "code": "zh", "rtl": false, "tts_voices": ["male", "female"]}
    }', 'Language configurations with TTS support')
ON CONFLICT (key) DO NOTHING;

-- Sample quality presets
INSERT INTO system_settings (key, value, description) VALUES
    ('quality_presets', '{
        "low": {"width": 480, "height": 640, "fps": 24, "bitrate": "500k", "audio_bitrate": "64k"},
        "medium": {"width": 720, "height": 960, "fps": 30, "bitrate": "1500k", "audio_bitrate": "128k"},
        "high": {"width": 1080, "height": 1440, "fps": 30, "bitrate": "3000k", "audio_bitrate": "192k"}
    }', 'Video quality presets with encoding settings')
ON CONFLICT (key) DO NOTHING;

-- Sample error messages for different scenarios
INSERT INTO system_settings (key, value, description) VALUES
    ('error_messages', '{
        "file_too_large": "File size exceeds the maximum limit",
        "unsupported_format": "File format is not supported",
        "processing_failed": "Video processing failed. Please try again",
        "quota_exceeded": "You have reached your video creation limit",
        "storage_full": "Storage limit exceeded. Please upgrade your plan",
        "invalid_image": "Invalid or corrupted image file",
        "text_too_long": "Text content exceeds maximum length",
        "rate_limit": "Too many requests. Please wait before trying again",
        "maintenance": "Service is temporarily unavailable for maintenance"
    }', 'Error messages for different scenarios')
ON CONFLICT (key) DO NOTHING;

-- Sample notification templates
INSERT INTO system_settings (key, value, description) VALUES
    ('notification_templates', '{
        "video_completed": {
            "title": "Video Ready!",
            "message": "Your video \"{title}\" has been processed successfully.",
            "action": "View Video"
        },
        "video_failed": {
            "title": "Processing Failed",
            "message": "We encountered an error while processing your video \"{title}\". Please try again.",
            "action": "Retry"
        },
        "storage_warning": {
            "title": "Storage Almost Full",
            "message": "You are using {percentage}% of your storage. Consider upgrading your plan.",
            "action": "Upgrade"
        },
        "quota_warning": {
            "title": "Quota Almost Reached",
            "message": "You have {remaining} video creations left this month.",
            "action": "Upgrade"
        }
    }', 'Notification templates for different events')
ON CONFLICT (key) DO NOTHING;

-- Sample feature flags
INSERT INTO system_settings (key, value, description) VALUES
    ('feature_flags', '{
        "google_auth": true,
        "video_download": true,
        "video_sharing": true,
        "analytics": true,
        "dark_mode": true,
        "rtl_support": true,
        "advanced_settings": false,
        "batch_processing": false,
        "api_access": false,
        "custom_voices": false
    }', 'Feature flags for enabling/disabling features')
ON CONFLICT (key) DO NOTHING;

-- Sample API rate limits
INSERT INTO system_settings (key, value, description) VALUES
    ('rate_limits', '{
        "video_creation": {"free": 5, "pro": 50, "premium": 200},
        "api_requests": {"free": 100, "pro": 1000, "premium": 10000},
        "file_uploads": {"free": 10, "pro": 100, "premium": 500},
        "downloads": {"free": 20, "pro": 200, "premium": 1000}
    }', 'Rate limits per hour for different user tiers')
ON CONFLICT (key) DO NOTHING;

-- Create some sample data for development (only if in development mode)
-- Note: This should only be run in development environment

-- Sample user profile (this would normally be created by the auth trigger)
-- INSERT INTO user_profiles (id, email, full_name, subscription_tier) VALUES
--     ('00000000-0000-0000-0000-000000000001', 'demo@veo7.com', 'Demo User', 'pro')
-- ON CONFLICT (id) DO NOTHING;

-- Sample videos for the demo user
-- INSERT INTO videos (id, user_id, title, description, text_content, status, settings) VALUES
--     (
--         '00000000-0000-0000-0000-000000000001',
--         '00000000-0000-0000-0000-000000000001',
--         'Welcome to VEO7',
--         'A sample welcome video demonstrating the platform capabilities',
--         'Welcome to VEO7, the revolutionary platform for creating AI-powered talking videos. Transform your ideas into engaging visual content with just a few clicks.',
--         'completed',
--         '{"quality": "high", "speed": 1.0, "voice": "female", "language": "en"}'::jsonb
--     ),
--     (
--         '00000000-0000-0000-0000-000000000002',
--         '00000000-0000-0000-0000-000000000001',
--         'Arabic Demo Video',
--         'مثال على فيديو باللغة العربية',
--         'مرحباً بكم في منصة VEO7، المنصة الثورية لإنشاء مقاطع فيديو ناطقة بالذكاء الاصطناعي. حولوا أفكاركم إلى محتوى بصري جذاب ببضع نقرات فقط.',
--         'completed',
--         '{"quality": "medium", "speed": 0.9, "voice": "male", "language": "ar"}'::jsonb
--     )
-- ON CONFLICT (id) DO NOTHING;

-- Sample processing logs for demo videos
-- INSERT INTO video_processing_logs (video_id, step, status, message, progress, completed_at) VALUES
--     ('00000000-0000-0000-0000-000000000001', 'validation', 'completed', 'Input validation successful', 100, NOW() - INTERVAL '5 minutes'),
--     ('00000000-0000-0000-0000-000000000001', 'image_processing', 'completed', 'Face image processed successfully', 100, NOW() - INTERVAL '4 minutes'),
--     ('00000000-0000-0000-0000-000000000001', 'audio_generation', 'completed', 'Speech audio generated', 100, NOW() - INTERVAL '3 minutes'),
--     ('00000000-0000-0000-0000-000000000001', 'face_detection', 'completed', 'Face landmarks detected', 100, NOW() - INTERVAL '2 minutes'),
--     ('00000000-0000-0000-0000-000000000001', 'video_synthesis', 'completed', 'Talking video synthesized', 100, NOW() - INTERVAL '1 minute'),
--     ('00000000-0000-0000-0000-000000000001', 'post_processing', 'completed', 'Final processing completed', 100, NOW())
-- ON CONFLICT (id) DO NOTHING;

-- Function to clean up old processing logs (for maintenance)
CREATE OR REPLACE FUNCTION cleanup_old_processing_logs()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM video_processing_logs 
    WHERE started_at < NOW() - INTERVAL '30 days';
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get system statistics
CREATE OR REPLACE FUNCTION get_system_stats()
RETURNS TABLE (
    total_users INTEGER,
    total_videos INTEGER,
    total_views INTEGER,
    processing_videos INTEGER,
    storage_used BIGINT,
    videos_today INTEGER,
    active_users_today INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT COUNT(*)::INTEGER FROM user_profiles) as total_users,
        (SELECT COUNT(*)::INTEGER FROM videos) as total_videos,
        (SELECT COALESCE(SUM(views), 0)::INTEGER FROM videos) as total_views,
        (SELECT COUNT(*)::INTEGER FROM videos WHERE status = 'processing') as processing_videos,
        (SELECT COALESCE(SUM(storage_used), 0) FROM user_profiles) as storage_used,
        (SELECT COUNT(*)::INTEGER FROM videos WHERE created_at >= CURRENT_DATE) as videos_today,
        (SELECT COUNT(DISTINCT user_id)::INTEGER FROM videos WHERE created_at >= CURRENT_DATE) as active_users_today;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create a view for video analytics
CREATE OR REPLACE VIEW video_analytics AS
SELECT 
    v.id,
    v.title,
    v.user_id,
    v.status,
    v.views,
    v.duration,
    v.file_size,
    v.created_at,
    up.email as user_email,
    up.subscription_tier,
    COUNT(vv.id) as unique_views,
    AVG(vv.watch_duration) as avg_watch_duration,
    MAX(vv.viewed_at) as last_viewed_at
FROM videos v
LEFT JOIN user_profiles up ON v.user_id = up.id
LEFT JOIN video_views vv ON v.id = vv.video_id
GROUP BY v.id, v.title, v.user_id, v.status, v.views, v.duration, v.file_size, v.created_at, up.email, up.subscription_tier;

-- Grant necessary permissions for the analytics view
-- GRANT SELECT ON video_analytics TO authenticated;

COMMENT ON TABLE user_profiles IS 'Extended user profiles with subscription and usage information';
COMMENT ON TABLE videos IS 'User-generated videos with metadata and processing status';
COMMENT ON TABLE video_processing_logs IS 'Detailed logs of video processing steps';
COMMENT ON TABLE video_views IS 'Analytics data for video views and engagement';
COMMENT ON TABLE user_sessions IS 'User session tracking for analytics';
COMMENT ON TABLE system_settings IS 'System-wide configuration settings';

COMMENT ON FUNCTION increment_video_views(UUID) IS 'Safely increment video view count';
COMMENT ON FUNCTION update_user_storage_usage(UUID) IS 'Recalculate user storage usage';
COMMENT ON FUNCTION get_user_stats(UUID) IS 'Get comprehensive user statistics';
COMMENT ON FUNCTION get_system_stats() IS 'Get system-wide statistics';
COMMENT ON FUNCTION cleanup_old_processing_logs() IS 'Clean up old processing logs for maintenance';