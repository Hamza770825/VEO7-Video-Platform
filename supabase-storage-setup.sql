-- VEO7 Video Platform - Supabase Storage Setup
-- This file contains all the SQL commands needed to set up storage buckets

-- Create storage buckets
INSERT INTO storage.buckets (id, name, public) VALUES 
('user-uploads', 'user-uploads', false),
('generated-videos', 'generated-videos', false),
('user-avatars', 'user-avatars', true);

-- Create storage policies

-- User uploads bucket policies (images, audio files)
CREATE POLICY "Users can upload their own files" ON storage.objects
    FOR INSERT WITH CHECK (
        bucket_id = 'user-uploads' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can view their own uploads" ON storage.objects
    FOR SELECT USING (
        bucket_id = 'user-uploads' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can update their own uploads" ON storage.objects
    FOR UPDATE USING (
        bucket_id = 'user-uploads' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can delete their own uploads" ON storage.objects
    FOR DELETE USING (
        bucket_id = 'user-uploads' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );

-- Generated videos bucket policies
CREATE POLICY "Users can view their own generated videos" ON storage.objects
    FOR SELECT USING (
        bucket_id = 'generated-videos' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Service role can manage generated videos" ON storage.objects
    FOR ALL USING (
        bucket_id = 'generated-videos' AND 
        auth.role() = 'service_role'
    );

-- User avatars bucket policies (public)
CREATE POLICY "Anyone can view avatars" ON storage.objects
    FOR SELECT USING (bucket_id = 'user-avatars');

CREATE POLICY "Users can upload their own avatar" ON storage.objects
    FOR INSERT WITH CHECK (
        bucket_id = 'user-avatars' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can update their own avatar" ON storage.objects
    FOR UPDATE USING (
        bucket_id = 'user-avatars' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );

CREATE POLICY "Users can delete their own avatar" ON storage.objects
    FOR DELETE USING (
        bucket_id = 'user-avatars' AND 
        auth.uid()::text = (storage.foldername(name))[1]
    );