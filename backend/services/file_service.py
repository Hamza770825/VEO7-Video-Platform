"""
File Service for VEO7 Video Platform
Handles file uploads, validation, and storage
"""

import os
import uuid
import aiofiles
import mimetypes
from typing import Optional, Tuple, List
from fastapi import UploadFile, HTTPException
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class FileService:
    def __init__(self):
        """Initialize file service"""
        self.temp_dir = "temp_uploads"
        self.output_dir = "output_videos"
        self.models_dir = "models"
        
        # Create directories if they don't exist
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)
        
        # File size limits (in bytes)
        self.max_image_size = 10 * 1024 * 1024  # 10MB
        self.max_audio_size = 50 * 1024 * 1024  # 50MB
        self.max_video_size = 100 * 1024 * 1024  # 100MB
        
        # Allowed file types
        self.allowed_image_types = {
            'image/jpeg', 'image/jpg', 'image/png', 'image/webp'
        }
        self.allowed_audio_types = {
            'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/ogg', 'audio/m4a'
        }
        self.allowed_video_types = {
            'video/mp4', 'video/avi', 'video/mov', 'video/webm'
        }
    
    async def health_check(self) -> str:
        """Check file service health"""
        try:
            # Check if directories exist and are writable
            test_file = os.path.join(self.temp_dir, "health_check.txt")
            async with aiofiles.open(test_file, 'w') as f:
                await f.write("health check")
            
            if os.path.exists(test_file):
                os.remove(test_file)
                return "healthy"
            else:
                return "unhealthy"
        except Exception as e:
            logger.error(f"File service health check failed: {e}")
            return "unhealthy"
    
    def _validate_file_type(self, file: UploadFile, allowed_types: set) -> bool:
        """Validate file type"""
        if file.content_type in allowed_types:
            return True
        
        # Also check by file extension as backup
        if file.filename:
            mime_type, _ = mimetypes.guess_type(file.filename)
            return mime_type in allowed_types
        
        return False
    
    def _validate_file_size(self, file: UploadFile, max_size: int) -> bool:
        """Validate file size"""
        if hasattr(file, 'size') and file.size:
            return file.size <= max_size
        return True  # If size is unknown, allow it (will be checked during upload)
    
    async def save_uploaded_file(self, file: UploadFile, file_type: str) -> str:
        """Save uploaded file and return file path"""
        try:
            # Validate file type
            if file_type == 'image':
                if not self._validate_file_type(file, self.allowed_image_types):
                    raise HTTPException(status_code=400, detail="Invalid image file type")
                max_size = self.max_image_size
            elif file_type == 'audio':
                if not self._validate_file_type(file, self.allowed_audio_types):
                    raise HTTPException(status_code=400, detail="Invalid audio file type")
                max_size = self.max_audio_size
            elif file_type == 'video':
                if not self._validate_file_type(file, self.allowed_video_types):
                    raise HTTPException(status_code=400, detail="Invalid video file type")
                max_size = self.max_video_size
            else:
                raise HTTPException(status_code=400, detail="Invalid file type")
            
            # Validate file size
            if not self._validate_file_size(file, max_size):
                raise HTTPException(status_code=400, detail=f"File too large. Maximum size: {max_size / (1024*1024):.1f}MB")
            
            # Generate unique filename
            file_extension = ""
            if file.filename:
                file_extension = os.path.splitext(file.filename)[1].lower()
            
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(self.temp_dir, unique_filename)
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                
                # Check actual file size
                if len(content) > max_size:
                    raise HTTPException(status_code=400, detail=f"File too large. Maximum size: {max_size / (1024*1024):.1f}MB")
                
                await f.write(content)
            
            # Additional validation for images
            if file_type == 'image':
                await self._validate_image(file_path)
            
            logger.info(f"Saved {file_type} file: {file_path}")
            return file_path
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error saving uploaded file: {e}")
            raise HTTPException(status_code=500, detail="Failed to save file")
    
    async def _validate_image(self, file_path: str):
        """Validate image file"""
        try:
            with Image.open(file_path) as img:
                # Check image dimensions
                width, height = img.size
                if width < 64 or height < 64:
                    os.remove(file_path)
                    raise HTTPException(status_code=400, detail="Image too small. Minimum size: 64x64 pixels")
                
                if width > 4096 or height > 4096:
                    os.remove(file_path)
                    raise HTTPException(status_code=400, detail="Image too large. Maximum size: 4096x4096 pixels")
                
                # Verify it's a valid image
                img.verify()
                
        except HTTPException:
            raise
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            logger.error(f"Image validation failed: {e}")
            raise HTTPException(status_code=400, detail="Invalid image file")
    
    async def save_generated_video(self, video_path: str, user_id: str, project_id: str) -> str:
        """Save generated video to output directory"""
        try:
            # Generate unique filename for output
            video_filename = f"{user_id}_{project_id}_{uuid.uuid4()}.mp4"
            output_path = os.path.join(self.output_dir, video_filename)
            
            # Copy video to output directory
            async with aiofiles.open(video_path, 'rb') as src:
                async with aiofiles.open(output_path, 'wb') as dst:
                    content = await src.read()
                    await dst.write(content)
            
            logger.info(f"Saved generated video: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error saving generated video: {e}")
            raise
    
    def cleanup_temp_files(self, file_paths: List[str]):
        """Clean up temporary files"""
        try:
            for file_path in file_paths:
                if os.path.exists(file_path) and file_path.startswith(self.temp_dir):
                    os.remove(file_path)
                    logger.info(f"Cleaned up temp file: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {e}")
    
    def get_file_url(self, file_path: str) -> str:
        """Get URL for accessing file"""
        try:
            # For output videos, return the static file URL
            if file_path.startswith(self.output_dir):
                filename = os.path.basename(file_path)
                return f"/static/videos/{filename}"
            
            return file_path
            
        except Exception as e:
            logger.error(f"Error getting file URL: {e}")
            return file_path
    
    def get_file_info(self, file_path: str) -> dict:
        """Get file information"""
        try:
            if not os.path.exists(file_path):
                return {"exists": False}
            
            stat = os.stat(file_path)
            mime_type, _ = mimetypes.guess_type(file_path)
            
            return {
                "exists": True,
                "size": stat.st_size,
                "mime_type": mime_type,
                "created_at": stat.st_ctime,
                "modified_at": stat.st_mtime
            }
            
        except Exception as e:
            logger.error(f"Error getting file info: {e}")
            return {"exists": False, "error": str(e)}
    
    async def create_thumbnail(self, image_path: str, size: Tuple[int, int] = (200, 200)) -> str:
        """Create thumbnail for image"""
        try:
            with Image.open(image_path) as img:
                # Create thumbnail
                img.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Generate thumbnail filename
                base_name = os.path.splitext(os.path.basename(image_path))[0]
                thumbnail_filename = f"{base_name}_thumb.jpg"
                thumbnail_path = os.path.join(self.temp_dir, thumbnail_filename)
                
                # Save thumbnail
                img.save(thumbnail_path, "JPEG", quality=85)
                
                logger.info(f"Created thumbnail: {thumbnail_path}")
                return thumbnail_path
                
        except Exception as e:
            logger.error(f"Error creating thumbnail: {e}")
            raise
    
    def get_storage_stats(self) -> dict:
        """Get storage statistics"""
        try:
            stats = {
                "temp_files": 0,
                "temp_size": 0,
                "output_files": 0,
                "output_size": 0
            }
            
            # Count temp files
            if os.path.exists(self.temp_dir):
                for file in os.listdir(self.temp_dir):
                    file_path = os.path.join(self.temp_dir, file)
                    if os.path.isfile(file_path):
                        stats["temp_files"] += 1
                        stats["temp_size"] += os.path.getsize(file_path)
            
            # Count output files
            if os.path.exists(self.output_dir):
                for file in os.listdir(self.output_dir):
                    file_path = os.path.join(self.output_dir, file)
                    if os.path.isfile(file_path):
                        stats["output_files"] += 1
                        stats["output_size"] += os.path.getsize(file_path)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting storage stats: {e}")
            return {"error": str(e)}