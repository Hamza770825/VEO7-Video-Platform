"""Enhanced Video Service
Handles advanced video generation with visual effects and optimized performance
"""

import os
import cv2
import numpy as np
import asyncio
import subprocess
import tempfile
import hashlib
import json
from typing import Optional, Tuple, Dict, List
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import moviepy.editor as mp
from functools import lru_cache
try:
    import io
    import base64
    SVG_SUPPORT = True
except ImportError:
    SVG_SUPPORT = False

# استيراد خدمة نماذج الذكاء الاصطناعي
try:
    from .ai_models_service import AIModelsService
    AI_MODELS_AVAILABLE = True
except ImportError:
    AI_MODELS_AVAILABLE = False

# Enhanced video generation presets
VIDEO_PRESETS = {
    "low": {
        "fps": 15, 
        "resolution": (480, 360), 
        "bitrate": "500k",
        "codec": "libx264",
        "crf": 28,
        "effects": ["basic_animation"]
    },
    "medium": {
        "fps": 24, 
        "resolution": (720, 480), 
        "bitrate": "1000k",
        "codec": "libx264",
        "crf": 23,
        "effects": ["basic_animation", "smooth_transitions"]
    },
    "high": {
        "fps": 30, 
        "resolution": (1280, 720), 
        "bitrate": "2000k",
        "codec": "libx264",
        "crf": 20,
        "effects": ["basic_animation", "smooth_transitions", "enhanced_visuals"]
    },
    "ultra": {
        "fps": 60, 
        "resolution": (1920, 1080), 
        "bitrate": "4000k",
        "codec": "libx264",
        "crf": 18,
        "effects": ["basic_animation", "smooth_transitions", "enhanced_visuals", "premium_effects"]
    }
}

# Visual effects configuration
VISUAL_EFFECTS = {
    "basic_animation": {
        "zoom_range": (1.0, 1.05),
        "pan_range": (-10, 10),
        "fade_duration": 0.5
    },
    "smooth_transitions": {
        "transition_types": ["fade", "slide", "zoom"],
        "transition_duration": 1.0
    },
    "enhanced_visuals": {
        "color_enhancement": True,
        "sharpening": True,
        "noise_reduction": True,
        "dynamic_lighting": True
    },
    "premium_effects": {
        "particle_effects": True,
        "advanced_transitions": True,
        "motion_blur": True,
        "depth_of_field": True
    }
}

