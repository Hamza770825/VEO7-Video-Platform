"""
Supabase Database Client
Handles authentication, storage, and database operations
"""

import os
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from datetime import datetime
import asyncio
from functools import wraps
import logging

# إعداد التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseClient:
    def __init__(self):
        """Initialize Supabase client"""
        self.url = os.getenv("SUPABASE_URL", "")
        self.key = os.getenv("SUPABASE_ANON_KEY", "")
        self.service_key = os.getenv("SUPABASE_SERVICE_KEY", "")
        
        # Check if using demo/test credentials or placeholder values
        self.is_demo_mode = (
            self.url == "https://demo.supabase.co" or 
            self.key == "demo_anon_key_for_testing" or
            self.url == "https://your-project.supabase.co" or
            self.key == "your-anon-key-here" or
            not self.url or not self.key or
            "demo" in self.url.lower() or
            "test" in self.url.lower() or
            "placeholder" in self.url.lower()
        )
        
        if self.is_demo_mode:
            logger.warning("⚠️  Warning: Using demo Supabase credentials. Some features will be mocked.")
            self.client = None
        else:
            try:
                self.client: Client = create_client(self.url, self.key)
                logger.info("✅ Successfully connected to Supabase")
            except Exception as e:
                logger.error(f"⚠️  Warning: Failed to connect to Supabase: {e}")
                self.is_demo_mode = True
                self.client = None
        
        self.storage_bucket = "videos"
    
    def async_wrapper(func):
        """Wrapper to handle async operations with Supabase"""
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: func(self, *args, **kwargs))
        return wrapper
    
    @async_wrapper
    def register_user(self, email: str, password: str, full_name: str = "") -> Dict[str, Any]:
        """Register a new user"""
        try:
            if self.is_demo_mode:
                # Mock response for demo mode - skip email validation in demo
                user_id = f"demo-user-{abs(hash(email)) % 10000}"
                return {
                    "success": True,
                    "message": "تم إنشاء الحساب بنجاح (وضع العرض التوضيحي)",
                    "user": {
                        "id": user_id,
                        "email": email,
                        "full_name": full_name,
                        "email_confirmed": False
                    }
                }
            
            # Basic email validation for production mode only
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                return {
                    "success": False,
                    "message": "عنوان البريد الإلكتروني غير صحيح"
                }
            
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "full_name": full_name
                    }
                }
            })
            
            if response.user:
                return {
                    "success": True,
                    "message": "تم إنشاء الحساب بنجاح. يرجى التحقق من بريدك الإلكتروني",
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "full_name": full_name,
                        "email_confirmed": response.user.email_confirmed_at is not None
                    }
                }
            else:
                return {
                    "success": False,
                    "message": "فشل في إنشاء الحساب"
                }
                
        except Exception as e:
            logger.error(f"خطأ في تسجيل المستخدم: {e}")
            return {
                "success": False,
                "message": f"خطأ في تسجيل المستخدم: {str(e)}"
            }
    
    @async_wrapper
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Login user"""
        try:
            if self.is_demo_mode:
                # Mock response for demo mode
                user_id = f"demo-user-{abs(hash(email)) % 10000}"
                return {
                    "success": True,
                    "message": "تم تسجيل الدخول بنجاح (وضع العرض التوضيحي)",
                    "user": {
                        "id": user_id,
                        "email": email,
                        "access_token": f"demo-token-{user_id}"
                    }
                }
            
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                # الحصول على بيانات المستخدم من جدول profiles
                profile_response = self.client.table("profiles").select("*").eq("id", response.user.id).execute()
                
                profile_data = {}
                if profile_response.data:
                    profile_data = profile_response.data[0]
                
                return {
                    "success": True,
                    "message": "تم تسجيل الدخول بنجاح",
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "access_token": response.session.access_token if response.session else None,
                        "profile": profile_data
                    }
                }
            else:
                return {
                    "success": False,
                    "message": "بيانات تسجيل الدخول غير صحيحة"
                }
                
        except Exception as e:
            logger.error(f"خطأ في تسجيل الدخول: {e}")
            return {
                "success": False,
                "message": f"خطأ في تسجيل الدخول: {str(e)}"
            }
    
    @async_wrapper
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile"""
        try:
            if self.is_demo_mode:
                return {
                    "success": True,
                    "profile": {
                        "id": "demo_user_id",
                        "email": "demo@example.com",
                        "full_name": "مستخدم تجريبي",
                        "subscription_plan": "free",
                        "credits_remaining": 10
                    }
                }
            
            # البحث في جدول users أولاً
            response = self.client.table("users").select("*").eq("id", user_id).execute()
            
            if response.data:
                return {
                    "success": True,
                    "profile": response.data[0]
                }
            
            # إذا لم يوجد في users، ابحث في profiles
            response = self.client.table("profiles").select("*").eq("id", user_id).execute()
            
            if response.data:
                return {
                    "success": True,
                    "profile": response.data[0]
                }
            
            return {
                "success": False,
                "message": "لم يتم العثور على ملف تعريف المستخدم"
            }
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على ملف تعريف المستخدم: {e}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على ملف تعريف المستخدم: {str(e)}"
            }
    
    @async_wrapper
    def resend_verification_email(self, email: str) -> Dict[str, Any]:
        """Resend verification email with improved error handling"""
        import re
        
        try:
            # Validate email format first
            if not email or not email.strip():
                return {
                    "success": False,
                    "message": "عنوان البريد الإلكتروني مطلوب"
                }
            
            # Basic email format validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email.strip()):
                return {
                    "success": False,
                    "message": "تنسيق البريد الإلكتروني غير صحيح"
                }
            
            # Check for test/example emails that Supabase might reject
            email_lower = email.lower().strip()
            test_domains = ['example.com', 'test.com', 'localhost', '127.0.0.1']
            if any(domain in email_lower for domain in test_domains):
                if self.is_demo_mode:
                    return {
                        "success": True,
                        "message": "Demo mode: تم إرسال رابط التحقق بنجاح (وضع العرض التوضيحي - لن يتم إرسال بريد إلكتروني فعلي)"
                    }
                else:
                    return {
                        "success": False,
                        "message": "البريد الإلكتروني غير صحيح أو غير موجود."
                    }
            
            if self.is_demo_mode:
                return {
                    "success": True,
                    "message": "Demo mode: تم إرسال رابط التحقق بنجاح (وضع العرض التوضيحي - لن يتم إرسال بريد إلكتروني فعلي)"
                }
            
            # Use sign_in_with_otp to resend verification email
            # This will send a new OTP/verification email to the user
            response = self.client.auth.sign_in_with_otp({
                "email": email.strip(),
                "options": {
                    "should_create_user": False  # Don't create new user, just resend to existing
                }
            })
            
            # For OTP/verification emails, response.user will be None but it's still successful
            # Check if response has data attribute and no error
            if hasattr(response, 'data') and response.data is not None:
                return {
                    "success": True,
                    "message": "تم إرسال رابط التحقق الجديد إلى بريدك الإلكتروني. يرجى التحقق من صندوق الوارد وملف الرسائل غير المرغوب فيها."
                }
            else:
                return {
                    "success": False,
                    "message": "فشل في إرسال رابط التحقق"
                }
            
        except Exception as e:
            error_msg = str(e).lower()
            logger.error(f"خطأ في إرسال رابط التحقق: {e}")
            
            # معالجة أنواع مختلفة من الأخطاء
            if "rate limit" in error_msg or "too many requests" in error_msg:
                return {
                    "success": False,
                    "message": "تم إرسال عدد كبير من الطلبات. يرجى الانتظار قبل المحاولة مرة أخرى."
                }
            elif "invalid" in error_msg or "malformed" in error_msg or "email address" in error_msg:
                return {
                    "success": False,
                    "message": "البريد الإلكتروني غير صحيح أو غير موجود."
                }
            elif "not found" in error_msg or "user not found" in error_msg:
                return {
                    "success": False,
                    "message": "البريد الإلكتروني غير صحيح أو غير موجود."
                }
            elif "already confirmed" in error_msg or "email_confirmed" in error_msg:
                return {
                    "success": False,
                    "message": "تم تأكيد البريد الإلكتروني بالفعل. يمكنك تسجيل الدخول الآن."
                }
            elif "provide either an email or phone" in error_msg:
                return {
                    "success": False,
                    "message": "عنوان البريد الإلكتروني مطلوب"
                }
            else:
                return {
                    "success": False,
                    "message": "البريد الإلكتروني غير صحيح أو غير موجود."
                }
    
    def sign_in_with_google(self, redirect_url: str = None) -> Dict[str, Any]:
        """Sign in with Google"""
        try:
            if self.is_demo_mode:
                return {
                    "success": True,
                    "message": "تم تسجيل الدخول بـ Google بنجاح (وضع العرض التوضيحي)",
                    "url": "https://demo.google.com/oauth"
                }
            
            response = self.client.auth.sign_in_with_oauth({
                "provider": "google",
                "options": {
                    "redirect_to": redirect_url or f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/auth/callback"
                }
            })
            
            return {
                "success": True,
                "message": "تم إنشاء رابط تسجيل الدخول بـ Google",
                "url": response.url
            }
            
        except Exception as e:
            logger.error(f"خطأ في تسجيل الدخول بـ Google: {e}")
            return {
                "success": False,
                "message": f"خطأ في تسجيل الدخول بـ Google: {str(e)}"
            }

    async def upload_video(self, video_data: bytes, filename: str) -> str:
        """Upload video to Supabase Storage"""
        try:
            if self.is_demo_mode:
                # Mock response for demo mode
                return f"https://demo.supabase.co/storage/v1/object/public/videos/{filename}"
            
            # Upload to storage
            response = self.client.storage.from_(self.storage_bucket).upload(
                filename, 
                video_data,
                file_options={"content-type": "video/mp4"}
            )
            
            if response.status_code == 200:
                # Get public URL
                public_url = self.client.storage.from_(self.storage_bucket).get_public_url(filename)
                return public_url
            else:
                raise Exception(f"Upload failed: {response.status_code}")
                
        except Exception as e:
            raise Exception(f"Upload error: {str(e)}")
    
    async def save_video_record(self, video_id: str, user_id: str, title: str, description: str, video_url: str, language: str) -> Dict[str, Any]:
        """Save video record to database"""
        try:
            if self.is_demo_mode:
                # Mock response for demo mode
                return {
                    "id": video_id,
                    "user_id": user_id,
                    "title": title,
                    "description": description,
                    "video_url": video_url,
                    "language": language,
                    "created_at": datetime.now().isoformat(),
                    "status": "completed"
                }
            
            video_data = {
                "id": video_id,
                "user_id": user_id,
                "title": title,
                "description": description,
                "video_url": video_url,
                "language": language,
                "created_at": datetime.now().isoformat(),
                "status": "completed"
            }
            
            response = self.client.table("videos").insert(video_data).execute()
            
            if response.data:
                return response.data[0]
            else:
                raise Exception("Failed to save video record")
                
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")
    
    @async_wrapper
    def get_user_videos(self, user_id: str, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """Get user videos"""
        try:
            if self.is_demo_mode:
                # Mock response for demo mode
                return {
                    "success": True,
                    "videos": [
                        {
                            "id": f"demo-video-{i}",
                            "user_id": user_id,
                            "title": f"Demo Video {i}",
                            "description": f"This is demo video {i}",
                            "video_url": f"https://demo.supabase.co/storage/v1/object/public/videos/demo-video-{i}.mp4",
                            "language": "ar",
                            "created_at": datetime.now().isoformat(),
                            "status": "completed"
                        }
                        for i in range(1, 4)
                    ],
                    "total": 3
                }
            
            response = self.client.table("videos").select("*").eq("user_id", user_id).order("created_at", desc=True).range(offset, offset + limit - 1).execute()
            
            # الحصول على العدد الإجمالي
            count_response = self.client.table("videos").select("id", count="exact").eq("user_id", user_id).execute()
            
            return {
                "success": True,
                "videos": response.data,
                "total": count_response.count
            }
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على فيديوهات المستخدم: {e}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على فيديوهات المستخدم: {str(e)}"
            }
    
    @async_wrapper
    def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            if self.is_demo_mode:
                return {
                    "success": True,
                    "stats": {
                        "total_videos": 5,
                        "total_views": 150,
                        "total_duration": 3600,
                        "credits_used": 5,
                        "credits_remaining": 5,
                        "followers_count": 25,
                        "following_count": 15,
                        "likes_received": 75,
                        "comments_received": 30
                    }
                }
            
            # استخدام الدالة المخصصة للحصول على الإحصائيات
            response = self.client.rpc("get_user_dashboard_stats", {"user_uuid": user_id}).execute()
            
            if response.data:
                return {
                    "success": True,
                    "stats": response.data
                }
            
            return {
                "success": False,
                "message": "لم يتم العثور على إحصائيات المستخدم"
            }
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على إحصائيات المستخدم: {e}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على إحصائيات المستخدم: {str(e)}"
            }
    
    @async_wrapper
    def search_videos(self, query: str, filters: Dict[str, Any] = None, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Search videos with advanced filters"""
        try:
            if self.is_demo_mode:
                return {
                    "success": True,
                    "videos": [
                        {
                            "id": f"demo-search-{i}",
                            "title": f"نتيجة البحث {i}: {query}",
                            "description": f"هذا فيديو تجريبي يحتوي على: {query}",
                            "video_url": f"https://demo.supabase.co/storage/v1/object/public/videos/search-{i}.mp4",
                            "thumbnail_url": f"https://demo.supabase.co/storage/v1/object/public/thumbnails/search-{i}.jpg",
                            "duration": 120 + i * 30,
                            "views": 100 + i * 50,
                            "likes": 10 + i * 5,
                            "created_at": datetime.now().isoformat(),
                            "user": {
                                "id": f"demo-user-{i}",
                                "username": f"user{i}",
                                "avatar_url": f"https://demo.supabase.co/storage/v1/object/public/avatars/user{i}.jpg"
                            }
                        }
                        for i in range(1, min(limit + 1, 6))
                    ],
                    "total": 5
                }
            
            # استخدام دالة البحث المتقدم
            params = {
                "search_term": query,
                "limit_count": limit,
                "offset_count": offset
            }
            
            if filters:
                # تحويل أسماء المعاملات لتتطابق مع دالة SQL
                if "category" in filters:
                    # يمكن إضافة فلتر الفئة لاحقاً
                    pass
                if "language" in filters:
                    # يمكن إضافة فلتر اللغة لاحقاً
                    pass
                if "duration_min" in filters:
                    params["duration_min"] = filters["duration_min"]
                if "duration_max" in filters:
                    params["duration_max"] = filters["duration_max"]
                if "sort_by" in filters:
                    params["sort_by"] = filters["sort_by"]
            
            response = self.client.rpc("advanced_search", params).execute()
            
            return {
                "success": True,
                "videos": response.data if response.data else [],
                "total": len(response.data) if response.data else 0
            }
            
        except Exception as e:
            logger.error(f"خطأ في البحث عن الفيديوهات: {e}")
            return {
                "success": False,
                "message": f"خطأ في البحث عن الفيديوهات: {str(e)}"
            }
    
    @async_wrapper
    def get_trending_videos(self, limit: int = 20, time_period: str = "week") -> Dict[str, Any]:
        """Get trending videos"""
        try:
            if self.is_demo_mode:
                return {
                    "success": True,
                    "videos": [
                        {
                            "id": f"demo-trending-{i}",
                            "title": f"فيديو رائج {i}",
                            "description": f"هذا فيديو رائج رقم {i}",
                            "video_url": f"https://demo.supabase.co/storage/v1/object/public/videos/trending-{i}.mp4",
                            "thumbnail_url": f"https://demo.supabase.co/storage/v1/object/public/thumbnails/trending-{i}.jpg",
                            "duration": 180 + i * 20,
                            "views": 1000 + i * 200,
                            "likes": 50 + i * 10,
                            "created_at": datetime.now().isoformat(),
                            "user": {
                                "id": f"demo-user-{i}",
                                "username": f"creator{i}",
                                "avatar_url": f"https://demo.supabase.co/storage/v1/object/public/avatars/creator{i}.jpg"
                            }
                        }
                        for i in range(1, min(limit + 1, 11))
                    ]
                }
            
            response = self.client.rpc("get_trending_videos", {
                "limit_count": limit,
                "time_period": time_period
            }).execute()
            
            return {
                "success": True,
                "videos": response.data if response.data else []
            }
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على الفيديوهات الرائجة: {e}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على الفيديوهات الرائجة: {str(e)}"
            }
    
    @async_wrapper
    def get_recommended_videos(self, user_id: str, limit: int = 20) -> Dict[str, Any]:
        """Get recommended videos for user"""
        try:
            if self.is_demo_mode:
                return {
                    "success": True,
                    "videos": [
                        {
                            "id": f"demo-recommended-{i}",
                            "title": f"فيديو مقترح {i}",
                            "description": f"هذا فيديو مقترح خصيصاً لك رقم {i}",
                            "video_url": f"https://demo.supabase.co/storage/v1/object/public/videos/recommended-{i}.mp4",
                            "thumbnail_url": f"https://demo.supabase.co/storage/v1/object/public/thumbnails/recommended-{i}.jpg",
                            "duration": 150 + i * 25,
                            "views": 500 + i * 100,
                            "likes": 25 + i * 8,
                            "created_at": datetime.now().isoformat(),
                            "user": {
                                "id": f"demo-user-{i}",
                                "username": f"recommender{i}",
                                "avatar_url": f"https://demo.supabase.co/storage/v1/object/public/avatars/recommender{i}.jpg"
                            }
                        }
                        for i in range(1, min(limit + 1, 11))
                    ]
                }
            
            response = self.client.rpc("get_recommended_videos", {
                "user_uuid": user_id,
                "limit_count": limit
            }).execute()
            
            return {
                "success": True,
                "videos": response.data if response.data else []
            }
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على الفيديوهات المقترحة: {e}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على الفيديوهات المقترحة: {str(e)}"
            }
    
    @async_wrapper
    def like_video(self, user_id: str, video_id: str) -> Dict[str, Any]:
        """Like or unlike a video"""
        try:
            if self.is_demo_mode:
                return {
                    "success": True,
                    "message": "تم الإعجاب بالفيديو (وضع العرض التوضيحي)",
                    "liked": True
                }
            
            # التحقق من وجود إعجاب سابق
            existing_like = self.client.table("likes").select("*").eq("user_id", user_id).eq("video_id", video_id).execute()
            
            if existing_like.data:
                # إلغاء الإعجاب
                self.client.table("likes").delete().eq("user_id", user_id).eq("video_id", video_id).execute()
                return {
                    "success": True,
                    "message": "تم إلغاء الإعجاب",
                    "liked": False
                }
            else:
                # إضافة إعجاب
                self.client.table("likes").insert({
                    "user_id": user_id,
                    "video_id": video_id,
                    "created_at": datetime.now().isoformat()
                }).execute()
                return {
                    "success": True,
                    "message": "تم الإعجاب بالفيديو",
                    "liked": True
                }
            
        except Exception as e:
            logger.error(f"خطأ في الإعجاب بالفيديو: {e}")
            return {
                "success": False,
                "message": f"خطأ في الإعجاب بالفيديو: {str(e)}"
            }
    
    @async_wrapper
    def add_comment(self, user_id: str, video_id: str, content: str, parent_id: str = None) -> Dict[str, Any]:
        """Add a comment to a video"""
        try:
            if self.is_demo_mode:
                return {
                    "success": True,
                    "comment": {
                        "id": f"demo-comment-{abs(hash(content)) % 10000}",
                        "user_id": user_id,
                        "video_id": video_id,
                        "content": content,
                        "parent_id": parent_id,
                        "created_at": datetime.now().isoformat(),
                        "user": {
                            "username": "مستخدم تجريبي",
                            "avatar_url": "https://demo.supabase.co/storage/v1/object/public/avatars/demo.jpg"
                        }
                    }
                }
            
            comment_data = {
                "user_id": user_id,
                "video_id": video_id,
                "content": content,
                "created_at": datetime.now().isoformat()
            }
            
            if parent_id:
                comment_data["parent_id"] = parent_id
            
            response = self.client.table("comments").insert(comment_data).execute()
            
            return {
                "success": True,
                "comment": response.data[0] if response.data else None
            }
            
        except Exception as e:
            logger.error(f"خطأ في إضافة التعليق: {e}")
            return {
                "success": False,
                "message": f"خطأ في إضافة التعليق: {str(e)}"
            }
    
    @async_wrapper
    def get_video_comments(self, video_id: str, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """Get comments for a video"""
        try:
            if self.is_demo_mode:
                return {
                    "success": True,
                    "comments": [
                        {
                            "id": f"demo-comment-{i}",
                            "user_id": f"demo-user-{i}",
                            "video_id": video_id,
                            "content": f"تعليق تجريبي رقم {i} على هذا الفيديو الرائع!",
                            "created_at": datetime.now().isoformat(),
                            "user": {
                                "username": f"مستخدم{i}",
                                "avatar_url": f"https://demo.supabase.co/storage/v1/object/public/avatars/user{i}.jpg"
                            },
                            "replies": []
                        }
                        for i in range(1, min(limit + 1, 6))
                    ],
                    "total": 5
                }
            
            response = self.client.table("comments").select("""
                *,
                user:profiles(username, avatar_url),
                replies:comments(*, user:profiles(username, avatar_url))
            """).eq("video_id", video_id).is_("parent_id", "null").order("created_at", desc=True).range(offset, offset + limit - 1).execute()
            
            return {
                "success": True,
                "comments": response.data if response.data else [],
                "total": len(response.data) if response.data else 0
            }
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على التعليقات: {e}")
            return {
                "success": False,
                "message": f"خطأ في الحصول على التعليقات: {str(e)}"
            }
    
    @async_wrapper
    def follow_user(self, follower_id: str, following_id: str) -> Dict[str, Any]:
        """Follow or unfollow a user"""
        try:
            if self.is_demo_mode:
                return {
                    "success": True,
                    "message": "تم متابعة المستخدم (وضع العرض التوضيحي)",
                    "following": True
                }
            
            # التحقق من وجود متابعة سابقة
            existing_follow = self.client.table("follows").select("*").eq("follower_id", follower_id).eq("following_id", following_id).execute()
            
            if existing_follow.data:
                # إلغاء المتابعة
                self.client.table("follows").delete().eq("follower_id", follower_id).eq("following_id", following_id).execute()
                return {
                    "success": True,
                    "message": "تم إلغاء المتابعة",
                    "following": False
                }
            else:
                # إضافة متابعة
                self.client.table("follows").insert({
                    "follower_id": follower_id,
                    "following_id": following_id,
                    "created_at": datetime.now().isoformat()
                }).execute()
                return {
                    "success": True,
                    "message": "تم متابعة المستخدم",
                    "following": True
                }
            
        except Exception as e:
            logger.error(f"خطأ في متابعة المستخدم: {e}")
            return {
                "success": False,
                "message": f"خطأ في متابعة المستخدم: {str(e)}"
            }
    
    @async_wrapper
    def increment_video_views(self, video_id: str, user_id: str = None) -> Dict[str, Any]:
        """Increment video view count"""
        try:
            if self.is_demo_mode:
                return {
                    "success": True,
                    "message": "تم تسجيل المشاهدة (وضع العرض التوضيحي)"
                }
            
            # استخدام دالة SQL لزيادة عدد المشاهدات
            response = self.client.rpc("increment_video_views", {
                "video_uuid": video_id,
                "viewer_uuid": user_id
            }).execute()
            
            return {
                "success": True,
                "message": "تم تسجيل المشاهدة"
            }
            
        except Exception as e:
            logger.error(f"خطأ في تسجيل المشاهدة: {e}")
            return {
                "success": False,
                "message": f"خطأ في تسجيل المشاهدة: {str(e)}"
            }
    
    @async_wrapper
    def get_video(self, video_id: str) -> Dict[str, Any]:
        """Get video by ID"""
        try:
            if self.is_demo_mode:
                # Mock response for demo mode
                return {
                    "id": video_id,
                    "user_id": "demo-user-123",
                    "title": "Demo Video",
                    "description": "This is a demo video",
                    "video_url": f"https://demo.supabase.co/storage/v1/object/public/videos/{video_id}.mp4",
                    "language": "ar",
                    "created_at": datetime.now().isoformat(),
                    "status": "completed"
                }
            
            response = self.client.table("videos").select("*").eq("id", video_id).execute()
            return response.data[0] if response.data else None
            
        except Exception as e:
            raise Exception(f"Fetch video error: {str(e)}")
    
    @async_wrapper
    def delete_video(self, video_id: str, user_id: str) -> bool:
        """Delete video and its record"""
        try:
            if self.is_demo_mode:
                # Mock response for demo mode
                return True
            
            # Get video record
            video_response = self.client.table("videos").select("*").eq("id", video_id).eq("user_id", user_id).execute()
            
            if not video_response.data:
                raise Exception("Video not found")
            
            video_record = video_response.data[0]
            
            # Delete from storage
            file_name = f"{user_id}/{video_id}.mp4"
            self.client.storage.from_(self.storage_bucket).remove([file_name])
            
            # Delete from database
            self.client.table("videos").delete().eq("id", video_id).eq("user_id", user_id).execute()
            
            return True
            
        except Exception as e:
            raise Exception(f"Delete error: {str(e)}")
    
    @async_wrapper
    def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        try:
            if self.is_demo_mode:
                return {
                    "success": True,
                    "profile": profile_data
                }
            
            profile_data["updated_at"] = datetime.now().isoformat()
            
            # تحديث في جدول profiles
            response = self.client.table("profiles").update(profile_data).eq("id", user_id).execute()
            
            # تحديث في جدول users أيضاً
            self.client.table("users").update(profile_data).eq("id", user_id).execute()
            
            return {
                "success": True,
                "profile": response.data[0] if response.data else None
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحديث ملف تعريف المستخدم: {e}")
            return {
                "success": False,
                "message": f"خطأ في تحديث ملف تعريف المستخدم: {str(e)}"
            }
    
    def _get_file_size(self, file_path: str) -> int:
        """Get file size in bytes"""
        try:
            if os.path.exists(file_path):
                return os.path.getsize(file_path)
            return 0
        except:
            return 0