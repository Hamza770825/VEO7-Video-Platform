"""
Video Generation Service for VEO7 Video Platform
Handles basic video generation from images and audio
"""

import os
import uuid
import subprocess
import logging
from typing import Optional, Dict, Any
from PIL import Image
from gtts import gTTS
import tempfile
import shutil

logger = logging.getLogger(__name__)

class VideoGenerationService:
    def __init__(self):
        """Initialize video generation service"""
        self.temp_dir = "temp_uploads"
        self.output_dir = "output_videos"
        self.models_dir = "models"
        
        # Create directories if they don't exist
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)
        
        logger.info("Video Generation Service initialized")
    
    async def health_check(self) -> str:
        """Check video generation service health"""
        try:
            # Check if ffmpeg is available
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return "healthy"
            else:
                return "unhealthy - ffmpeg not available"
        except Exception as e:
            logger.error(f"Video generation health check failed: {e}")
            return "unhealthy"
    
    def _check_model_availability(self) -> Dict[str, bool]:
        """Check which AI models are available"""
        try:
            models = {
                "sadtalker": False,
                "wav2lip": False,
                "basic_ffmpeg": True  # Always available if ffmpeg is installed
            }
            
            # For now, we'll use basic video generation
            # AI models can be added later when properly configured
            
            return models
            
        except Exception as e:
            logger.error(f"Error checking model availability: {e}")
            return {"basic_ffmpeg": True}
    
    async def generate_from_image_audio(
        self, 
        image_path: str, 
        audio_path: str, 
        output_path: str,
        method: str = "basic"
    ) -> bool:
        """Generate video from image and audio"""
        try:
            # For now, we'll use basic video generation
            # AI models can be added later
            return await self._generate_basic_video(image_path, audio_path, output_path)
                
        except Exception as e:
            logger.error(f"Error generating video from image and audio: {e}")
            return False
    
    async def generate_from_text_audio(
        self, 
        text: str, 
        audio_path: str, 
        output_path: str
    ) -> bool:
        """Generate video from text and audio"""
        try:
            # Create a simple text image
            temp_image = await self._create_text_image(text)
            if temp_image:
                result = await self._generate_basic_video(temp_image, audio_path, output_path)
                # Clean up temp image
                if os.path.exists(temp_image):
                    os.remove(temp_image)
                return result
            return False
                
        except Exception as e:
            logger.error(f"Error generating video from text and audio: {e}")
            return False
    
    async def generate_from_image_text(
        self, 
        image_path: str, 
        text: str, 
        output_path: str,
        language: str = "en"
    ) -> bool:
        """Generate video from image and text (convert text to speech first)"""
        try:
            # Convert text to speech
            temp_audio = await self._text_to_speech(text, language)
            if temp_audio:
                result = await self._generate_basic_video(image_path, temp_audio, output_path)
                # Clean up temp audio
                if os.path.exists(temp_audio):
                    os.remove(temp_audio)
                return result
            return False
                
        except Exception as e:
            logger.error(f"Error generating video from image and text: {e}")
            return False
    
    async def _generate_basic_video(self, image_path: str, audio_path: str, output_path: str) -> bool:
        """Create basic video using FFmpeg"""
        try:
            # Get audio duration
            duration = await self._get_audio_duration(audio_path)
            if duration <= 0:
                duration = 5  # Default 5 seconds
            
            # FFmpeg command to create video from image and audio
            cmd = [
                'ffmpeg', '-y',  # -y to overwrite output file
                '-loop', '1',  # Loop the image
                '-i', image_path,  # Input image
                '-i', audio_path,  # Input audio
                '-c:v', 'libx264',  # Video codec
                '-c:a', 'aac',  # Audio codec
                '-t', str(duration),  # Duration
                '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
                '-shortest',  # End when shortest input ends
                output_path
            ]
            
            # Run FFmpeg
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info(f"Successfully created basic video: {output_path}")
                return True
            else:
                logger.error(f"FFmpeg error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("FFmpeg timeout")
            return False
        except Exception as e:
            logger.error(f"Error creating basic video: {e}")
            return False
    
    async def _create_text_image(self, text: str, width: int = 800, height: int = 600) -> Optional[str]:
        """Create an image with text"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create image
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Try to use a font, fallback to default if not available
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position (center)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            # Draw text
            draw.text((x, y), text, fill='black', font=font)
            
            # Save image
            temp_path = os.path.join(self.temp_dir, f"text_{uuid.uuid4()}.png")
            img.save(temp_path)
            
            logger.info(f"Created text image: {temp_path}")
            return temp_path
            
        except Exception as e:
            logger.error(f"Error creating text image: {e}")
            return None
    
    async def _text_to_speech(self, text: str, language: str = "en") -> Optional[str]:
        """Convert text to speech using gTTS"""
        try:
            # Create TTS
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Save to temp file
            temp_path = os.path.join(self.temp_dir, f"tts_{uuid.uuid4()}.mp3")
            tts.save(temp_path)
            
            logger.info(f"Created TTS audio: {temp_path}")
            return temp_path
            
        except Exception as e:
            logger.error(f"Error creating TTS: {e}")
            # Create silent audio as fallback
            return await self._create_silent_audio(5)  # 5 seconds
    
    async def _create_silent_audio(self, duration: int = 5) -> Optional[str]:
        """Create silent audio file"""
        try:
            temp_path = os.path.join(self.temp_dir, f"silent_{uuid.uuid4()}.mp3")
            
            # Create silent audio using FFmpeg
            cmd = [
                'ffmpeg', '-y',
                '-f', 'lavfi',
                '-i', f'anullsrc=channel_layout=stereo:sample_rate=44100',
                '-t', str(duration),
                '-c:a', 'mp3',
                temp_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info(f"Created silent audio: {temp_path}")
                return temp_path
            else:
                logger.error(f"Error creating silent audio: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating silent audio: {e}")
            return None
    
    async def _get_audio_duration(self, audio_path: str) -> float:
        """Get audio duration in seconds"""
        try:
            cmd = [
                'ffprobe', '-v', 'quiet',
                '-show_entries', 'format=duration',
                '-of', 'csv=p=0',
                audio_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return duration
            else:
                logger.warning(f"Could not get audio duration: {result.stderr}")
                return 5.0  # Default 5 seconds
                
        except Exception as e:
            logger.error(f"Error getting audio duration: {e}")
            return 5.0  # Default 5 seconds
    
    def cleanup_temp_files(self, file_paths: list):
        """Clean up temporary files"""
        try:
            for file_path in file_paths:
                if os.path.exists(file_path) and file_path.startswith(self.temp_dir):
                    os.remove(file_path)
                    logger.info(f"Cleaned up temp file: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {e}")
    
    def get_generation_stats(self) -> dict:
        """Get video generation statistics"""
        try:
            stats = {
                "temp_files": 0,
                "output_files": 0,
                "models_available": self._check_model_availability()
            }
            
            # Count files
            if os.path.exists(self.temp_dir):
                stats["temp_files"] = len([f for f in os.listdir(self.temp_dir) if os.path.isfile(os.path.join(self.temp_dir, f))])
            
            if os.path.exists(self.output_dir):
                stats["output_files"] = len([f for f in os.listdir(self.output_dir) if os.path.isfile(os.path.join(self.output_dir, f))])
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting generation stats: {e}")
            return {"error": str(e)}