class VideoService:
    def __init__(self, temp_dir: str = "temp", output_dir: str = "outputs", cache_dir: str = "cache/video"):
        """Initialize enhanced video service"""
        self.temp_dir = temp_dir
        self.output_dir = output_dir
        self.cache_dir = cache_dir
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # تهيئة خدمة نماذج الذكاء الاصطناعي
        self.ai_models_service = None
        if AI_MODELS_AVAILABLE:
            try:
                self.ai_models_service = AIModelsService()
            except Exception as e:
                print(f"Failed to initialize AI models service: {e}")
        
        # Video settings
        self.default_fps = 25
        self.default_resolution = (512, 512)
        self.max_duration = 60  # Maximum video duration in seconds
        
        # Video cache for optimization
        self.video_cache = {}
        self._load_cache_index()
    
    def _load_cache_index(self):
        """Load video cache index"""
        cache_index_path = os.path.join(self.cache_dir, "cache_index.json")
        if os.path.exists(cache_index_path):
            try:
                with open(cache_index_path, 'r', encoding='utf-8') as f:
                    self.video_cache = json.load(f)
            except:
                self.video_cache = {}
    
    def _save_cache_index(self):
        """Save video cache index"""
        cache_index_path = os.path.join(self.cache_dir, "cache_index.json")
        try:
            with open(cache_index_path, 'w', encoding='utf-8') as f:
                json.dump(self.video_cache, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def _get_cache_key(self, image_path: str, audio_path: str, quality: str, effects: List[str]) -> str:
        """Generate cache key for video"""
        # Create hash from file contents and settings
        with open(image_path, 'rb') as f:
            image_hash = hashlib.md5(f.read()).hexdigest()[:8]
        with open(audio_path, 'rb') as f:
            audio_hash = hashlib.md5(f.read()).hexdigest()[:8]
        
        content = f"{image_hash}_{audio_hash}_{quality}_{'_'.join(sorted(effects))}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    async def generate_video(self, image_path: str, audio_path: str, 
                           output_path: str = None, quality: str = "medium",
                           effects: List[str] = None, custom_settings: Dict = None) -> str:
        """
        Generate enhanced video from image and audio with visual effects
        
        Args:
            image_path: Path to input image
            audio_path: Path to input audio
            output_path: Output video path
            quality: Video quality preset (low, medium, high, ultra)
            effects: List of visual effects to apply
            custom_settings: Custom video generation settings
            
        Returns:
            Path to generated video
        """
        # Set default effects based on quality
        if effects is None:
            effects = VIDEO_PRESETS.get(quality, VIDEO_PRESETS["medium"])["effects"]
        
        # Check cache first
        cache_key = self._get_cache_key(image_path, audio_path, quality, effects)
        if cache_key in self.video_cache:
            cached_path = self.video_cache[cache_key]
            if os.path.exists(cached_path):
                print(f"Using cached video: {cached_path}")
                return cached_path
        
        if not output_path:
            output_path = os.path.join(self.output_dir, f"video_{quality}_{hash(image_path + audio_path)}.mp4")
        
        try:
            # Get quality settings
            quality_settings = VIDEO_PRESETS.get(quality, VIDEO_PRESETS["medium"])
            if custom_settings:
                quality_settings.update(custom_settings)
            
            # Preprocess image with enhanced features
            processed_image = await self._preprocess_image_enhanced(image_path, quality_settings)
            
            # Get audio duration
            audio_duration = await self._get_audio_duration(audio_path)
            
            # Check duration limit
            if audio_duration > self.max_duration:
                raise Exception(f"Audio duration ({audio_duration}s) exceeds maximum limit ({self.max_duration}s)")
            
            # Generate video with enhanced features
            video_path = await self._generate_with_enhanced_features(
                processed_image, audio_path, output_path, audio_duration, quality_settings, effects
            )
            
            # Apply visual effects
            enhanced_video = await self._apply_visual_effects(video_path, effects, quality_settings)
            
            # Post-process video with quality optimization
            final_video = await self._postprocess_video_enhanced(enhanced_video, enhanced_video, quality_settings)
            
            # Cache the result
            self.video_cache[cache_key] = final_video
            self._save_cache_index()
            
            return final_video
            
        except Exception as e:
            raise Exception(f"Enhanced video generation failed: {str(e)}")
    
    async def _preprocess_image(self, image_path: str) -> str:
        """Preprocess input image for better results"""
        try:
            # Handle SVG files - create a simple placeholder image
            if image_path.lower().endswith('.svg'):
                # For now, create a simple colored rectangle as placeholder
                # In production, you would want to use a proper SVG renderer
                placeholder_image = Image.new('RGB', (512, 512), color='lightblue')
                temp_png_path = os.path.join(self.temp_dir, f"temp_{os.path.basename(image_path)}.png")
                placeholder_image.save(temp_png_path)
                image_path = temp_png_path
            
            # Load image
            image = Image.open(image_path)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Detect face
            face_locations = await self._detect_face(image_path)
            
            if not face_locations:
                # If no face detected, use center crop
                image = await self._center_crop_image(image)
            else:
                # Crop around detected face
                image = await self._crop_face(image, face_locations[0])
            
            # Resize to standard resolution
            image = image.resize(self.default_resolution, Image.Resampling.LANCZOS)
            
            # Enhance image quality
            image = await self._enhance_image(image)
            
            # Save processed image
            processed_path = os.path.join(self.temp_dir, f"processed_{os.path.basename(image_path)}")
            image.save(processed_path, quality=95)
            
            return processed_path
            
        except Exception as e:
            raise Exception(f"Image preprocessing failed: {str(e)}")
    
    async def _preprocess_image_enhanced(self, image_path: str, quality_settings: Dict) -> str:
        """Enhanced image preprocessing with quality-specific optimizations"""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get target resolution from quality settings
            target_resolution = quality_settings.get("resolution", (720, 480))
            
            # Smart resize with aspect ratio preservation
            image = self._smart_resize(image, target_resolution)
            
            # Apply quality-specific enhancements
            if "enhanced_visuals" in quality_settings.get("effects", []):
                image = await self._apply_image_enhancements(image)
            
            # Save processed image with quality-specific settings
            processed_path = os.path.join(self.temp_dir, f"enhanced_{os.path.basename(image_path)}")
            image.save(processed_path, quality=95, optimize=True)
            
            return processed_path
            
        except Exception as e:
            print(f"Enhanced image preprocessing failed: {str(e)}")
            return image_path
    
    def _smart_resize(self, image: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
        """Smart resize with aspect ratio preservation"""
        original_width, original_height = image.size
        target_width, target_height = target_size
        
        # Calculate aspect ratios
        original_ratio = original_width / original_height
        target_ratio = target_width / target_height
        
        if original_ratio > target_ratio:
            # Image is wider, fit by height
            new_height = target_height
            new_width = int(target_height * original_ratio)
        else:
            # Image is taller, fit by width
            new_width = target_width
            new_height = int(target_width / original_ratio)
        
        # Resize and crop to target size
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Center crop to exact target size
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        
        return image.crop((left, top, right, bottom))
    
    async def _apply_image_enhancements(self, image: Image.Image) -> Image.Image:
        """Apply advanced image enhancements"""
        try:
            # Color enhancement
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(1.15)
            
            # Contrast enhancement
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.1)
            
            # Sharpness enhancement
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.2)
            
            # Brightness adjustment
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.05)
            
            # Noise reduction (subtle blur then sharpen)
            image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
            image = image.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
            
            return image
            
        except Exception as e:
            print(f"Image enhancement failed: {str(e)}")
            return image
    
    async def _detect_face(self, image_path: str) -> list:
        """Detect faces in image using OpenCV"""
        try:
            # Load image with OpenCV
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Use OpenCV's face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # Convert to face_recognition format (top, right, bottom, left)
            face_locations = []
            for (x, y, w, h) in faces:
                face_locations.append((y, x + w, y + h, x))
            
            return face_locations
        except Exception as e:
            print(f"Face detection failed: {e}")
            return []
    
    async def _crop_face(self, image: Image.Image, face_location: tuple) -> Image.Image:
        """Crop image around detected face"""
        try:
            top, right, bottom, left = face_location
            
            # Add padding around face
            padding = 50
            height, width = image.size[1], image.size[0]
            
            left = max(0, left - padding)
            top = max(0, top - padding)
            right = min(width, right + padding)
            bottom = min(height, bottom + padding)
            
            # Crop image
            cropped = image.crop((left, top, right, bottom))
            
            return cropped
            
        except Exception as e:
            print(f"Face cropping failed: {e}")
            return image
    
    async def _center_crop_image(self, image: Image.Image) -> Image.Image:
        """Center crop image to square"""
        try:
            width, height = image.size
            size = min(width, height)
            
            left = (width - size) // 2
            top = (height - size) // 2
            right = left + size
            bottom = top + size
            
            return image.crop((left, top, right, bottom))
            
        except Exception as e:
            print(f"Center cropping failed: {e}")
            return image
    
    async def _enhance_image(self, image: Image.Image) -> Image.Image:
        """Enhance image quality"""
        try:
            # Enhance brightness
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.1)
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.1)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.2)
            
            return image
            
        except Exception as e:
            print(f"Image enhancement failed: {e}")
            return image
    
    async def _generate_with_sadtalker(self, image_path: str, audio_path: str, output_path: str) -> str:
        """Generate video using SadTalker (if available)"""
        try:
            # استخدام خدمة نماذج الذكاء الاصطناعي إذا كانت متاحة
            if self.ai_models_service:
                result = await self.ai_models_service.generate_sadtalker_video(
                    image_path=image_path,
                    audio_path=audio_path,
                    output_path=output_path
                )
                
                if result.get('success', False):
                    return result['output_path']
                else:
                    print(f"SadTalker failed: {result.get('message', 'Unknown error')}")
                    # العودة إلى الطريقة البسيطة
                    return await self._generate_simple_video(image_path, audio_path, output_path)
            else:
                # استخدام الطريقة البسيطة إذا لم تكن خدمة الذكاء الاصطناعي متاحة
                return await self._generate_simple_video(image_path, audio_path, output_path)
            
        except Exception as e:
            raise Exception(f"SadTalker generation failed: {str(e)}")
    
    async def _generate_with_wav2lip(self, image_path: str, audio_path: str, output_path: str) -> str:
        """Generate video using Wav2Lip (if available)"""
        try:
            # استخدام خدمة نماذج الذكاء الاصطناعي إذا كانت متاحة
            if self.ai_models_service:
                # أولاً نحتاج إنشاء فيديو بسيط ثم تطبيق Wav2Lip عليه
                temp_video = os.path.join(self.temp_dir, f"temp_video_{hash(image_path + audio_path)}.mp4")
                await self._generate_simple_video(image_path, audio_path, temp_video)
                
                result = await self.ai_models_service.generate_wav2lip_video(
                    video_path=temp_video,
                    audio_path=audio_path,
                    output_path=output_path
                )
                
                # تنظيف الملف المؤقت
                if os.path.exists(temp_video):
                    os.remove(temp_video)
                
                if result.get('success', False):
                    return result['output_path']
                else:
                    print(f"Wav2Lip failed: {result.get('message', 'Unknown error')}")
                    # العودة إلى الطريقة البسيطة
                    return await self._generate_simple_video(image_path, audio_path, output_path)
            else:
                # استخدام الطريقة البسيطة إذا لم تكن خدمة الذكاء الاصطناعي متاحة
                return await self._generate_simple_video(image_path, audio_path, output_path)
            
        except Exception as e:
            raise Exception(f"Wav2Lip generation failed: {str(e)}")
    
    async def _generate_simple_video(self, image_path: str, audio_path: str, output_path: str) -> str:
        """Generate simple video with static image and audio"""
        try:
            # Load image
            image = cv2.imread(image_path)
            height, width, layers = image.shape
            
            # Get audio duration
            audio_duration = await self._get_audio_duration(audio_path)
            
            # Calculate number of frames
            total_frames = int(audio_duration * self.default_fps)
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            temp_video = os.path.join(self.temp_dir, f"temp_{os.path.basename(output_path)}")
            video_writer = cv2.VideoWriter(temp_video, fourcc, self.default_fps, (width, height))
            
            # Add subtle animation (slight zoom and movement)
            for frame_num in range(total_frames):
                # Create slight zoom effect
                zoom_factor = 1.0 + 0.02 * np.sin(frame_num * 0.1)
                
                # Resize image with zoom
                new_width = int(width * zoom_factor)
                new_height = int(height * zoom_factor)
                zoomed = cv2.resize(image, (new_width, new_height))
                
                # Center crop to original size
                start_x = (new_width - width) // 2
                start_y = (new_height - height) // 2
                frame = zoomed[start_y:start_y + height, start_x:start_x + width]
                
                # Write frame
                video_writer.write(frame)
            
            video_writer.release()
            
            # Combine video with audio using moviepy
            video_clip = mp.VideoFileClip(temp_video)
            audio_clip = mp.AudioFileClip(audio_path)
            
            # Sync audio and video
            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')
            
            # Cleanup
            video_clip.close()
            audio_clip.close()
            final_clip.close()
            
            if os.path.exists(temp_video):
                os.remove(temp_video)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Simple video generation failed: {str(e)}")
    
    async def _post_process_video(self, video_path: str) -> str:
        """Post-process generated video"""
        try:
            # Load video
            clip = mp.VideoFileClip(video_path)
            
            # Apply color correction
            clip = clip.fx(mp.vfx.colorx, 1.1)  # Slight color enhancement
            
            # Apply stabilization (if needed)
            # clip = clip.fx(mp.vfx.stabilize)
            
            # Save processed video
            processed_path = video_path.replace(".mp4", "_processed.mp4")
            clip.write_videofile(processed_path, codec='libx264', audio_codec='aac')
            
            clip.close()
            
            # Replace original with processed
            os.remove(video_path)
            os.rename(processed_path, video_path)
            
            return video_path
            
        except Exception as e:
            print(f"Post-processing failed: {e}")
            return video_path  # Return original if post-processing fails
    
    async def _get_audio_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds"""
        try:
            audio_clip = mp.AudioFileClip(audio_path)
            duration = audio_clip.duration
            audio_clip.close()
            return duration
        except Exception as e:
            raise Exception(f"Audio duration calculation failed: {str(e)}")
    
    async def get_video_info(self, video_path: str) -> dict:
        """Get video information"""
        try:
            clip = mp.VideoFileClip(video_path)
            info = {
                "duration": clip.duration,
                "fps": clip.fps,
                "size": clip.size,
                "file_size": os.path.getsize(video_path)
            }
            clip.close()
            return info
        except Exception as e:
            raise Exception(f"Video info extraction failed: {str(e)}")
    
    async def create_thumbnail(self, video_path: str, time_offset: float = 1.0) -> str:
        """Create thumbnail from video"""
        try:
            clip = mp.VideoFileClip(video_path)
            
            # Extract frame at specified time
            frame = clip.get_frame(min(time_offset, clip.duration - 0.1))
            
            # Save as image
            thumbnail_path = video_path.replace(".mp4", "_thumbnail.jpg")
            Image.fromarray(frame.astype('uint8')).save(thumbnail_path, quality=85)
            
            clip.close()
            return thumbnail_path
            
        except Exception as e:
            raise Exception(f"Thumbnail creation failed: {str(e)}")
    
    def cleanup_temp_files(self):
        """Clean up temporary video files"""
        try:
            for file in os.listdir(self.temp_dir):
                if file.endswith(('.mp4', '.avi', '.mov', '.tmp')):
                    file_path = os.path.join(self.temp_dir, file)
                    # Remove files older than 1 hour
                    if os.path.getctime(file_path) < (time.time() - 3600):
                        os.remove(file_path)
        except Exception as e:
            print(f"Cleanup failed: {str(e)}")

    async def _generate_with_enhanced_features(self, image_path: str, audio_path: str, 
                                             output_path: str, duration: float, 
                                             quality_settings: Dict, effects: List[str]) -> str:
        """Generate video with enhanced features and quality settings"""
        try:
            # Try SadTalker first (better quality)
            try:
                video_path = await self._generate_with_sadtalker_enhanced(
                    image_path, audio_path, output_path, quality_settings
                )
            except Exception as e:
                print(f"Enhanced SadTalker failed: {e}, trying enhanced Wav2Lip...")
                # Fallback to enhanced Wav2Lip
                video_path = await self._generate_with_wav2lip_enhanced(
                    image_path, audio_path, output_path, quality_settings
                )
            
            return video_path
            
        except Exception as e:
            print(f"Enhanced video generation failed: {str(e)}")
            raise
    
    async def _generate_with_sadtalker_enhanced(self, image_path: str, audio_path: str, 
                                              output_path: str, quality_settings: Dict) -> str:
        """Enhanced SadTalker generation with quality settings"""
        try:
            # For now, use enhanced simple video generation
            return await self._generate_simple_video_enhanced(image_path, audio_path, output_path, quality_settings)
            
        except Exception as e:
            print(f"Enhanced SadTalker generation failed: {str(e)}")
            raise
    
    async def _generate_with_wav2lip_enhanced(self, image_path: str, audio_path: str, 
                                            output_path: str, quality_settings: Dict) -> str:
        """Enhanced Wav2Lip generation with quality settings"""
        try:
            # For now, use enhanced simple video generation
            return await self._generate_simple_video_enhanced(image_path, audio_path, output_path, quality_settings)
            
        except Exception as e:
            print(f"Enhanced Wav2Lip generation failed: {str(e)}")
            raise
    
    async def _generate_simple_video_enhanced(self, image_path: str, audio_path: str, 
                                            output_path: str, quality_settings: Dict) -> str:
        """Generate enhanced simple video with quality settings"""
        try:
            # Load image
            image = cv2.imread(image_path)
            target_resolution = quality_settings.get("resolution", (720, 480))
            
            # Resize to target resolution
            image = cv2.resize(image, target_resolution)
            height, width, layers = image.shape
            
            # Get audio duration
            audio_duration = await self._get_audio_duration(audio_path)
            
            # Calculate number of frames
            fps = quality_settings.get("fps", self.default_fps)
            total_frames = int(audio_duration * fps)
            
            # Create video writer with quality settings
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            temp_video = os.path.join(self.temp_dir, f"temp_enhanced_{os.path.basename(output_path)}")
            video_writer = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))
            
            # Enhanced animation with multiple effects
            for frame_num in range(total_frames):
                frame = image.copy()
                
                # Apply enhanced animations based on quality
                if "basic_animation" in quality_settings.get("effects", []):
                    frame = self._apply_basic_frame_animation(frame, frame_num, total_frames)
                
                if "enhanced_visuals" in quality_settings.get("effects", []):
                    frame = self._apply_enhanced_frame_visuals(frame, frame_num, total_frames)
                
                # Write frame
                video_writer.write(frame)
            
            video_writer.release()
            
            # Combine video with audio using moviepy
            video_clip = mp.VideoFileClip(temp_video)
            audio_clip = mp.AudioFileClip(audio_path)
            
            # Sync audio and video
            final_clip = video_clip.set_audio(audio_clip)
            
            # Write with quality settings
            final_clip.write_videofile(
                output_path, 
                codec=quality_settings.get("codec", "libx264"),
                bitrate=quality_settings.get("bitrate", "1000k"),
                fps=fps,
                audio_codec='aac'
            )
            
            # Cleanup
            video_clip.close()
            audio_clip.close()
            final_clip.close()
            
            if os.path.exists(temp_video):
                os.remove(temp_video)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Enhanced simple video generation failed: {str(e)}")
    
    def _apply_basic_frame_animation(self, frame, frame_num: int, total_frames: int):
        """Apply basic animation to a single frame"""
        try:
            height, width = frame.shape[:2]
            
            # Create subtle zoom effect
            zoom_factor = 1.0 + 0.03 * np.sin(frame_num * 0.05)
            
            # Resize image with zoom
            new_width = int(width * zoom_factor)
            new_height = int(height * zoom_factor)
            zoomed = cv2.resize(frame, (new_width, new_height))
            
            # Center crop to original size
            start_x = (new_width - width) // 2
            start_y = (new_height - height) // 2
            
            if start_x >= 0 and start_y >= 0:
                frame = zoomed[start_y:start_y + height, start_x:start_x + width]
            
            return frame
            
        except Exception as e:
            print(f"Basic frame animation failed: {str(e)}")
            return frame
    
    def _apply_enhanced_frame_visuals(self, frame, frame_num: int, total_frames: int):
        """Apply enhanced visual effects to a single frame"""
        try:
            # Color enhancement
            frame = cv2.convertScaleAbs(frame, alpha=1.1, beta=10)
            
            # Subtle sharpening
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            frame = cv2.filter2D(frame, -1, kernel * 0.1)
            
            # Noise reduction
            frame = cv2.bilateralFilter(frame, 9, 75, 75)
            
            return frame
            
        except Exception as e:
            print(f"Enhanced frame visuals failed: {str(e)}")
            return frame
    
    async def _apply_visual_effects(self, video_path: str, effects: List[str], 
                                  quality_settings: Dict) -> str:
        """Apply visual effects to video"""
        try:
            if not effects or len(effects) == 0:
                return video_path
            
            # Load video
            video = mp.VideoFileClip(video_path)
            
            # Apply effects based on list
            for effect in effects:
                if effect == "smooth_transitions":
                    video = await self._apply_smooth_transitions(video)
                elif effect == "premium_effects":
                    video = await self._apply_premium_effects(video)
            
            # Generate output path for effects
            effects_path = video_path.replace('.mp4', '_effects.mp4')
            
            # Write video with effects
            video.write_videofile(
                effects_path,
                codec=quality_settings.get("codec", "libx264"),
                bitrate=quality_settings.get("bitrate", "1000k"),
                fps=quality_settings.get("fps", 24),
                verbose=False,
                logger=None
            )
            
            video.close()
            
            return effects_path
            
        except Exception as e:
            print(f"Visual effects application failed: {str(e)}")
            return video_path
    
    async def _apply_smooth_transitions(self, video: mp.VideoFileClip) -> mp.VideoFileClip:
        """Apply smooth transition effects"""
        try:
            # Add fade in/out
            fade_duration = 0.5
            video = video.fadein(fade_duration).fadeout(fade_duration)
            
            return video
            
        except Exception as e:
            print(f"Smooth transitions failed: {str(e)}")
            return video
    
    async def _apply_premium_effects(self, video: mp.VideoFileClip) -> mp.VideoFileClip:
        """Apply premium visual effects"""
        try:
            # Color enhancement
            video = video.fx(mp.vfx.colorx, 1.15)
            
            return video
            
        except Exception as e:
            print(f"Premium effects failed: {str(e)}")
            return video
    
    async def _postprocess_video_enhanced(self, video_path: str, output_path: str, quality_settings: Dict) -> str:
        """Enhanced post-processing with quality-specific optimizations"""
        try:
            # Load video
            video = mp.VideoFileClip(video_path)
            
            # Apply quality-specific enhancements
            video = video.fx(mp.vfx.colorx, 1.1)
            
            # Ensure proper frame rate
            target_fps = quality_settings.get("fps", self.default_fps)
            if video.fps != target_fps:
                video = video.set_fps(target_fps)
            
            # Write with quality settings
            video.write_videofile(
                output_path,
                codec=quality_settings.get("codec", "libx264"),
                bitrate=quality_settings.get("bitrate", "1000k"),
                audio_codec='aac',
                fps=target_fps,
                verbose=False,
                logger=None
            )
            
            video.close()
            
            return output_path
            
        except Exception as e:
            print(f"Enhanced post-processing failed: {str(e)}")
            return video_path
    
    async def enhance_image_quality(self, image_path: str, output_path: str = None, scale: int = 2) -> str:
        """
        تحسين جودة الصورة باستخدام Real-ESRGAN
        
        Args:
            image_path: مسار الصورة الأصلية
            output_path: مسار الصورة المحسنة (اختياري)
            scale: معامل التكبير (2 أو 4)
        
        Returns:
            مسار الصورة المحسنة
        """
        try:
            if not output_path:
                name, ext = os.path.splitext(os.path.basename(image_path))
                output_path = os.path.join(self.output_dir, f"{name}_enhanced{ext}")
            
            # استخدام خدمة نماذج الذكاء الاصطناعي إذا كانت متاحة
            if self.ai_models_service:
                result = await self.ai_models_service.enhance_image(
                    image_path=image_path,
                    output_path=output_path,
                    scale=scale
                )
                
                if result.get('success', False):
                    return result['output_path']
                else:
                    print(f"Real-ESRGAN failed: {result.get('message', 'Unknown error')}")
                    # العودة إلى تحسين بسيط
                    return await self._simple_image_enhancement(image_path, output_path, scale)
            else:
                # استخدام تحسين بسيط إذا لم تكن خدمة الذكاء الاصطناعي متاحة
                return await self._simple_image_enhancement(image_path, output_path, scale)
                
        except Exception as e:
            print(f"Image enhancement failed: {e}")
            return image_path
    
    async def _simple_image_enhancement(self, image_path: str, output_path: str, scale: int) -> str:
        """تحسين بسيط للصورة باستخدام PIL"""
        try:
            with Image.open(image_path) as img:
                # تكبير الصورة
                new_size = (img.width * scale, img.height * scale)
                enhanced_img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # تحسين الألوان والحدة
                enhancer = ImageEnhance.Sharpness(enhanced_img)
                enhanced_img = enhancer.enhance(1.2)
                
                enhancer = ImageEnhance.Color(enhanced_img)
                enhanced_img = enhancer.enhance(1.1)
                
                enhanced_img.save(output_path, quality=95)
                return output_path
                
        except Exception as e:
            print(f"Simple image enhancement failed: {e}")
            return image_path
    
    async def get_ai_models_status(self) -> Dict[str, Any]:
        """الحصول على حالة نماذج الذكاء الاصطناعي"""
        if self.ai_models_service:
            return self.ai_models_service.get_models_status()
        else:
            return {
                'models_status': {'sadtalker': False, 'wav2lip': False, 'realesrgan': False},
                'ai_models_available': False,
                'message': 'خدمة نماذج الذكاء الاصطناعي غير متاحة'
            }
    
    async def initialize_ai_models(self) -> Dict[str, bool]:
        """تهيئة نماذج الذكاء الاصطناعي"""
        if self.ai_models_service:
            return await self.ai_models_service.initialize_models()
        else:
            return {'sadtalker': False, 'wav2lip': False, 'realesrgan': False}

    async def get_available_quality_presets(self) -> Dict[str, Dict]:
        """Get available video quality presets"""
        return VIDEO_PRESETS
    
    async def get_available_effects(self) -> Dict[str, Dict]:
        """Get available visual effects"""
        return VISUAL_EFFECTS
    
    async def estimate_video_duration(self, audio_path: str) -> float:
        """Estimate video duration based on audio"""
        try:
            return await self._get_audio_duration(audio_path)
        except Exception as e:
            print(f"Duration estimation failed: {str(e)}")
            return 0.0