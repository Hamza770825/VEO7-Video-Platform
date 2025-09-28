"""
Batch Processing Service
Handles batch processing of multiple videos with queue management and progress tracking
"""

import asyncio
import os
import json
import time
import uuid
from typing import List, Dict, Optional, Callable, Any
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from queue import Queue, PriorityQueue
import logging

from .video_service import VideoService
from .audio_service import AudioService
from .translation_service import EnhancedTranslationService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class JobPriority(Enum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1
    URGENT = 0

@dataclass
class BatchJob:
    """Represents a single job in the batch processing queue"""
    id: str
    job_type: str  # 'video', 'audio', 'translation'
    input_data: Dict[str, Any]
    priority: JobPriority
    status: JobStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    progress: float = 0.0
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3

    def __lt__(self, other):
        """For priority queue ordering"""
        return self.priority.value < other.priority.value

@dataclass
class BatchRequest:
    """Represents a batch processing request"""
    id: str
    name: str
    jobs: List[BatchJob]
    created_at: datetime
    total_jobs: int
    completed_jobs: int = 0
    failed_jobs: int = 0
    status: JobStatus = JobStatus.PENDING
    estimated_duration: Optional[float] = None
    actual_duration: Optional[float] = None

class BatchProcessingService:
    def __init__(self, max_workers: int = 4, cache_dir: str = "cache/batch"):
        """Initialize batch processing service"""
        self.max_workers = max_workers
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Initialize services
        self.video_service = VideoService()
        self.audio_service = AudioService()
        self.translation_service = EnhancedTranslationService()
        
        # Queue management
        self.job_queue = PriorityQueue()
        self.active_jobs: Dict[str, BatchJob] = {}
        self.completed_jobs: Dict[str, BatchJob] = {}
        self.batch_requests: Dict[str, BatchRequest] = {}
        
        # Worker management
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.is_running = False
        self.worker_thread = None
        
        # Statistics
        self.stats = {
            'total_jobs_processed': 0,
            'total_jobs_failed': 0,
            'average_processing_time': 0.0,
            'queue_size': 0,
            'active_workers': 0
        }
        
        # Load persistent data
        self._load_persistent_data()
        
        # Start worker thread
        self.start_processing()
    
    def _load_persistent_data(self):
        """Load persistent batch data from disk"""
        try:
            batch_file = os.path.join(self.cache_dir, "batch_requests.json")
            if os.path.exists(batch_file):
                with open(batch_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Restore batch requests
                for batch_id, batch_data in data.get('batch_requests', {}).items():
                    batch_request = BatchRequest(**batch_data)
                    # Convert datetime strings back to datetime objects
                    batch_request.created_at = datetime.fromisoformat(batch_data['created_at'])
                    
                    # Restore jobs
                    jobs = []
                    for job_data in batch_data.get('jobs', []):
                        job = BatchJob(**job_data)
                        job.created_at = datetime.fromisoformat(job_data['created_at'])
                        if job_data.get('started_at'):
                            job.started_at = datetime.fromisoformat(job_data['started_at'])
                        if job_data.get('completed_at'):
                            job.completed_at = datetime.fromisoformat(job_data['completed_at'])
                        job.priority = JobPriority(job_data['priority'])
                        job.status = JobStatus(job_data['status'])
                        jobs.append(job)
                    
                    batch_request.jobs = jobs
                    batch_request.status = JobStatus(batch_data['status'])
                    self.batch_requests[batch_id] = batch_request
                    
                logger.info(f"Loaded {len(self.batch_requests)} batch requests from disk")
                
        except Exception as e:
            logger.error(f"Failed to load persistent data: {e}")
    
    def _save_persistent_data(self):
        """Save persistent batch data to disk"""
        try:
            batch_file = os.path.join(self.cache_dir, "batch_requests.json")
            
            # Prepare data for serialization
            data = {
                'batch_requests': {},
                'stats': self.stats
            }
            
            for batch_id, batch_request in self.batch_requests.items():
                batch_data = asdict(batch_request)
                
                # Convert datetime objects to strings
                batch_data['created_at'] = batch_request.created_at.isoformat()
                batch_data['status'] = batch_request.status.value
                
                # Convert jobs
                jobs_data = []
                for job in batch_request.jobs:
                    job_data = asdict(job)
                    job_data['created_at'] = job.created_at.isoformat()
                    if job.started_at:
                        job_data['started_at'] = job.started_at.isoformat()
                    if job.completed_at:
                        job_data['completed_at'] = job.completed_at.isoformat()
                    job_data['priority'] = job.priority.value
                    job_data['status'] = job.status.value
                    jobs_data.append(job_data)
                
                batch_data['jobs'] = jobs_data
                data['batch_requests'][batch_id] = batch_data
            
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save persistent data: {e}")
    
    async def create_video_batch(self, video_requests: List[Dict], 
                                batch_name: str = None, 
                                priority: JobPriority = JobPriority.MEDIUM) -> str:
        """
        Create a batch of video generation jobs
        
        Args:
            video_requests: List of video generation requests
            batch_name: Optional name for the batch
            priority: Priority level for the batch
            
        Returns:
            Batch ID
        """
        try:
            batch_id = str(uuid.uuid4())
            batch_name = batch_name or f"Video Batch {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create jobs
            jobs = []
            for i, request in enumerate(video_requests):
                job_id = f"{batch_id}_video_{i}"
                job = BatchJob(
                    id=job_id,
                    job_type="video",
                    input_data=request,
                    priority=priority,
                    status=JobStatus.PENDING,
                    created_at=datetime.now()
                )
                jobs.append(job)
                
                # Add to queue
                self.job_queue.put(job)
            
            # Create batch request
            batch_request = BatchRequest(
                id=batch_id,
                name=batch_name,
                jobs=jobs,
                created_at=datetime.now(),
                total_jobs=len(jobs),
                estimated_duration=self._estimate_batch_duration(jobs)
            )
            
            self.batch_requests[batch_id] = batch_request
            self.stats['queue_size'] = self.job_queue.qsize()
            
            # Save to disk
            self._save_persistent_data()
            
            logger.info(f"Created video batch {batch_id} with {len(jobs)} jobs")
            return batch_id
            
        except Exception as e:
            logger.error(f"Failed to create video batch: {e}")
            raise Exception(f"Batch creation failed: {str(e)}")
    
    async def create_audio_batch(self, audio_requests: List[Dict], 
                                batch_name: str = None, 
                                priority: JobPriority = JobPriority.MEDIUM) -> str:
        """Create a batch of audio generation jobs"""
        try:
            batch_id = str(uuid.uuid4())
            batch_name = batch_name or f"Audio Batch {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            jobs = []
            for i, request in enumerate(audio_requests):
                job_id = f"{batch_id}_audio_{i}"
                job = BatchJob(
                    id=job_id,
                    job_type="audio",
                    input_data=request,
                    priority=priority,
                    status=JobStatus.PENDING,
                    created_at=datetime.now()
                )
                jobs.append(job)
                self.job_queue.put(job)
            
            batch_request = BatchRequest(
                id=batch_id,
                name=batch_name,
                jobs=jobs,
                created_at=datetime.now(),
                total_jobs=len(jobs),
                estimated_duration=self._estimate_batch_duration(jobs)
            )
            
            self.batch_requests[batch_id] = batch_request
            self.stats['queue_size'] = self.job_queue.qsize()
            self._save_persistent_data()
            
            logger.info(f"Created audio batch {batch_id} with {len(jobs)} jobs")
            return batch_id
            
        except Exception as e:
            logger.error(f"Failed to create audio batch: {e}")
            raise Exception(f"Audio batch creation failed: {str(e)}")
    
    async def create_translation_batch(self, translation_requests: List[Dict], 
                                      batch_name: str = None, 
                                      priority: JobPriority = JobPriority.MEDIUM) -> str:
        """Create a batch of translation jobs"""
        try:
            batch_id = str(uuid.uuid4())
            batch_name = batch_name or f"Translation Batch {datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            jobs = []
            for i, request in enumerate(translation_requests):
                job_id = f"{batch_id}_translation_{i}"
                job = BatchJob(
                    id=job_id,
                    job_type="translation",
                    input_data=request,
                    priority=priority,
                    status=JobStatus.PENDING,
                    created_at=datetime.now()
                )
                jobs.append(job)
                self.job_queue.put(job)
            
            batch_request = BatchRequest(
                id=batch_id,
                name=batch_name,
                jobs=jobs,
                created_at=datetime.now(),
                total_jobs=len(jobs),
                estimated_duration=self._estimate_batch_duration(jobs)
            )
            
            self.batch_requests[batch_id] = batch_request
            self.stats['queue_size'] = self.job_queue.qsize()
            self._save_persistent_data()
            
            logger.info(f"Created translation batch {batch_id} with {len(jobs)} jobs")
            return batch_id
            
        except Exception as e:
            logger.error(f"Failed to create translation batch: {e}")
            raise Exception(f"Translation batch creation failed: {str(e)}")
    
    def _estimate_batch_duration(self, jobs: List[BatchJob]) -> float:
        """Estimate total duration for batch processing"""
        try:
            # Base estimates per job type (in seconds)
            estimates = {
                'video': 30.0,  # Average video generation time
                'audio': 5.0,   # Average audio generation time
                'translation': 2.0  # Average translation time
            }
            
            total_estimate = 0.0
            for job in jobs:
                base_estimate = estimates.get(job.job_type, 10.0)
                
                # Adjust based on input complexity
                if job.job_type == 'video':
                    duration = job.input_data.get('duration', 5.0)
                    quality = job.input_data.get('quality', 'medium')
                    quality_multiplier = {'fast': 0.7, 'medium': 1.0, 'high': 1.5}.get(quality, 1.0)
                    total_estimate += base_estimate * (duration / 5.0) * quality_multiplier
                
                elif job.job_type == 'audio':
                    text_length = len(job.input_data.get('text', ''))
                    total_estimate += base_estimate * (text_length / 100.0)
                
                elif job.job_type == 'translation':
                    text_length = len(job.input_data.get('text', ''))
                    total_estimate += base_estimate * (text_length / 200.0)
            
            # Account for parallel processing
            parallel_factor = min(self.max_workers, len(jobs)) / len(jobs)
            return total_estimate * parallel_factor
            
        except Exception as e:
            logger.error(f"Duration estimation failed: {e}")
            return len(jobs) * 10.0  # Fallback estimate
    
    def start_processing(self):
        """Start the batch processing worker thread"""
        if not self.is_running:
            self.is_running = True
            self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
            self.worker_thread.start()
            logger.info("Batch processing started")
    
    def stop_processing(self):
        """Stop the batch processing worker thread"""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5.0)
        logger.info("Batch processing stopped")
    
    def _process_queue(self):
        """Main worker thread function"""
        while self.is_running:
            try:
                # Get job from queue (with timeout to allow checking is_running)
                try:
                    job = self.job_queue.get(timeout=1.0)
                except:
                    continue
                
                if job.status == JobStatus.CANCELLED:
                    continue
                
                # Process the job
                self._process_job(job)
                self.job_queue.task_done()
                
            except Exception as e:
                logger.error(f"Queue processing error: {e}")
                time.sleep(1.0)
    
    def _process_job(self, job: BatchJob):
        """Process a single job"""
        try:
            job.status = JobStatus.PROCESSING
            job.started_at = datetime.now()
            self.active_jobs[job.id] = job
            
            logger.info(f"Processing job {job.id} ({job.job_type})")
            
            # Process based on job type
            if job.job_type == "video":
                result = self._process_video_job(job)
            elif job.job_type == "audio":
                result = self._process_audio_job(job)
            elif job.job_type == "translation":
                result = self._process_translation_job(job)
            else:
                raise Exception(f"Unknown job type: {job.job_type}")
            
            # Mark as completed
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.now()
            job.result = result
            job.progress = 100.0
            
            # Update statistics
            self.stats['total_jobs_processed'] += 1
            processing_time = (job.completed_at - job.started_at).total_seconds()
            self._update_average_processing_time(processing_time)
            
            logger.info(f"Job {job.id} completed successfully")
            
        except Exception as e:
            logger.error(f"Job {job.id} failed: {e}")
            job.status = JobStatus.FAILED
            job.error = str(e)
            job.completed_at = datetime.now()
            
            # Retry logic
            if job.retry_count < job.max_retries:
                job.retry_count += 1
                job.status = JobStatus.PENDING
                job.started_at = None
                job.completed_at = None
                job.error = None
                
                # Re-queue with lower priority
                job.priority = JobPriority(min(job.priority.value + 1, JobPriority.LOW.value))
                self.job_queue.put(job)
                logger.info(f"Job {job.id} queued for retry ({job.retry_count}/{job.max_retries})")
            else:
                self.stats['total_jobs_failed'] += 1
                logger.error(f"Job {job.id} failed permanently after {job.max_retries} retries")
        
        finally:
            # Move from active to completed
            if job.id in self.active_jobs:
                del self.active_jobs[job.id]
            self.completed_jobs[job.id] = job
            
            # Update batch status
            self._update_batch_status(job)
            
            # Update queue size
            self.stats['queue_size'] = self.job_queue.qsize()
            self.stats['active_workers'] = len(self.active_jobs)
            
            # Save progress
            self._save_persistent_data()
    
    def _process_video_job(self, job: BatchJob) -> Dict[str, Any]:
        """Process a video generation job"""
        try:
            input_data = job.input_data
            
            # Extract parameters
            image_path = input_data.get('image_path')
            audio_path = input_data.get('audio_path')
            output_path = input_data.get('output_path')
            duration = input_data.get('duration', 5.0)
            quality = input_data.get('quality', 'medium')
            effects = input_data.get('effects', [])
            
            # Generate video
            result = asyncio.run(self.video_service.generate_video(
                image_path=image_path,
                audio_path=audio_path,
                output_path=output_path,
                duration=duration,
                quality=quality,
                effects=effects
            ))
            
            return {
                'output_path': result,
                'duration': duration,
                'quality': quality,
                'effects_applied': effects
            }
            
        except Exception as e:
            raise Exception(f"Video processing failed: {str(e)}")
    
    def _process_audio_job(self, job: BatchJob) -> Dict[str, Any]:
        """Process an audio generation job"""
        try:
            input_data = job.input_data
            
            # Extract parameters
            text = input_data.get('text')
            output_path = input_data.get('output_path')
            voice = input_data.get('voice', 'female')
            quality = input_data.get('quality', 'medium')
            language = input_data.get('language', 'en')
            
            # Generate audio
            result = asyncio.run(self.audio_service.generate_audio(
                text=text,
                output_path=output_path,
                voice=voice,
                quality=quality,
                language=language
            ))
            
            return {
                'output_path': result,
                'text_length': len(text),
                'voice': voice,
                'quality': quality,
                'language': language
            }
            
        except Exception as e:
            raise Exception(f"Audio processing failed: {str(e)}")
    
    def _process_translation_job(self, job: BatchJob) -> Dict[str, Any]:
        """Process a translation job"""
        try:
            input_data = job.input_data
            
            # Extract parameters
            text = input_data.get('text')
            source_lang = input_data.get('source_lang')
            target_lang = input_data.get('target_lang')
            quality = input_data.get('quality', 'medium')
            
            # Perform translation
            result = asyncio.run(self.translation_service.translate_text(
                text=text,
                source_lang=source_lang,
                target_lang=target_lang,
                quality=quality
            ))
            
            return result
            
        except Exception as e:
            raise Exception(f"Translation processing failed: {str(e)}")
    
    def _update_batch_status(self, job: BatchJob):
        """Update the status of the batch containing this job"""
        try:
            # Find the batch containing this job
            batch_id = job.id.split('_')[0]
            if batch_id not in self.batch_requests:
                return
            
            batch_request = self.batch_requests[batch_id]
            
            # Count completed and failed jobs
            completed_jobs = sum(1 for j in batch_request.jobs if j.status == JobStatus.COMPLETED)
            failed_jobs = sum(1 for j in batch_request.jobs if j.status == JobStatus.FAILED)
            
            batch_request.completed_jobs = completed_jobs
            batch_request.failed_jobs = failed_jobs
            
            # Update batch status
            if completed_jobs + failed_jobs == batch_request.total_jobs:
                if failed_jobs == 0:
                    batch_request.status = JobStatus.COMPLETED
                elif completed_jobs == 0:
                    batch_request.status = JobStatus.FAILED
                else:
                    batch_request.status = JobStatus.COMPLETED  # Partial success
                
                # Calculate actual duration
                if batch_request.jobs:
                    start_times = [j.started_at for j in batch_request.jobs if j.started_at]
                    end_times = [j.completed_at for j in batch_request.jobs if j.completed_at]
                    
                    if start_times and end_times:
                        batch_request.actual_duration = (max(end_times) - min(start_times)).total_seconds()
            
        except Exception as e:
            logger.error(f"Failed to update batch status: {e}")
    
    def _update_average_processing_time(self, processing_time: float):
        """Update average processing time statistics"""
        try:
            current_avg = self.stats['average_processing_time']
            total_processed = self.stats['total_jobs_processed']
            
            if total_processed == 1:
                self.stats['average_processing_time'] = processing_time
            else:
                # Calculate running average
                self.stats['average_processing_time'] = (
                    (current_avg * (total_processed - 1) + processing_time) / total_processed
                )
        except Exception as e:
            logger.error(f"Failed to update average processing time: {e}")
    
    async def get_batch_status(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a batch"""
        try:
            if batch_id not in self.batch_requests:
                return None
            
            batch_request = self.batch_requests[batch_id]
            
            # Calculate progress
            total_progress = sum(job.progress for job in batch_request.jobs)
            overall_progress = total_progress / batch_request.total_jobs if batch_request.total_jobs > 0 else 0
            
            # Get job statuses
            job_statuses = {}
            for status in JobStatus:
                job_statuses[status.value] = sum(1 for job in batch_request.jobs if job.status == status)
            
            return {
                'id': batch_request.id,
                'name': batch_request.name,
                'status': batch_request.status.value,
                'total_jobs': batch_request.total_jobs,
                'completed_jobs': batch_request.completed_jobs,
                'failed_jobs': batch_request.failed_jobs,
                'overall_progress': overall_progress,
                'job_statuses': job_statuses,
                'created_at': batch_request.created_at.isoformat(),
                'estimated_duration': batch_request.estimated_duration,
                'actual_duration': batch_request.actual_duration,
                'jobs': [
                    {
                        'id': job.id,
                        'type': job.job_type,
                        'status': job.status.value,
                        'progress': job.progress,
                        'created_at': job.created_at.isoformat(),
                        'started_at': job.started_at.isoformat() if job.started_at else None,
                        'completed_at': job.completed_at.isoformat() if job.completed_at else None,
                        'error': job.error,
                        'retry_count': job.retry_count
                    }
                    for job in batch_request.jobs
                ]
            }
            
        except Exception as e:
            logger.error(f"Failed to get batch status: {e}")
            return None
    
    async def cancel_batch(self, batch_id: str) -> bool:
        """Cancel a batch and all its jobs"""
        try:
            if batch_id not in self.batch_requests:
                return False
            
            batch_request = self.batch_requests[batch_id]
            
            # Cancel all pending jobs
            for job in batch_request.jobs:
                if job.status == JobStatus.PENDING:
                    job.status = JobStatus.CANCELLED
            
            batch_request.status = JobStatus.CANCELLED
            
            logger.info(f"Batch {batch_id} cancelled")
            self._save_persistent_data()
            return True
            
        except Exception as e:
            logger.error(f"Failed to cancel batch: {e}")
            return False
    
    async def get_service_stats(self) -> Dict[str, Any]:
        """Get batch processing service statistics"""
        try:
            return {
                'queue_size': self.stats['queue_size'],
                'active_workers': self.stats['active_workers'],
                'total_jobs_processed': self.stats['total_jobs_processed'],
                'total_jobs_failed': self.stats['total_jobs_failed'],
                'average_processing_time': self.stats['average_processing_time'],
                'success_rate': (
                    self.stats['total_jobs_processed'] / 
                    (self.stats['total_jobs_processed'] + self.stats['total_jobs_failed'])
                    if (self.stats['total_jobs_processed'] + self.stats['total_jobs_failed']) > 0 else 0
                ),
                'max_workers': self.max_workers,
                'is_running': self.is_running,
                'total_batches': len(self.batch_requests),
                'active_batches': sum(1 for b in self.batch_requests.values() 
                                    if b.status == JobStatus.PROCESSING)
            }
            
        except Exception as e:
            logger.error(f"Failed to get service stats: {e}")
            return {}
    
    async def cleanup_old_batches(self, days_old: int = 7):
        """Clean up old completed batches"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days_old)
            to_remove = []
            
            for batch_id, batch_request in self.batch_requests.items():
                if (batch_request.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED] and
                    batch_request.created_at < cutoff_date):
                    to_remove.append(batch_id)
            
            for batch_id in to_remove:
                del self.batch_requests[batch_id]
            
            # Clean up completed jobs
            cutoff_time = datetime.now() - timedelta(days=days_old)
            old_jobs = [job_id for job_id, job in self.completed_jobs.items() 
                       if job.completed_at and job.completed_at < cutoff_time]
            
            for job_id in old_jobs:
                del self.completed_jobs[job_id]
            
            self._save_persistent_data()
            logger.info(f"Cleaned up {len(to_remove)} old batches and {len(old_jobs)} old jobs")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")

    def __del__(self):
        """Cleanup when service is destroyed"""
        self.stop_processing()
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=True)