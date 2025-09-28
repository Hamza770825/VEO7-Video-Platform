"""
Supabase Service for VEO7 Video Platform
Handles all database operations and authentication
"""

import os
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)

class SupabaseService:
    def __init__(self):
        """Initialize Supabase client"""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_ANON_KEY")
        self.service_key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("Supabase URL and key must be provided")
        
        # Client for regular operations
        self.client: Client = create_client(self.url, self.key)
        
        # Service client for admin operations
        if self.service_key:
            self.service_client: Client = create_client(self.url, self.service_key)
        else:
            self.service_client = self.client
    
    async def health_check(self) -> str:
        """Check Supabase connection health"""
        try:
            result = self.client.table("users").select("count").limit(1).execute()
            return "healthy"
        except Exception as e:
            logger.error(f"Supabase health check failed: {e}")
            return "unhealthy"
    
    async def get_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Get user from JWT token"""
        try:
            # Set the token for the client
            self.client.auth.set_session(token, None)
            user = self.client.auth.get_user()
            
            if user and user.user:
                return {
                    "id": user.user.id,
                    "email": user.user.email,
                    "user_metadata": user.user.user_metadata
                }
            return None
        except Exception as e:
            logger.error(f"Error getting user from token: {e}")
            return None
    
    # User Profile Operations
    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile"""
        try:
            result = self.client.table("users").select("*").eq("id", user_id).single().execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            raise
    
    async def update_user_profile(self, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        try:
            update_data["updated_at"] = datetime.now().isoformat()
            result = self.client.table("users").update(update_data).eq("id", user_id).execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
            raise
    
    # Project Operations
    async def get_user_projects(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all projects for a user"""
        try:
            result = self.client.table("projects").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting user projects: {e}")
            raise
    
    async def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new project"""
        try:
            project_data["id"] = str(uuid.uuid4())
            project_data["created_at"] = datetime.now().isoformat()
            project_data["updated_at"] = datetime.now().isoformat()
            
            result = self.client.table("projects").insert(project_data).execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            raise
    
    async def get_project(self, project_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get specific project"""
        try:
            result = self.client.table("projects").select("*").eq("id", project_id).eq("user_id", user_id).single().execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting project: {e}")
            return None
    
    async def update_project(self, project_id: str, user_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update project"""
        try:
            update_data["updated_at"] = datetime.now().isoformat()
            result = self.client.table("projects").update(update_data).eq("id", project_id).eq("user_id", user_id).execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Error updating project: {e}")
            raise
    
    async def delete_project(self, project_id: str, user_id: str):
        """Delete project"""
        try:
            self.client.table("projects").delete().eq("id", project_id).eq("user_id", user_id).execute()
        except Exception as e:
            logger.error(f"Error deleting project: {e}")
            raise
    
    # Job Operations
    async def create_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new job"""
        try:
            job_data["id"] = str(uuid.uuid4())
            job_data["created_at"] = datetime.now().isoformat()
            job_data["updated_at"] = datetime.now().isoformat()
            job_data["progress"] = 0
            
            result = self.client.table("jobs").insert(job_data).execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Error creating job: {e}")
            raise
    
    async def get_job(self, job_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get job status"""
        try:
            result = self.client.table("jobs").select("*").eq("id", job_id).eq("user_id", user_id).single().execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting job: {e}")
            return None
    
    async def update_job(self, job_id: str, update_data: Dict[str, Any]):
        """Update job status"""
        try:
            update_data["updated_at"] = datetime.now().isoformat()
            self.client.table("jobs").update(update_data).eq("id", job_id).execute()
        except Exception as e:
            logger.error(f"Error updating job: {e}")
            raise
    
    # Coins Operations
    async def deduct_user_coins(self, user_id: str, amount: int, project_id: str):
        """Deduct coins from user account"""
        try:
            # Create transaction record
            transaction_data = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "amount": -amount,
                "type": "video_generation",
                "description": f"Video generation for project {project_id}",
                "project_id": project_id,
                "created_at": datetime.now().isoformat()
            }
            
            # Insert transaction
            self.client.table("coins_transactions").insert(transaction_data).execute()
            
            # Update user coins using the database function
            self.client.rpc("update_user_coins", {
                "user_id": user_id,
                "amount": -amount
            }).execute()
            
        except Exception as e:
            logger.error(f"Error deducting coins: {e}")
            raise
    
    async def add_user_coins(self, user_id: str, amount: int, transaction_type: str, description: str):
        """Add coins to user account"""
        try:
            # Create transaction record
            transaction_data = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "amount": amount,
                "type": transaction_type,
                "description": description,
                "created_at": datetime.now().isoformat()
            }
            
            # Insert transaction
            self.client.table("coins_transactions").insert(transaction_data).execute()
            
            # Update user coins using the database function
            self.client.rpc("update_user_coins", {
                "user_id": user_id,
                "amount": amount
            }).execute()
            
        except Exception as e:
            logger.error(f"Error adding coins: {e}")
            raise
    
    # Plans Operations
    async def get_plans(self) -> List[Dict[str, Any]]:
        """Get all available plans"""
        try:
            result = self.client.table("plans").select("*").eq("is_active", True).order("price").execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting plans: {e}")
            raise
    
    async def get_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Get specific plan"""
        try:
            result = self.client.table("plans").select("*").eq("id", plan_id).single().execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting plan: {e}")
            return None
    
    # Subscription Operations
    async def create_subscription(self, subscription_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new subscription"""
        try:
            subscription_data["id"] = str(uuid.uuid4())
            subscription_data["created_at"] = datetime.now().isoformat()
            subscription_data["updated_at"] = datetime.now().isoformat()
            
            result = self.client.table("subscriptions").insert(subscription_data).execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Error creating subscription: {e}")
            raise
    
    async def update_subscription(self, subscription_id: str, update_data: Dict[str, Any]):
        """Update subscription"""
        try:
            update_data["updated_at"] = datetime.now().isoformat()
            self.client.table("subscriptions").update(update_data).eq("id", subscription_id).execute()
        except Exception as e:
            logger.error(f"Error updating subscription: {e}")
            raise
    
    async def get_user_subscription(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's active subscription"""
        try:
            result = self.client.table("subscriptions").select("*, plans(*)").eq("user_id", user_id).eq("status", "active").single().execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting user subscription: {e}")
            return None
    
    # Comments Operations
    async def create_comment(self, comment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new comment"""
        try:
            comment_data["id"] = str(uuid.uuid4())
            comment_data["created_at"] = datetime.now().isoformat()
            comment_data["updated_at"] = datetime.now().isoformat()
            
            result = self.client.table("comments").insert(comment_data).execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Error creating comment: {e}")
            raise
    
    async def get_project_comments(self, project_id: str) -> List[Dict[str, Any]]:
        """Get comments for a project"""
        try:
            result = self.client.table("comments").select("*, users(full_name, avatar_url)").eq("project_id", project_id).order("created_at", desc=True).execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting project comments: {e}")
            raise
    
    # Ratings Operations
    async def create_or_update_rating(self, rating_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create or update rating"""
        try:
            # Check if rating exists
            existing = self.client.table("ratings").select("*").eq("project_id", rating_data["project_id"]).eq("user_id", rating_data["user_id"]).execute()
            
            if existing.data:
                # Update existing rating
                rating_data["updated_at"] = datetime.now().isoformat()
                result = self.client.table("ratings").update(rating_data).eq("project_id", rating_data["project_id"]).eq("user_id", rating_data["user_id"]).execute()
                return result.data[0]
            else:
                # Create new rating
                rating_data["id"] = str(uuid.uuid4())
                rating_data["created_at"] = datetime.now().isoformat()
                rating_data["updated_at"] = datetime.now().isoformat()
                result = self.client.table("ratings").insert(rating_data).execute()
                return result.data[0]
                
        except Exception as e:
            logger.error(f"Error creating/updating rating: {e}")
            raise
    
    async def get_project_rating(self, project_id: str) -> Dict[str, Any]:
        """Get project rating statistics"""
        try:
            # Get average rating and count
            result = self.client.rpc("get_project_rating_stats", {"project_id": project_id}).execute()
            return result.data[0] if result.data else {"average_rating": 0, "total_ratings": 0}
        except Exception as e:
            logger.error(f"Error getting project rating: {e}")
            return {"average_rating": 0, "total_ratings": 0}