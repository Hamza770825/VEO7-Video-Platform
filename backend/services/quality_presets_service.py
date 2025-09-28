"""
Quality Presets Service
Provides predefined quality settings for video and audio processing
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import json
import os
from pathlib import Path

class QualityLevel(Enum):
    """Quality levels"""
    ULTRA = "ultra"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    DRAFT = "draft"

class VideoCodec(Enum):
    """Video codecs"""
    H264 = "h264"
    H265 = "h265"
    VP9 = "vp9"
    AV1 = "av1"

class AudioCodec(Enum):
    """Audio codecs"""
    AAC = "aac"
    MP3 = "mp3"
    OPUS = "opus"
    FLAC = "flac"

@dataclass
class VideoQualitySettings:
    """Video quality settings"""
    # Basic settings
    resolution: str  # e.g., "1920x1080", "1280x720"
    fps: int
    bitrate: str  # e.g., "5000k", "2000k"
    codec: str
    
    # Advanced settings
    preset: str = "medium"  # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
    crf: Optional[int] = None  # Constant Rate Factor (0-51, lower = better quality)
    profile: Optional[str] = None  # baseline, main, high
    level: Optional[str] = None  # 3.0, 3.1, 4.0, 4.1, etc.
    
    # Filters and effects
    denoise: bool = False
    sharpen: bool = False
    stabilization: bool = False
    color_correction: bool = False
    
    # Output settings
    format: str = "mp4"
    two_pass: bool = False
    
    # Performance settings
    threads: Optional[int] = None
    hardware_acceleration: bool = False
    gpu_device: Optional[str] = None

@dataclass
class AudioQualitySettings:
    """Audio quality settings"""
    # Basic settings
    sample_rate: int  # 44100, 48000, 96000
    bitrate: str  # "128k", "192k", "320k"
    codec: str
    channels: int = 2  # 1 (mono), 2 (stereo), 6 (5.1), 8 (7.1)
    
    # Advanced settings
    quality: Optional[str] = None  # For VBR encoding
    compression_level: Optional[int] = None
    
    # Audio processing
    normalize: bool = False
    noise_reduction: bool = False
    echo_cancellation: bool = False
    compressor: bool = False
    equalizer: Optional[Dict[str, float]] = None
    
    # Output settings
    format: str = "mp3"

@dataclass
class QualityPreset:
    """Complete quality preset"""
    name: str
    description: str
    level: QualityLevel
    video: VideoQualitySettings
    audio: AudioQualitySettings
    use_case: str
    estimated_file_size_factor: float  # Multiplier for file size estimation
    processing_time_factor: float  # Multiplier for processing time estimation

class QualityPresetsService:
    """Service for managing quality presets"""
    
    def __init__(self, presets_file: Optional[str] = None):
        """Initialize quality presets service"""
        self.presets_file = presets_file or "data/quality_presets.json"
        self.presets: Dict[str, QualityPreset] = {}
        self._load_default_presets()
        self._load_custom_presets()
    
    def _load_default_presets(self):
        """Load default quality presets"""
        
        # Ultra Quality - Best possible quality
        self.presets["ultra_4k"] = QualityPreset(
            name="Ultra 4K",
            description="Maximum quality 4K video with lossless audio",
            level=QualityLevel.ULTRA,
            video=VideoQualitySettings(
                resolution="3840x2160",
                fps=60,
                bitrate="25000k",
                codec=VideoCodec.H265.value,
                preset="slow",
                crf=18,
                profile="main",
                denoise=True,
                sharpen=True,
                stabilization=True,
                color_correction=True,
                two_pass=True,
                hardware_acceleration=True
            ),
            audio=AudioQualitySettings(
                sample_rate=96000,
                bitrate="320k",
                codec=AudioCodec.FLAC.value,
                channels=2,
                normalize=True,
                noise_reduction=True,
                compressor=True
            ),
            use_case="Professional video production, archival",
            estimated_file_size_factor=8.0,
            processing_time_factor=4.0
        )
        
        # High Quality - Excellent quality for most uses
        self.presets["high_1080p"] = QualityPreset(
            name="High 1080p",
            description="High quality 1080p video for streaming and sharing",
            level=QualityLevel.HIGH,
            video=VideoQualitySettings(
                resolution="1920x1080",
                fps=30,
                bitrate="8000k",
                codec=VideoCodec.H264.value,
                preset="medium",
                crf=20,
                profile="high",
                denoise=True,
                stabilization=True,
                color_correction=True,
                hardware_acceleration=True
            ),
            audio=AudioQualitySettings(
                sample_rate=48000,
                bitrate="192k",
                codec=AudioCodec.AAC.value,
                channels=2,
                normalize=True,
                noise_reduction=True
            ),
            use_case="YouTube, Vimeo, professional sharing",
            estimated_file_size_factor=3.0,
            processing_time_factor=2.0
        )
        
        # Medium Quality - Balanced quality and file size
        self.presets["medium_720p"] = QualityPreset(
            name="Medium 720p",
            description="Balanced quality and file size for web streaming",
            level=QualityLevel.MEDIUM,
            video=VideoQualitySettings(
                resolution="1280x720",
                fps=30,
                bitrate="3000k",
                codec=VideoCodec.H264.value,
                preset="fast",
                crf=23,
                profile="main",
                denoise=True,
                hardware_acceleration=True
            ),
            audio=AudioQualitySettings(
                sample_rate=44100,
                bitrate="128k",
                codec=AudioCodec.AAC.value,
                channels=2,
                normalize=True
            ),
            use_case="Web streaming, social media",
            estimated_file_size_factor=1.5,
            processing_time_factor=1.0
        )
        
        # Low Quality - Small file size
        self.presets["low_480p"] = QualityPreset(
            name="Low 480p",
            description="Small file size for mobile and low bandwidth",
            level=QualityLevel.LOW,
            video=VideoQualitySettings(
                resolution="854x480",
                fps=24,
                bitrate="1000k",
                codec=VideoCodec.H264.value,
                preset="faster",
                crf=28,
                profile="baseline",
                hardware_acceleration=True
            ),
            audio=AudioQualitySettings(
                sample_rate=44100,
                bitrate="96k",
                codec=AudioCodec.AAC.value,
                channels=2
            ),
            use_case="Mobile viewing, low bandwidth",
            estimated_file_size_factor=0.5,
            processing_time_factor=0.5
        )
        
        # Draft Quality - Fast processing for previews
        self.presets["draft_360p"] = QualityPreset(
            name="Draft 360p",
            description="Fast processing for previews and drafts",
            level=QualityLevel.DRAFT,
            video=VideoQualitySettings(
                resolution="640x360",
                fps=24,
                bitrate="500k",
                codec=VideoCodec.H264.value,
                preset="ultrafast",
                crf=32,
                profile="baseline",
                hardware_acceleration=True
            ),
            audio=AudioQualitySettings(
                sample_rate=22050,
                bitrate="64k",
                codec=AudioCodec.MP3.value,
                channels=1
            ),
            use_case="Quick previews, drafts",
            estimated_file_size_factor=0.2,
            processing_time_factor=0.2
        )
        
        # Audio-only presets
        self.presets["audio_high"] = QualityPreset(
            name="Audio High Quality",
            description="High quality audio for music and podcasts",
            level=QualityLevel.HIGH,
            video=VideoQualitySettings(
                resolution="1x1",  # Minimal video
                fps=1,
                bitrate="1k",
                codec=VideoCodec.H264.value,
                preset="ultrafast"
            ),
            audio=AudioQualitySettings(
                sample_rate=48000,
                bitrate="320k",
                codec=AudioCodec.FLAC.value,
                channels=2,
                normalize=True,
                noise_reduction=True,
                compressor=True
            ),
            use_case="Music, high-quality audio content",
            estimated_file_size_factor=0.8,
            processing_time_factor=0.3
        )
        
        self.presets["audio_medium"] = QualityPreset(
            name="Audio Medium Quality",
            description="Standard quality audio for podcasts and voice",
            level=QualityLevel.MEDIUM,
            video=VideoQualitySettings(
                resolution="1x1",
                fps=1,
                bitrate="1k",
                codec=VideoCodec.H264.value,
                preset="ultrafast"
            ),
            audio=AudioQualitySettings(
                sample_rate=44100,
                bitrate="128k",
                codec=AudioCodec.MP3.value,
                channels=2,
                normalize=True,
                noise_reduction=True
            ),
            use_case="Podcasts, voice content",
            estimated_file_size_factor=0.3,
            processing_time_factor=0.2
        )
    
    def _load_custom_presets(self):
        """Load custom presets from file"""
        try:
            if os.path.exists(self.presets_file):
                with open(self.presets_file, 'r', encoding='utf-8') as f:
                    custom_data = json.load(f)
                
                for preset_id, preset_data in custom_data.items():
                    # Convert dict back to QualityPreset
                    video_settings = VideoQualitySettings(**preset_data['video'])
                    audio_settings = AudioQualitySettings(**preset_data['audio'])
                    
                    preset = QualityPreset(
                        name=preset_data['name'],
                        description=preset_data['description'],
                        level=QualityLevel(preset_data['level']),
                        video=video_settings,
                        audio=audio_settings,
                        use_case=preset_data['use_case'],
                        estimated_file_size_factor=preset_data['estimated_file_size_factor'],
                        processing_time_factor=preset_data['processing_time_factor']
                    )
                    
                    self.presets[preset_id] = preset
                    
        except Exception as e:
            print(f"Warning: Failed to load custom presets: {e}")
    
    def save_custom_presets(self):
        """Save custom presets to file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.presets_file), exist_ok=True)
            
            # Filter out default presets (only save custom ones)
            default_preset_ids = {
                "ultra_4k", "high_1080p", "medium_720p", "low_480p", 
                "draft_360p", "audio_high", "audio_medium"
            }
            
            custom_presets = {
                preset_id: asdict(preset) 
                for preset_id, preset in self.presets.items() 
                if preset_id not in default_preset_ids
            }
            
            # Convert enum values to strings
            for preset_data in custom_presets.values():
                preset_data['level'] = preset_data['level'].value if hasattr(preset_data['level'], 'value') else preset_data['level']
            
            with open(self.presets_file, 'w', encoding='utf-8') as f:
                json.dump(custom_presets, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Warning: Failed to save custom presets: {e}")
    
    def get_preset(self, preset_id: str) -> Optional[QualityPreset]:
        """Get a quality preset by ID"""
        return self.presets.get(preset_id)
    
    def get_presets_by_level(self, level: QualityLevel) -> List[QualityPreset]:
        """Get all presets for a specific quality level"""
        return [preset for preset in self.presets.values() if preset.level == level]
    
    def get_all_presets(self) -> Dict[str, QualityPreset]:
        """Get all available presets"""
        return self.presets.copy()
    
    def get_preset_names(self) -> List[str]:
        """Get list of all preset names"""
        return list(self.presets.keys())
    
    def add_custom_preset(self, preset_id: str, preset: QualityPreset) -> bool:
        """Add a custom quality preset"""
        try:
            self.presets[preset_id] = preset
            self.save_custom_presets()
            return True
        except Exception as e:
            print(f"Failed to add custom preset: {e}")
            return False
    
    def remove_preset(self, preset_id: str) -> bool:
        """Remove a custom preset (cannot remove default presets)"""
        default_preset_ids = {
            "ultra_4k", "high_1080p", "medium_720p", "low_480p", 
            "draft_360p", "audio_high", "audio_medium"
        }
        
        if preset_id in default_preset_ids:
            return False  # Cannot remove default presets
        
        if preset_id in self.presets:
            del self.presets[preset_id]
            self.save_custom_presets()
            return True
        
        return False
    
    def estimate_file_size(self, preset_id: str, duration_seconds: float, input_file_size_mb: Optional[float] = None) -> float:
        """Estimate output file size in MB"""
        preset = self.get_preset(preset_id)
        if not preset:
            return 0.0
        
        # Base estimation using bitrate
        video_bitrate_kbps = int(preset.video.bitrate.replace('k', ''))
        audio_bitrate_kbps = int(preset.audio.bitrate.replace('k', ''))
        total_bitrate_kbps = video_bitrate_kbps + audio_bitrate_kbps
        
        # Calculate size based on bitrate
        estimated_size_mb = (total_bitrate_kbps * duration_seconds) / (8 * 1024)  # Convert to MB
        
        # Apply preset factor
        estimated_size_mb *= preset.estimated_file_size_factor
        
        # If input file size is provided, use it as a reference
        if input_file_size_mb:
            # Blend estimation with input size reference
            size_ratio = estimated_size_mb / max(input_file_size_mb, 1)
            if size_ratio > 2:  # If estimation is much larger, cap it
                estimated_size_mb = input_file_size_mb * 2
        
        return round(estimated_size_mb, 2)
    
    def estimate_processing_time(self, preset_id: str, duration_seconds: float, input_resolution: Optional[str] = None) -> float:
        """Estimate processing time in seconds"""
        preset = self.get_preset(preset_id)
        if not preset:
            return 0.0
        
        # Base processing time (rough estimate: 1x duration for medium quality)
        base_time = duration_seconds
        
        # Apply preset factor
        estimated_time = base_time * preset.processing_time_factor
        
        # Adjust for resolution difference
        if input_resolution and preset.video.resolution:
            try:
                input_w, input_h = map(int, input_resolution.split('x'))
                output_w, output_h = map(int, preset.video.resolution.split('x'))
                
                input_pixels = input_w * input_h
                output_pixels = output_w * output_h
                
                # Adjust time based on pixel count ratio
                pixel_ratio = output_pixels / max(input_pixels, 1)
                estimated_time *= (0.5 + 0.5 * pixel_ratio)  # Smooth scaling
                
            except ValueError:
                pass  # Use base estimation if resolution parsing fails
        
        return round(estimated_time, 1)
    
    def get_ffmpeg_video_args(self, preset_id: str) -> List[str]:
        """Get FFmpeg arguments for video encoding"""
        preset = self.get_preset(preset_id)
        if not preset:
            return []
        
        args = []
        video = preset.video
        
        # Codec
        args.extend(['-c:v', video.codec])
        
        # Resolution
        if video.resolution != "1x1":  # Skip for audio-only
            args.extend(['-s', video.resolution])
        
        # Frame rate
        args.extend(['-r', str(video.fps)])
        
        # Bitrate
        args.extend(['-b:v', video.bitrate])
        
        # Preset
        if video.codec in ['h264', 'h265']:
            args.extend(['-preset', video.preset])
        
        # CRF (Constant Rate Factor)
        if video.crf is not None:
            args.extend(['-crf', str(video.crf)])
        
        # Profile
        if video.profile:
            args.extend(['-profile:v', video.profile])
        
        # Level
        if video.level:
            args.extend(['-level', video.level])
        
        # Filters
        filters = []
        if video.denoise:
            filters.append('hqdn3d')
        if video.sharpen:
            filters.append('unsharp=5:5:1.0:5:5:0.0')
        if video.stabilization:
            filters.append('deshake')
        
        if filters:
            args.extend(['-vf', ','.join(filters)])
        
        # Two-pass encoding
        if video.two_pass:
            args.extend(['-pass', '1'])
        
        # Hardware acceleration
        if video.hardware_acceleration:
            if video.gpu_device:
                args.extend(['-hwaccel_device', video.gpu_device])
            args.extend(['-hwaccel', 'auto'])
        
        # Threads
        if video.threads:
            args.extend(['-threads', str(video.threads)])
        
        return args
    
    def get_ffmpeg_audio_args(self, preset_id: str) -> List[str]:
        """Get FFmpeg arguments for audio encoding"""
        preset = self.get_preset(preset_id)
        if not preset:
            return []
        
        args = []
        audio = preset.audio
        
        # Codec
        args.extend(['-c:a', audio.codec])
        
        # Sample rate
        args.extend(['-ar', str(audio.sample_rate)])
        
        # Bitrate
        args.extend(['-b:a', audio.bitrate])
        
        # Channels
        args.extend(['-ac', str(audio.channels)])
        
        # Quality (for VBR)
        if audio.quality:
            args.extend(['-q:a', audio.quality])
        
        # Audio filters
        filters = []
        if audio.normalize:
            filters.append('loudnorm')
        if audio.noise_reduction:
            filters.append('afftdn')
        if audio.compressor:
            filters.append('acompressor')
        
        if filters:
            args.extend(['-af', ','.join(filters)])
        
        return args
    
    def get_recommended_preset(self, use_case: str, quality_preference: str = "medium") -> Optional[str]:
        """Get recommended preset based on use case and quality preference"""
        use_case_lower = use_case.lower()
        quality_lower = quality_preference.lower()
        
        # Define recommendations
        recommendations = {
            "youtube": {
                "high": "high_1080p",
                "medium": "medium_720p",
                "low": "low_480p"
            },
            "social_media": {
                "high": "medium_720p",
                "medium": "low_480p",
                "low": "draft_360p"
            },
            "professional": {
                "high": "ultra_4k",
                "medium": "high_1080p",
                "low": "medium_720p"
            },
            "mobile": {
                "high": "medium_720p",
                "medium": "low_480p",
                "low": "draft_360p"
            },
            "podcast": {
                "high": "audio_high",
                "medium": "audio_medium",
                "low": "audio_medium"
            },
            "preview": {
                "high": "medium_720p",
                "medium": "low_480p",
                "low": "draft_360p"
            }
        }
        
        # Find matching use case
        for case, presets in recommendations.items():
            if case in use_case_lower:
                return presets.get(quality_lower, presets.get("medium"))
        
        # Default recommendations
        default_presets = {
            "high": "high_1080p",
            "medium": "medium_720p",
            "low": "low_480p",
            "ultra": "ultra_4k",
            "draft": "draft_360p"
        }
        
        return default_presets.get(quality_lower, "medium_720p")