"""
Batch Processing API Routes
Handles batch processing endpoints for multiple videos, audio, and translations
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends, Query
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from services.batch_service import BatchProcessingService, JobPriority, JobStatus

# Configure logging
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/batch", tags=["batch"])

# Initialize batch service (singleton)
batch_service = None

def get_batch_service():
    """Get batch service instance"""
    global batch_service
    if batch_service is None:
        batch_service = BatchProcessingService()
    return batch_service

# Pydantic models for request/response

class VideoJobRequest(BaseModel):
    """Single video job request"""
    image_path: str = Field(..., description="Path to input image")
    audio_path: Optional[str] = Field(None, description="Path to input audio")
    output_path: str = Field(..., description="Path for output video")
    duration: float = Field(5.0, ge=1.0, le=60.0, description="Video duration in seconds")
    quality: str = Field("medium", description="Video quality (fast/medium/high)")
    effects: List[str] = Field(default_factory=list, description="Visual effects to apply")

class AudioJobRequest(BaseModel):
    """Single audio job request"""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to convert to speech")
    output_path: str = Field(..., description="Path for output audio")
    voice: str = Field("female", description="Voice type (male/female)")
    quality: str = Field("medium", description="Audio quality (fast/medium/high)")
    language: str = Field("en", description="Language code")

class TranslationJobRequest(BaseModel):
    """Single translation job request"""
    text: str = Field(..., min_length=1, max_length=10000, description="Text to translate")
    source_lang: Optional[str] = Field(None, description="Source language (auto-detect if None)")
    target_lang: str = Field(..., description="Target language code")
    quality: str = Field("medium", description="Translation quality (fast/medium/high)")

class BatchVideoRequest(BaseModel):
    """Batch video processing request"""
    jobs: List[VideoJobRequest] = Field(..., min_items=1, max_items=50, description="Video jobs")
    batch_name: Optional[str] = Field(None, description="Optional batch name")
    priority: str = Field("medium", description="Batch priority (low/medium/high/urgent)")

class BatchAudioRequest(BaseModel):
    """Batch audio processing request"""
    jobs: List[AudioJobRequest] = Field(..., min_items=1, max_items=100, description="Audio jobs")
    batch_name: Optional[str] = Field(None, description="Optional batch name")
    priority: str = Field("medium", description="Batch priority (low/medium/high/urgent)")

class BatchTranslationRequest(BaseModel):
    """Batch translation processing request"""
    jobs: List[TranslationJobRequest] = Field(..., min_items=1, max_items=200, description="Translation jobs")
    batch_name: Optional[str] = Field(None, description="Optional batch name")
    priority: str = Field("medium", description="Batch priority (low/medium/high/urgent)")

class BatchResponse(BaseModel):
    """Batch creation response"""
    batch_id: str = Field(..., description="Unique batch identifier")
    message: str = Field(..., description="Success message")
    total_jobs: int = Field(..., description="Total number of jobs in batch")
    estimated_duration: Optional[float] = Field(None, description="Estimated processing time in seconds")

class JobStatusResponse(BaseModel):
    """Job status response"""
    id: str
    type: str
    status: str
    progress: float
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]
    error: Optional[str]
    retry_count: int

class BatchStatusResponse(BaseModel):
    """Batch status response"""
    id: str
    name: str
    status: str
    total_jobs: int
    completed_jobs: int
    failed_jobs: int
    overall_progress: float
    job_statuses: Dict[str, int]
    created_at: str
    estimated_duration: Optional[float]
    actual_duration: Optional[float]
    jobs: List[JobStatusResponse]

class ServiceStatsResponse(BaseModel):
    """Service statistics response"""
    queue_size: int
    active_workers: int
    total_jobs_processed: int
    total_jobs_failed: int
    average_processing_time: float
    success_rate: float
    max_workers: int
    is_running: bool
    total_batches: int
    active_batches: int

# Helper functions

def parse_priority(priority_str: str) -> JobPriority:
    """Parse priority string to JobPriority enum"""
    priority_map = {
        "low": JobPriority.LOW,
        "medium": JobPriority.MEDIUM,
        "high": JobPriority.HIGH,
        "urgent": JobPriority.URGENT
    }
    return priority_map.get(priority_str.lower(), JobPriority.MEDIUM)

# API Endpoints

@router.post("/video", response_model=BatchResponse)
async def create_video_batch(
    request: BatchVideoRequest,
    service: BatchProcessingService = Depends(get_batch_service)
):
    """
    Create a batch of video generation jobs
    
    This endpoint allows you to submit multiple video generation requests
    that will be processed in parallel according to the specified priority.
    """
    try:
        # Convert jobs to dict format
        video_requests = [job.dict() for job in request.jobs]
        priority = parse_priority(request.priority)
        
        # Create batch
        batch_id = await service.create_video_batch(
            video_requests=video_requests,
            batch_name=request.batch_name,
            priority=priority
        )
        
        # Get batch info for response
        batch_status = await service.get_batch_status(batch_id)
        
        return BatchResponse(
            batch_id=batch_id,
            message=f"Video batch created successfully with {len(request.jobs)} jobs",
            total_jobs=len(request.jobs),
            estimated_duration=batch_status.get('estimated_duration') if batch_status else None
        )
        
    except Exception as e:
        logger.error(f"Failed to create video batch: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create video batch: {str(e)}")

@router.post("/audio", response_model=BatchResponse)
async def create_audio_batch(
    request: BatchAudioRequest,
    service: BatchProcessingService = Depends(get_batch_service)
):
    """
    Create a batch of audio generation jobs
    
    This endpoint allows you to submit multiple text-to-speech requests
    that will be processed in parallel according to the specified priority.
    """
    try:
        # Convert jobs to dict format
        audio_requests = [job.dict() for job in request.jobs]
        priority = parse_priority(request.priority)
        
        # Create batch
        batch_id = await service.create_audio_batch(
            audio_requests=audio_requests,
            batch_name=request.batch_name,
            priority=priority
        )
        
        # Get batch info for response
        batch_status = await service.get_batch_status(batch_id)
        
        return BatchResponse(
            batch_id=batch_id,
            message=f"Audio batch created successfully with {len(request.jobs)} jobs",
            total_jobs=len(request.jobs),
            estimated_duration=batch_status.get('estimated_duration') if batch_status else None
        )
        
    except Exception as e:
        logger.error(f"Failed to create audio batch: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create audio batch: {str(e)}")

@router.post("/translation", response_model=BatchResponse)
async def create_translation_batch(
    request: BatchTranslationRequest,
    service: BatchProcessingService = Depends(get_batch_service)
):
    """
    Create a batch of translation jobs
    
    This endpoint allows you to submit multiple translation requests
    that will be processed in parallel according to the specified priority.
    """
    try:
        # Convert jobs to dict format
        translation_requests = [job.dict() for job in request.jobs]
        priority = parse_priority(request.priority)
        
        # Create batch
        batch_id = await service.create_translation_batch(
            translation_requests=translation_requests,
            batch_name=request.batch_name,
            priority=priority
        )
        
        # Get batch info for response
        batch_status = await service.get_batch_status(batch_id)
        
        return BatchResponse(
            batch_id=batch_id,
            message=f"Translation batch created successfully with {len(request.jobs)} jobs",
            total_jobs=len(request.jobs),
            estimated_duration=batch_status.get('estimated_duration') if batch_status else None
        )
        
    except Exception as e:
        logger.error(f"Failed to create translation batch: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create translation batch: {str(e)}")

@router.get("/status/{batch_id}", response_model=BatchStatusResponse)
async def get_batch_status(
    batch_id: str,
    service: BatchProcessingService = Depends(get_batch_service)
):
    """
    Get the status of a specific batch
    
    Returns detailed information about the batch including:
    - Overall progress and status
    - Individual job statuses
    - Timing information
    - Error details if any
    """
    try:
        batch_status = await service.get_batch_status(batch_id)
        
        if not batch_status:
            raise HTTPException(status_code=404, detail=f"Batch {batch_id} not found")
        
        # Convert jobs to response format
        jobs = [
            JobStatusResponse(**job_data)
            for job_data in batch_status['jobs']
        ]
        
        return BatchStatusResponse(
            id=batch_status['id'],
            name=batch_status['name'],
            status=batch_status['status'],
            total_jobs=batch_status['total_jobs'],
            completed_jobs=batch_status['completed_jobs'],
            failed_jobs=batch_status['failed_jobs'],
            overall_progress=batch_status['overall_progress'],
            job_statuses=batch_status['job_statuses'],
            created_at=batch_status['created_at'],
            estimated_duration=batch_status['estimated_duration'],
            actual_duration=batch_status['actual_duration'],
            jobs=jobs
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get batch status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get batch status: {str(e)}")

@router.delete("/cancel/{batch_id}")
async def cancel_batch(
    batch_id: str,
    service: BatchProcessingService = Depends(get_batch_service)
):
    """
    Cancel a batch and all its pending jobs
    
    Jobs that are already processing will complete, but pending jobs will be cancelled.
    """
    try:
        success = await service.cancel_batch(batch_id)
        
        if not success:
            raise HTTPException(status_code=404, detail=f"Batch {batch_id} not found or cannot be cancelled")
        
        return {"message": f"Batch {batch_id} cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to cancel batch: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to cancel batch: {str(e)}")

@router.get("/stats", response_model=ServiceStatsResponse)
async def get_service_stats(
    service: BatchProcessingService = Depends(get_batch_service)
):
    """
    Get batch processing service statistics
    
    Returns information about:
    - Queue size and active workers
    - Processing statistics
    - Success rates
    - Service health
    """
    try:
        stats = await service.get_service_stats()
        return ServiceStatsResponse(**stats)
        
    except Exception as e:
        logger.error(f"Failed to get service stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get service stats: {str(e)}")

@router.get("/list")
async def list_batches(
    status: Optional[str] = Query(None, description="Filter by status (pending/processing/completed/failed/cancelled)"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of batches to return"),
    offset: int = Query(0, ge=0, description="Number of batches to skip"),
    service: BatchProcessingService = Depends(get_batch_service)
):
    """
    List all batches with optional filtering
    
    Returns a paginated list of batches with basic information.
    Use the status endpoint to get detailed information about a specific batch.
    """
    try:
        # Get all batches
        all_batches = []
        for batch_id, batch_request in service.batch_requests.items():
            batch_info = {
                'id': batch_request.id,
                'name': batch_request.name,
                'status': batch_request.status.value,
                'total_jobs': batch_request.total_jobs,
                'completed_jobs': batch_request.completed_jobs,
                'failed_jobs': batch_request.failed_jobs,
                'created_at': batch_request.created_at.isoformat(),
                'estimated_duration': batch_request.estimated_duration,
                'actual_duration': batch_request.actual_duration
            }
            all_batches.append(batch_info)
        
        # Filter by status if specified
        if status:
            status_filter = status.lower()
            all_batches = [b for b in all_batches if b['status'] == status_filter]
        
        # Sort by creation time (newest first)
        all_batches.sort(key=lambda x: x['created_at'], reverse=True)
        
        # Apply pagination
        total_count = len(all_batches)
        batches = all_batches[offset:offset + limit]
        
        return {
            'batches': batches,
            'total_count': total_count,
            'limit': limit,
            'offset': offset,
            'has_more': offset + limit < total_count
        }
        
    except Exception as e:
        logger.error(f"Failed to list batches: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list batches: {str(e)}")

@router.post("/cleanup")
async def cleanup_old_batches(
    days_old: int = Query(7, ge=1, le=365, description="Remove batches older than this many days"),
    service: BatchProcessingService = Depends(get_batch_service)
):
    """
    Clean up old completed batches
    
    Removes batches that are completed, failed, or cancelled and older than the specified number of days.
    This helps keep the system clean and reduces memory usage.
    """
    try:
        await service.cleanup_old_batches(days_old=days_old)
        return {"message": f"Cleanup completed for batches older than {days_old} days"}
        
    except Exception as e:
        logger.error(f"Failed to cleanup batches: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to cleanup batches: {str(e)}")

@router.get("/health")
async def health_check(
    service: BatchProcessingService = Depends(get_batch_service)
):
    """
    Health check endpoint for the batch processing service
    
    Returns the current health status of the batch processing service.
    """
    try:
        stats = await service.get_service_stats()
        
        # Determine health status
        is_healthy = (
            stats.get('is_running', False) and
            stats.get('queue_size', 0) < 1000 and  # Queue not too large
            stats.get('success_rate', 0) > 0.8  # Good success rate
        )
        
        return {
            'status': 'healthy' if is_healthy else 'unhealthy',
            'is_running': stats.get('is_running', False),
            'queue_size': stats.get('queue_size', 0),
            'active_workers': stats.get('active_workers', 0),
            'success_rate': stats.get('success_rate', 0),
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }