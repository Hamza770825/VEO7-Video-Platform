"""
Quality Presets API Routes
Provides endpoints for managing video and audio quality presets
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from services.quality_presets_service import (
    QualityPresetsService, 
    QualityPreset, 
    VideoQualitySettings, 
    AudioQualitySettings,
    QualityLevel
)

# Configure logging
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/quality", tags=["quality"])

# Initialize quality presets service (singleton)
quality_service = None

def get_quality_service():
    """Get quality presets service instance"""
    global quality_service
    if quality_service is None:
        quality_service = QualityPresetsService()
    return quality_service

# Pydantic models for requests and responses

class VideoQualitySettingsResponse(BaseModel):
    """Video quality settings response"""
    resolution: str
    fps: int
    bitrate: str
    codec: str
    preset: str = "medium"
    crf: Optional[int] = None
    profile: Optional[str] = None
    level: Optional[str] = None
    denoise: bool = False
    sharpen: bool = False
    stabilization: bool = False
    color_correction: bool = False
    format: str = "mp4"
    two_pass: bool = False
    threads: Optional[int] = None
    hardware_acceleration: bool = False
    gpu_device: Optional[str] = None

class AudioQualitySettingsResponse(BaseModel):
    """Audio quality settings response"""
    sample_rate: int
    bitrate: str
    codec: str
    channels: int = 2
    quality: Optional[str] = None
    compression_level: Optional[int] = None
    normalize: bool = False
    noise_reduction: bool = False
    echo_cancellation: bool = False
    compressor: bool = False
    equalizer: Optional[Dict[str, float]] = None
    format: str = "mp3"

class QualityPresetResponse(BaseModel):
    """Quality preset response"""
    name: str
    description: str
    level: str
    video: VideoQualitySettingsResponse
    audio: AudioQualitySettingsResponse
    use_case: str
    estimated_file_size_factor: float
    processing_time_factor: float

class QualityPresetSummary(BaseModel):
    """Quality preset summary"""
    id: str
    name: str
    description: str
    level: str
    use_case: str
    resolution: str
    video_codec: str
    audio_codec: str
    estimated_file_size_factor: float
    processing_time_factor: float

class CreatePresetRequest(BaseModel):
    """Create custom preset request"""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    level: str = Field(..., pattern="^(ultra|high|medium|low|draft)$")
    video: VideoQualitySettingsResponse
    audio: AudioQualitySettingsResponse
    use_case: str = Field(..., min_length=1, max_length=200)
    estimated_file_size_factor: float = Field(..., gt=0, le=10)
    processing_time_factor: float = Field(..., gt=0, le=10)

class EstimationRequest(BaseModel):
    """File size and processing time estimation request"""
    preset_id: str
    duration_seconds: float = Field(..., gt=0)
    input_file_size_mb: Optional[float] = Field(None, gt=0)
    input_resolution: Optional[str] = None

class EstimationResponse(BaseModel):
    """Estimation response"""
    preset_id: str
    preset_name: str
    duration_seconds: float
    estimated_file_size_mb: float
    estimated_processing_time_seconds: float
    estimated_processing_time_human: str

class RecommendationRequest(BaseModel):
    """Preset recommendation request"""
    use_case: str = Field(..., min_length=1)
    quality_preference: str = Field("medium", pattern="^(ultra|high|medium|low|draft)$")
    duration_seconds: Optional[float] = Field(None, gt=0)
    target_file_size_mb: Optional[float] = Field(None, gt=0)

class RecommendationResponse(BaseModel):
    """Preset recommendation response"""
    recommended_preset_id: str
    preset: QualityPresetResponse
    reasoning: str
    alternatives: List[QualityPresetSummary]

class FFmpegArgsResponse(BaseModel):
    """FFmpeg arguments response"""
    preset_id: str
    video_args: List[str]
    audio_args: List[str]
    complete_command_template: str

# Helper functions

def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hours"

def convert_preset_to_response(preset: QualityPreset) -> QualityPresetResponse:
    """Convert QualityPreset to response model"""
    return QualityPresetResponse(
        name=preset.name,
        description=preset.description,
        level=preset.level.value,
        video=VideoQualitySettingsResponse(**preset.video.__dict__),
        audio=AudioQualitySettingsResponse(**preset.audio.__dict__),
        use_case=preset.use_case,
        estimated_file_size_factor=preset.estimated_file_size_factor,
        processing_time_factor=preset.processing_time_factor
    )

def convert_preset_to_summary(preset_id: str, preset: QualityPreset) -> QualityPresetSummary:
    """Convert QualityPreset to summary model"""
    return QualityPresetSummary(
        id=preset_id,
        name=preset.name,
        description=preset.description,
        level=preset.level.value,
        use_case=preset.use_case,
        resolution=preset.video.resolution,
        video_codec=preset.video.codec,
        audio_codec=preset.audio.codec,
        estimated_file_size_factor=preset.estimated_file_size_factor,
        processing_time_factor=preset.processing_time_factor
    )

# API Endpoints

@router.get("/presets", response_model=List[QualityPresetSummary])
async def get_all_presets(
    level: Optional[str] = Query(None, description="Filter by quality level"),
    service: QualityPresetsService = Depends(get_quality_service)
):
    """
    Get all available quality presets
    
    Returns a list of all quality presets with summary information.
    Optionally filter by quality level.
    """
    try:
        all_presets = service.get_all_presets()
        
        # Filter by level if specified
        if level:
            try:
                quality_level = QualityLevel(level.lower())
                filtered_presets = {
                    pid: preset for pid, preset in all_presets.items()
                    if preset.level == quality_level
                }
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid quality level: {level}")
        else:
            filtered_presets = all_presets
        
        # Convert to summary format
        summaries = [
            convert_preset_to_summary(preset_id, preset)
            for preset_id, preset in filtered_presets.items()
        ]
        
        # Sort by level and name
        level_order = {"ultra": 0, "high": 1, "medium": 2, "low": 3, "draft": 4}
        summaries.sort(key=lambda x: (level_order.get(x.level, 5), x.name))
        
        return summaries
        
    except Exception as e:
        logger.error(f"Failed to get presets: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get presets: {str(e)}")

@router.get("/presets/{preset_id}", response_model=QualityPresetResponse)
async def get_preset(
    preset_id: str,
    service: QualityPresetsService = Depends(get_quality_service)
):
    """
    Get detailed information about a specific quality preset
    
    Returns complete configuration details for the specified preset.
    """
    try:
        preset = service.get_preset(preset_id)
        if not preset:
            raise HTTPException(status_code=404, detail=f"Preset not found: {preset_id}")
        
        return convert_preset_to_response(preset)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get preset {preset_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get preset: {str(e)}")

@router.post("/presets", response_model=QualityPresetResponse)
async def create_custom_preset(
    request: CreatePresetRequest,
    service: QualityPresetsService = Depends(get_quality_service)
):
    """
    Create a custom quality preset
    
    Creates a new custom quality preset with the specified settings.
    Custom presets can be modified and deleted, unlike default presets.
    """
    try:
        # Generate preset ID
        preset_id = f"custom_{request.name.lower().replace(' ', '_')}"
        
        # Check if preset already exists
        if service.get_preset(preset_id):
            raise HTTPException(status_code=409, detail=f"Preset already exists: {preset_id}")
        
        # Convert request to preset object
        video_settings = VideoQualitySettings(**request.video.dict())
        audio_settings = AudioQualitySettings(**request.audio.dict())
        
        preset = QualityPreset(
            name=request.name,
            description=request.description,
            level=QualityLevel(request.level),
            video=video_settings,
            audio=audio_settings,
            use_case=request.use_case,
            estimated_file_size_factor=request.estimated_file_size_factor,
            processing_time_factor=request.processing_time_factor
        )
        
        # Add preset
        success = service.add_custom_preset(preset_id, preset)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save custom preset")
        
        return convert_preset_to_response(preset)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create custom preset: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create preset: {str(e)}")

@router.delete("/presets/{preset_id}")
async def delete_preset(
    preset_id: str,
    service: QualityPresetsService = Depends(get_quality_service)
):
    """
    Delete a custom quality preset
    
    Deletes the specified custom preset. Default presets cannot be deleted.
    """
    try:
        success = service.remove_preset(preset_id)
        if not success:
            # Check if preset exists
            if not service.get_preset(preset_id):
                raise HTTPException(status_code=404, detail=f"Preset not found: {preset_id}")
            else:
                raise HTTPException(status_code=403, detail="Cannot delete default preset")
        
        return {"message": f"Preset {preset_id} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete preset {preset_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete preset: {str(e)}")

@router.post("/estimate", response_model=EstimationResponse)
async def estimate_output(
    request: EstimationRequest,
    service: QualityPresetsService = Depends(get_quality_service)
):
    """
    Estimate file size and processing time
    
    Provides estimates for output file size and processing time
    based on the selected quality preset and input parameters.
    """
    try:
        preset = service.get_preset(request.preset_id)
        if not preset:
            raise HTTPException(status_code=404, detail=f"Preset not found: {request.preset_id}")
        
        # Calculate estimates
        estimated_size = service.estimate_file_size(
            request.preset_id,
            request.duration_seconds,
            request.input_file_size_mb
        )
        
        estimated_time = service.estimate_processing_time(
            request.preset_id,
            request.duration_seconds,
            request.input_resolution
        )
        
        return EstimationResponse(
            preset_id=request.preset_id,
            preset_name=preset.name,
            duration_seconds=request.duration_seconds,
            estimated_file_size_mb=estimated_size,
            estimated_processing_time_seconds=estimated_time,
            estimated_processing_time_human=format_duration(estimated_time)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to estimate output: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to estimate output: {str(e)}")

@router.post("/recommend", response_model=RecommendationResponse)
async def recommend_preset(
    request: RecommendationRequest,
    service: QualityPresetsService = Depends(get_quality_service)
):
    """
    Get preset recommendation
    
    Recommends the best quality preset based on use case,
    quality preference, and optional constraints.
    """
    try:
        # Get recommendation
        recommended_id = service.get_recommended_preset(
            request.use_case,
            request.quality_preference
        )
        
        if not recommended_id:
            raise HTTPException(status_code=404, detail="No suitable preset found")
        
        recommended_preset = service.get_preset(recommended_id)
        if not recommended_preset:
            raise HTTPException(status_code=500, detail="Recommended preset not found")
        
        # Generate reasoning
        reasoning_parts = [
            f"Based on use case '{request.use_case}' and quality preference '{request.quality_preference}'"
        ]
        
        if request.duration_seconds:
            estimated_time = service.estimate_processing_time(recommended_id, request.duration_seconds)
            reasoning_parts.append(f"Estimated processing time: {format_duration(estimated_time)}")
        
        if request.target_file_size_mb and request.duration_seconds:
            estimated_size = service.estimate_file_size(recommended_id, request.duration_seconds)
            if estimated_size > request.target_file_size_mb * 1.5:
                reasoning_parts.append("Note: Estimated file size may exceed target")
        
        reasoning = ". ".join(reasoning_parts)
        
        # Get alternatives (same level and adjacent levels)
        all_presets = service.get_all_presets()
        current_level = recommended_preset.level
        
        # Define level adjacency
        level_order = [QualityLevel.DRAFT, QualityLevel.LOW, QualityLevel.MEDIUM, QualityLevel.HIGH, QualityLevel.ULTRA]
        current_index = level_order.index(current_level)
        
        adjacent_levels = set([current_level])
        if current_index > 0:
            adjacent_levels.add(level_order[current_index - 1])
        if current_index < len(level_order) - 1:
            adjacent_levels.add(level_order[current_index + 1])
        
        alternatives = [
            convert_preset_to_summary(pid, preset)
            for pid, preset in all_presets.items()
            if preset.level in adjacent_levels and pid != recommended_id
        ]
        
        # Sort alternatives by level
        level_order_dict = {"draft": 0, "low": 1, "medium": 2, "high": 3, "ultra": 4}
        alternatives.sort(key=lambda x: (level_order_dict.get(x.level, 5), x.name))
        
        return RecommendationResponse(
            recommended_preset_id=recommended_id,
            preset=convert_preset_to_response(recommended_preset),
            reasoning=reasoning,
            alternatives=alternatives[:5]  # Limit to 5 alternatives
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to recommend preset: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to recommend preset: {str(e)}")

@router.get("/presets/{preset_id}/ffmpeg", response_model=FFmpegArgsResponse)
async def get_ffmpeg_args(
    preset_id: str,
    service: QualityPresetsService = Depends(get_quality_service)
):
    """
    Get FFmpeg arguments for a preset
    
    Returns the FFmpeg command-line arguments needed to encode
    video and audio using the specified quality preset.
    """
    try:
        preset = service.get_preset(preset_id)
        if not preset:
            raise HTTPException(status_code=404, detail=f"Preset not found: {preset_id}")
        
        video_args = service.get_ffmpeg_video_args(preset_id)
        audio_args = service.get_ffmpeg_audio_args(preset_id)
        
        # Create complete command template
        command_parts = ["ffmpeg", "-i", "INPUT_FILE"]
        command_parts.extend(video_args)
        command_parts.extend(audio_args)
        command_parts.append("OUTPUT_FILE")
        
        complete_command = " ".join(command_parts)
        
        return FFmpegArgsResponse(
            preset_id=preset_id,
            video_args=video_args,
            audio_args=audio_args,
            complete_command_template=complete_command
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get FFmpeg args for {preset_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get FFmpeg args: {str(e)}")

@router.get("/levels")
async def get_quality_levels():
    """
    Get available quality levels
    
    Returns information about all available quality levels
    and their characteristics.
    """
    try:
        levels = [
            {
                "id": "ultra",
                "name": "Ultra Quality",
                "description": "Maximum quality for professional use",
                "characteristics": ["Highest file size", "Longest processing time", "Best quality"]
            },
            {
                "id": "high",
                "name": "High Quality",
                "description": "Excellent quality for streaming and sharing",
                "characteristics": ["Large file size", "Moderate processing time", "Excellent quality"]
            },
            {
                "id": "medium",
                "name": "Medium Quality",
                "description": "Balanced quality and file size",
                "characteristics": ["Moderate file size", "Fast processing", "Good quality"]
            },
            {
                "id": "low",
                "name": "Low Quality",
                "description": "Small file size for mobile and low bandwidth",
                "characteristics": ["Small file size", "Very fast processing", "Acceptable quality"]
            },
            {
                "id": "draft",
                "name": "Draft Quality",
                "description": "Fast processing for previews",
                "characteristics": ["Minimal file size", "Fastest processing", "Preview quality"]
            }
        ]
        
        return {"levels": levels}
        
    except Exception as e:
        logger.error(f"Failed to get quality levels: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get quality levels: {str(e)}")

@router.get("/health")
async def quality_health_check():
    """
    Quality service health check
    
    Returns the health status of the quality presets service.
    """
    try:
        service = get_quality_service()
        all_presets = service.get_all_presets()
        
        # Check if default presets are available
        default_presets = ["ultra_4k", "high_1080p", "medium_720p", "low_480p", "draft_360p"]
        missing_defaults = [p for p in default_presets if p not in all_presets]
        
        is_healthy = len(missing_defaults) == 0
        
        return {
            "status": "healthy" if is_healthy else "degraded",
            "total_presets": len(all_presets),
            "default_presets_available": len(default_presets) - len(missing_defaults),
            "custom_presets": len(all_presets) - (len(default_presets) - len(missing_defaults)),
            "missing_defaults": missing_defaults,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Quality health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }