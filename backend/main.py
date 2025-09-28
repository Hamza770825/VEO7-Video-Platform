"""
VEO7 Video Platform - Backend API
FastAPI application for video generation and processing with Supabase integration
"""

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import uvicorn
import os
from typing import Optional, List, Dict, Any
import asyncio
from datetime import datetime
import uuid
import json
import logging
from pathlib import Path

# Import services
from services.supabase_service import SupabaseService
from services.video_generation_service import VideoGenerationService
from services.paypal_service import PayPalService
from services.paypal_plans import PayPalPlansManager
from services.file_service import FileService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic Models
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    input_type: str  # 'image_audio', 'text_audio', 'image_text'
    input_text: Optional[str] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class CommentCreate(BaseModel):
    project_id: str
    content: str

class RatingCreate(BaseModel):
    project_id: str
    rating: int  # 1-5

class PayPalPayment(BaseModel):
    plan_id: str
    payment_method: str = "paypal"

class PayPalWebhook(BaseModel):
    event_type: str
    resource: Dict[str, Any]

# Initialize FastAPI app
app = FastAPI(
    title="VEO7 Video Platform API",
    description="Professional video generation platform with AI capabilities",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize services
supabase_service = SupabaseService()
video_service = VideoGenerationService()
paypal_service = PayPalService()
paypal_plans_manager = PayPalPlansManager(paypal_service)
file_service = FileService()

# Create directories
os.makedirs("temp_uploads", exist_ok=True)
os.makedirs("output_videos", exist_ok=True)
os.makedirs("models", exist_ok=True)

# Mount static files
app.mount("/outputs", StaticFiles(directory="output_videos"), name="outputs")

# Dependency to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current authenticated user"""
    try:
        token = credentials.credentials
        user = await supabase_service.get_user_from_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")

# Root endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "VEO7 Video Platform API",
        "version": "2.0.0",
        "status": "active",
        "docs": "/docs",
        "features": [
            "AI Video Generation",
            "SadTalker Integration",
            "Wav2Lip Integration", 
            "PayPal Payments",
            "Supabase Backend",
            "Real-time Processing"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test services
        supabase_status = await supabase_service.health_check()
        paypal_status = await paypal_service.health_check()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "supabase": supabase_status,
                "paypal": paypal_status,
                "video_generation": "ready",
                "file_storage": "ready"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

@app.get("/api/health")
async def api_health_check():
    """API Health check endpoint"""
    try:
        # Test services
        supabase_status = await supabase_service.health_check()
        paypal_status = await paypal_service.health_check()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "supabase": supabase_status,
                "paypal": paypal_status,
                "video_generation": "ready",
                "file_storage": "ready"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# Authentication endpoints
@app.post("/api/auth/verify-token")
async def verify_token(user = Depends(get_current_user)):
    """Verify user token and return user info"""
    return {
        "valid": True,
        "user": user
    }

# Project endpoints
@app.get("/api/projects")
async def get_projects(user = Depends(get_current_user)):
    """Get user's projects"""
    try:
        projects = await supabase_service.get_user_projects(user["id"])
        return {"projects": projects}
    except Exception as e:
        logger.error(f"Error getting projects: {e}")
        raise HTTPException(status_code=500, detail="Failed to get projects")

@app.post("/api/projects")
async def create_project(
    project: ProjectCreate,
    user = Depends(get_current_user)
):
    """Create new project"""
    try:
        # Check if user has enough coins
        user_data = await supabase_service.get_user_profile(user["id"])
        if user_data["coins"] < 10:  # 10 coins per video
            raise HTTPException(status_code=400, detail="Insufficient coins")
        
        # Create project
        project_data = {
            "user_id": user["id"],
            "title": project.title,
            "description": project.description,
            "input_type": project.input_type,
            "input_text": project.input_text,
            "status": "pending",
            "coins_used": 10
        }
        
        new_project = await supabase_service.create_project(project_data)
        return {"project": new_project}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail="Failed to create project")

@app.get("/api/projects/{project_id}")
async def get_project(project_id: str, user = Depends(get_current_user)):
    """Get specific project"""
    try:
        project = await supabase_service.get_project(project_id, user["id"])
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"project": project}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project: {e}")
        raise HTTPException(status_code=500, detail="Failed to get project")

@app.put("/api/projects/{project_id}")
async def update_project(
    project_id: str,
    project_update: ProjectUpdate,
    user = Depends(get_current_user)
):
    """Update project"""
    try:
        updated_project = await supabase_service.update_project(
            project_id, user["id"], project_update.dict(exclude_unset=True)
        )
        return {"project": updated_project}
    except Exception as e:
        logger.error(f"Error updating project: {e}")
        raise HTTPException(status_code=500, detail="Failed to update project")

@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: str, user = Depends(get_current_user)):
    """Delete project"""
    try:
        await supabase_service.delete_project(project_id, user["id"])
        return {"message": "Project deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting project: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete project")

# File upload endpoints
@app.post("/api/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    user = Depends(get_current_user)
):
    """Upload image file"""
    try:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        file_url = await file_service.upload_file(file, user["id"], "images")
        return {"file_url": file_url}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading image: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload image")

@app.post("/api/upload/audio")
async def upload_audio(
    file: UploadFile = File(...),
    user = Depends(get_current_user)
):
    """Upload audio file"""
    try:
        if not file.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        file_url = await file_service.upload_file(file, user["id"], "audio")
        return {"file_url": file_url}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading audio: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload audio")

# Video generation endpoints
@app.post("/api/generate-video/{project_id}")
async def generate_video(
    project_id: str,
    background_tasks: BackgroundTasks,
    image_file: Optional[UploadFile] = File(None),
    audio_file: Optional[UploadFile] = File(None),
    user = Depends(get_current_user)
):
    """Generate video from project"""
    try:
        # Get project
        project = await supabase_service.get_project(project_id, user["id"])
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        if project["status"] != "pending":
            raise HTTPException(status_code=400, detail="Project already processed")
        
        # Check user coins
        user_data = await supabase_service.get_user_profile(user["id"])
        if user_data["coins"] < project["coins_used"]:
            raise HTTPException(status_code=400, detail="Insufficient coins")
        
        # Create job
        job_data = {
            "project_id": project_id,
            "user_id": user["id"],
            "status": "queued"
        }
        job = await supabase_service.create_job(job_data)
        
        # Start video generation in background
        background_tasks.add_task(
            process_video_generation,
            project_id,
            job["id"],
            image_file,
            audio_file,
            user["id"]
        )
        
        return {
            "message": "Video generation started",
            "job_id": job["id"],
            "estimated_time": "2-5 minutes"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting video generation: {e}")
        raise HTTPException(status_code=500, detail="Failed to start video generation")

async def process_video_generation(
    project_id: str,
    job_id: str,
    image_file: Optional[UploadFile],
    audio_file: Optional[UploadFile],
    user_id: str
):
    """Background task for video generation"""
    try:
        # Update job status
        await supabase_service.update_job(job_id, {"status": "processing", "progress": 10})
        
        # Get project details
        project = await supabase_service.get_project(project_id, user_id)
        
        # Process files
        image_path = None
        audio_path = None
        
        if image_file:
            image_path = await file_service.save_temp_file(image_file)
        
        if audio_file:
            audio_path = await file_service.save_temp_file(audio_file)
        
        # Update progress
        await supabase_service.update_job(job_id, {"progress": 30})
        
        # Generate video based on input type
        output_path = None
        if project["input_type"] == "image_audio":
            output_path = await video_service.generate_from_image_audio(
                image_path, audio_path, project_id
            )
        elif project["input_type"] == "text_audio":
            output_path = await video_service.generate_from_text_audio(
                project["input_text"], audio_path, project_id
            )
        elif project["input_type"] == "image_text":
            output_path = await video_service.generate_from_image_text(
                image_path, project["input_text"], project_id
            )
        
        # Update progress
        await supabase_service.update_job(job_id, {"progress": 80})
        
        # Upload video to Supabase Storage
        video_url = await file_service.upload_video_to_storage(output_path, user_id, project_id)
        
        # Update project with video URL
        await supabase_service.update_project(project_id, user_id, {
            "output_video_url": video_url,
            "status": "completed",
            "processing_completed_at": datetime.now().isoformat()
        })
        
        # Deduct coins
        await supabase_service.deduct_user_coins(user_id, project["coins_used"], project_id)
        
        # Complete job
        await supabase_service.update_job(job_id, {
            "status": "completed",
            "progress": 100,
            "completed_at": datetime.now().isoformat()
        })
        
        # Cleanup temp files
        if image_path:
            os.remove(image_path)
        if audio_path:
            os.remove(audio_path)
        if output_path:
            os.remove(output_path)
            
    except Exception as e:
        logger.error(f"Video generation failed: {e}")
        # Update job with error
        await supabase_service.update_job(job_id, {
            "status": "failed",
            "error_message": str(e)
        })
        # Update project status
        await supabase_service.update_project(project_id, user_id, {
            "status": "failed"
        })

# Job status endpoints
@app.get("/api/jobs/{job_id}")
async def get_job_status(job_id: str, user = Depends(get_current_user)):
    """Get job status"""
    try:
        job = await supabase_service.get_job(job_id, user["id"])
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return {"job": job}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get job status")

# User profile endpoints
@app.get("/api/profile")
async def get_profile(user = Depends(get_current_user)):
    """Get user profile"""
    try:
        profile = await supabase_service.get_user_profile(user["id"])
        return {"profile": profile}
    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to get profile")

@app.put("/api/profile")
async def update_profile(
    full_name: Optional[str] = Form(None),
    avatar_file: Optional[UploadFile] = File(None),
    user = Depends(get_current_user)
):
    """Update user profile"""
    try:
        update_data = {}
        
        if full_name:
            update_data["full_name"] = full_name
        
        if avatar_file:
            avatar_url = await file_service.upload_file(avatar_file, user["id"], "avatars")
            update_data["avatar_url"] = avatar_url
        
        if update_data:
            updated_profile = await supabase_service.update_user_profile(user["id"], update_data)
            return {"profile": updated_profile}
        
        return {"message": "No changes made"}
        
    except Exception as e:
        logger.error(f"Error updating profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to update profile")

# PayPal endpoints
@app.get("/api/plans")
async def get_plans():
    """Get available plans"""
    try:
        plans = await supabase_service.get_plans()
        return {"plans": plans}
    except Exception as e:
        logger.error(f"Error getting plans from database: {e}")
        # Fallback to mock plans service
        try:
            from mock_plans_service import mock_plans_service
            plans = mock_plans_service.get_active_plans()
            logger.info("Using mock plans service as fallback")
            return {"plans": plans}
        except Exception as mock_error:
            logger.error(f"Error with mock plans service: {mock_error}")
            raise HTTPException(status_code=500, detail="Failed to get plans")

@app.post("/api/payment/create")
async def create_payment(
    payment_data: PayPalPayment,
    user = Depends(get_current_user)
):
    """Create PayPal payment"""
    try:
        plan = await supabase_service.get_plan(payment_data.plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        payment_url = await paypal_service.create_payment(plan, user["id"])
        return {"payment_url": payment_url}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating payment: {e}")
        raise HTTPException(status_code=500, detail="Failed to create payment")

@app.post("/api/payment/webhook")
async def paypal_webhook(webhook_data: PayPalWebhook):
    """Handle PayPal webhooks"""
    try:
        await paypal_service.handle_webhook(webhook_data.dict())
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")

# Comments and ratings
@app.post("/api/comments")
async def create_comment(
    comment: CommentCreate,
    user = Depends(get_current_user)
):
    """Create comment"""
    try:
        comment_data = {
            "project_id": comment.project_id,
            "user_id": user["id"],
            "content": comment.content
        }
        new_comment = await supabase_service.create_comment(comment_data)
        return {"comment": new_comment}
    except Exception as e:
        logger.error(f"Error creating comment: {e}")
        raise HTTPException(status_code=500, detail="Failed to create comment")

@app.get("/api/projects/{project_id}/comments")
async def get_project_comments(project_id: str):
    """Get project comments"""
    try:
        comments = await supabase_service.get_project_comments(project_id)
        return {"comments": comments}
    except Exception as e:
        logger.error(f"Error getting comments: {e}")
        raise HTTPException(status_code=500, detail="Failed to get comments")

@app.post("/api/ratings")
async def create_rating(
    rating: RatingCreate,
    user = Depends(get_current_user)
):
    """Create or update rating"""
    try:
        rating_data = {
            "project_id": rating.project_id,
            "user_id": user["id"],
            "rating": rating.rating
        }
        new_rating = await supabase_service.create_or_update_rating(rating_data)
        return {"rating": new_rating}
    except Exception as e:
        logger.error(f"Error creating rating: {e}")
        raise HTTPException(status_code=500, detail="Failed to create rating")

# File service endpoints
@app.get("/api/files/storage-stats")
async def get_storage_stats():
    """Get storage statistics"""
    try:
        stats = file_service.get_storage_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting storage stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get storage stats")

# Video generation endpoints
@app.get("/api/video/generation-stats")
async def get_generation_stats():
    """Get video generation statistics"""
    try:
        stats = video_service.get_generation_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting generation stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get generation stats")

# PayPal service endpoints
@app.get("/api/payments/paypal-stats")
async def get_paypal_stats():
    """Get PayPal service statistics"""
    try:
        stats = {
            "environment": paypal_service.environment,
            "status": "configured" if paypal_service.client_id else "not_configured"
        }
        return stats
    except Exception as e:
        logger.error(f"Error getting PayPal stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get PayPal stats")

# PayPal Plans endpoints
@app.get("/api/payments/plans")
async def get_subscription_plans():
    """Get all available subscription plans"""
    try:
        plans = paypal_plans_manager.get_all_plans()
        return {"plans": plans}
    except Exception as e:
        logger.error(f"Error getting subscription plans: {e}")
        raise HTTPException(status_code=500, detail="Failed to get subscription plans")

@app.get("/api/payments/plans/{plan_id}")
async def get_plan_details(plan_id: str):
    """Get specific plan details"""
    try:
        plan = paypal_plans_manager.get_plan_details(plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        return {"plan": plan}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting plan details: {e}")
        raise HTTPException(status_code=500, detail="Failed to get plan details")

@app.post("/api/payments/plans/create")
async def create_paypal_plans():
    """Create PayPal subscription plans"""
    try:
        created_plans = await paypal_plans_manager.create_paypal_plans()
        return {"created_plans": created_plans}
    except Exception as e:
        logger.error(f"Error creating PayPal plans: {e}")
        raise HTTPException(status_code=500, detail="Failed to create PayPal plans")

@app.post("/api/payments/subscribe/{plan_id}")
async def create_subscription(plan_id: str, user: dict = Depends(get_current_user)):
    """Create PayPal subscription for user"""
    try:
        plan = paypal_plans_manager.get_plan_details(plan_id)
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        user_data = {
            "email": user.get("email"),
            "first_name": user.get("first_name", "User"),
            "last_name": user.get("last_name", "VEO7")
        }
        
        # This would need the actual PayPal plan ID from the created plans
        # For now, we'll return the plan details
        return {
            "plan": plan,
            "user": user_data,
            "message": "Subscription creation endpoint ready"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating subscription: {e}")
        raise HTTPException(status_code=500, detail="Failed to create subscription")

# AI Models Endpoints
@app.get("/api/ai-models/status")
async def get_ai_models_status(user_data: dict = Depends(get_current_user)):
    """الحصول على حالة نماذج الذكاء الاصطناعي"""
    try:
        status = await video_service.get_ai_models_status()
        return {"status": status}
    except Exception as e:
        logger.error(f"Error getting AI models status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get AI models status")

@app.post("/api/ai-models/initialize")
async def initialize_ai_models(user_data: dict = Depends(get_current_user)):
    """تهيئة نماذج الذكاء الاصطناعي"""
    try:
        # التحقق من صلاحيات المستخدم (admin فقط)
        if user_data.get('role') != 'admin':
            raise HTTPException(status_code=403, detail="Admin access required")
        
        result = await video_service.initialize_ai_models()
        return {"initialized_models": result}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error initializing AI models: {e}")
        raise HTTPException(status_code=500, detail="Failed to initialize AI models")

@app.post("/api/ai-models/enhance-image")
async def enhance_image_quality(
    file: UploadFile = File(...),
    scale: int = Form(2),
    user_data: dict = Depends(get_current_user)
):
    """تحسين جودة الصورة باستخدام Real-ESRGAN"""
    try:
        # التحقق من نوع الملف
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # حفظ الملف المرفوع
        upload_dir = "temp_uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_id = str(uuid.uuid4())
        input_path = os.path.join(upload_dir, f"{file_id}_{file.filename}")
        
        with open(input_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # تحسين الصورة
        enhanced_path = await video_service.enhance_image_quality(
            image_path=input_path,
            scale=scale
        )
        
        # تنظيف الملف المؤقت
        if os.path.exists(input_path):
            os.remove(input_path)
        
        # إرجاع الصورة المحسنة
        if os.path.exists(enhanced_path):
            return FileResponse(
                enhanced_path,
                media_type="image/jpeg",
                filename=f"enhanced_{file.filename}"
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to enhance image")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error enhancing image: {e}")
        raise HTTPException(status_code=500, detail="Failed to enhance image")

@app.post("/api/ai-models/generate-sadtalker")
async def generate_sadtalker_video(
    image: UploadFile = File(...),
    audio: UploadFile = File(...),
    quality: str = Form("medium"),
    user_data: dict = Depends(get_current_user)
):
    """توليد فيديو باستخدام SadTalker"""
    try:
        # التحقق من أنواع الملفات
        if not image.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="First file must be an image")
        
        if not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="Second file must be audio")
        
        # حفظ الملفات المرفوعة
        upload_dir = "temp_uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_id = str(uuid.uuid4())
        image_path = os.path.join(upload_dir, f"{file_id}_image_{image.filename}")
        audio_path = os.path.join(upload_dir, f"{file_id}_audio_{audio.filename}")
        
        # حفظ الصورة
        with open(image_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
        
        # حفظ الصوت
        with open(audio_path, "wb") as buffer:
            content = await audio.read()
            buffer.write(content)
        
        # توليد الفيديو باستخدام SadTalker
        output_path = os.path.join("outputs", f"sadtalker_{file_id}.mp4")
        
        if hasattr(video_service, 'ai_models_service') and video_service.ai_models_service:
            result = await video_service.ai_models_service.generate_sadtalker_video(
                image_path=image_path,
                audio_path=audio_path,
                output_path=output_path,
                quality=quality
            )
            
            # تنظيف الملفات المؤقتة
            for temp_file in [image_path, audio_path]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            if result.get('success', False):
                return FileResponse(
                    result['output_path'],
                    media_type="video/mp4",
                    filename=f"sadtalker_video_{file_id}.mp4"
                )
            else:
                raise HTTPException(status_code=500, detail=result.get('message', 'SadTalker generation failed'))
        else:
            raise HTTPException(status_code=503, detail="SadTalker service not available")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating SadTalker video: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate SadTalker video")

@app.post("/api/ai-models/generate-wav2lip")
async def generate_wav2lip_video(
    video: UploadFile = File(...),
    audio: UploadFile = File(...),
    quality: str = Form("medium"),
    user_data: dict = Depends(get_current_user)
):
    """مزامنة حركة الشفاه باستخدام Wav2Lip"""
    try:
        # التحقق من أنواع الملفات
        if not video.content_type.startswith('video/'):
            raise HTTPException(status_code=400, detail="First file must be a video")
        
        if not audio.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="Second file must be audio")
        
        # حفظ الملفات المرفوعة
        upload_dir = "temp_uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        file_id = str(uuid.uuid4())
        video_path = os.path.join(upload_dir, f"{file_id}_video_{video.filename}")
        audio_path = os.path.join(upload_dir, f"{file_id}_audio_{audio.filename}")
        
        # حفظ الفيديو
        with open(video_path, "wb") as buffer:
            content = await video.read()
            buffer.write(content)
        
        # حفظ الصوت
        with open(audio_path, "wb") as buffer:
            content = await audio.read()
            buffer.write(content)
        
        # مزامنة الفيديو باستخدام Wav2Lip
        output_path = os.path.join("outputs", f"wav2lip_{file_id}.mp4")
        
        if hasattr(video_service, 'ai_models_service') and video_service.ai_models_service:
            result = await video_service.ai_models_service.generate_wav2lip_video(
                video_path=video_path,
                audio_path=audio_path,
                output_path=output_path,
                quality=quality
            )
            
            # تنظيف الملفات المؤقتة
            for temp_file in [video_path, audio_path]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            
            if result.get('success', False):
                return FileResponse(
                    result['output_path'],
                    media_type="video/mp4",
                    filename=f"wav2lip_video_{file_id}.mp4"
                )
            else:
                raise HTTPException(status_code=500, detail=result.get('message', 'Wav2Lip generation failed'))
        else:
            raise HTTPException(status_code=503, detail="Wav2Lip service not available")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating Wav2Lip video: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate Wav2Lip video")

# Additional endpoints for compatibility
@app.get("/api/videos")
async def get_videos(current_user: dict = Depends(get_current_user)):
    """Get user videos - alias for projects"""
    try:
        projects = await supabase_service.get_user_projects(current_user['id'])
        return {"success": True, "videos": projects}
    except Exception as e:
        logger.error(f"Error getting videos: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/videos/generate")
async def generate_video_alias(
    project_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """Generate video - alias for generate-video"""
    try:
        # Create project first
        project = await supabase_service.create_project(
            user_id=current_user['id'],
            title=project_data.get('title', 'Generated Video'),
            description=project_data.get('description', ''),
            input_type=project_data.get('input_type', 'text_audio'),
            input_text=project_data.get('input_text', '')
        )
        
        # Start video generation
        job_id = str(uuid.uuid4())
        asyncio.create_task(video_service.generate_video_async(
            project_id=project['id'],
            job_id=job_id,
            **project_data
        ))
        
        return {
            "success": True,
            "job_id": job_id,
            "project_id": project['id'],
            "message": "Video generation started"
        }
    except Exception as e:
        logger.error(f"Error generating video: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/videos/create")
async def create_video(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """Create video - compatible with frontend"""
    try:
        # Parse form data or JSON
        content_type = request.headers.get('content-type', '')
        
        if 'multipart/form-data' in content_type:
            # Handle form data with file upload
            form = await request.form()
            
            # Extract data from form
            title = form.get('title', 'Generated Video')
            description = form.get('description', '')
            text = form.get('text', '')
            settings_str = form.get('settings', '{}')
            
            try:
                settings = json.loads(settings_str) if settings_str else {}
            except:
                settings = {}
            
            # Handle image file
            image_file = form.get('image')
            if image_file and hasattr(image_file, 'file'):
                # Save uploaded image
                upload_dir = Path("uploads/images")
                upload_dir.mkdir(parents=True, exist_ok=True)
                
                file_extension = Path(image_file.filename).suffix
                filename = f"{uuid.uuid4()}{file_extension}"
                file_path = upload_dir / filename
                
                with open(file_path, "wb") as buffer:
                    content = await image_file.read()
                    buffer.write(content)
                
                image_path = str(file_path)
            else:
                image_path = None
        else:
            # Handle JSON data
            data = await request.json()
            title = data.get('title', 'Generated Video')
            description = data.get('description', '')
            text = data.get('text_content', data.get('text', ''))
            settings = data.get('settings', {})
            image_path = None
        
        # Create project
        project = await supabase_service.create_project(
            user_id=current_user['id'],
            title=title,
            description=description,
            input_type='text_audio',
            input_text=text
        )
        
        # Start video generation
        job_id = str(uuid.uuid4())
        
        # Prepare generation data
        generation_data = {
            'text': text,
            'settings': settings,
            'image_path': image_path
        }
        
        # Start async video generation
        asyncio.create_task(video_service.generate_video_async(
            project_id=project['id'],
            job_id=job_id,
            **generation_data
        ))
        
        return {
            "success": True,
            "video_id": project['id'],
            "job_id": job_id,
            "message": "Video creation started",
            "status": "processing"
        }
        
    except Exception as e:
        logger.error(f"Error creating video: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/videos/{video_id}/status")
async def get_video_status(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get video processing status"""
    try:
        # Get project/video details
        project = await supabase_service.get_project(video_id)
        
        if not project or project.get('user_id') != current_user['id']:
            raise HTTPException(status_code=404, detail="Video not found")
        
        # Return status based on project status
        status_mapping = {
            'pending': 'processing_audio',
            'processing': 'processing_video',
            'completed': 'completed',
            'failed': 'failed'
        }
        
        return {
            "success": True,
            "status": status_mapping.get(project.get('status', 'pending'), 'processing_audio'),
            "progress": 50 if project.get('status') == 'processing' else 100 if project.get('status') == 'completed' else 25,
            "video_id": video_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting video status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/auth/login")
async def login_endpoint():
    """Login endpoint - handled by frontend"""
    return {"message": "Login handled by frontend authentication"}

@app.post("/api/auth/register")
async def register_endpoint():
    """Register endpoint - handled by frontend"""
    return {"message": "Registration handled by frontend authentication"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )