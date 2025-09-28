#!/usr/bin/env python3
"""
Mock Plans Service
This provides a temporary plans service when the database table doesn't exist
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

class MockPlansService:
    """Mock plans service for testing"""
    
    def __init__(self):
        """Initialize with default plans"""
        self.plans = [
            {
                "id": str(uuid.uuid4()),
                "name": "Free",
                "description": "خطة مجانية للمبتدئين",
                "price": 0.00,
                "currency": "USD",
                "duration_days": 30,
                "features": ["إنشاء 5 فيديوهات شهرياً", "جودة HD", "دعم أساسي"],
                "max_projects": 3,
                "max_videos_per_month": 5,
                "max_storage_gb": 1,
                "is_active": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Basic",
                "description": "خطة أساسية للاستخدام الشخصي",
                "price": 9.99,
                "currency": "USD",
                "duration_days": 30,
                "features": ["إنشاء 25 فيديو شهرياً", "جودة Full HD", "دعم عبر البريد الإلكتروني", "إزالة العلامة المائية"],
                "max_projects": 10,
                "max_videos_per_month": 25,
                "max_storage_gb": 5,
                "is_active": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Pro",
                "description": "خطة احترافية للمبدعين",
                "price": 29.99,
                "currency": "USD",
                "duration_days": 30,
                "features": ["إنشاء 100 فيديو شهرياً", "جودة 4K", "دعم أولوية", "تحليلات متقدمة", "تصدير بصيغ متعددة"],
                "max_projects": 50,
                "max_videos_per_month": 100,
                "max_storage_gb": 20,
                "is_active": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Enterprise",
                "description": "خطة للشركات والمؤسسات",
                "price": 99.99,
                "currency": "USD",
                "duration_days": 30,
                "features": ["فيديوهات غير محدودة", "جودة 4K+", "دعم مخصص 24/7", "API مخصص", "تكامل مع الأنظمة", "تدريب فريق العمل"],
                "max_projects": -1,
                "max_videos_per_month": -1,
                "max_storage_gb": 100,
                "is_active": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
    
    def get_active_plans(self) -> List[Dict[str, Any]]:
        """Get all active plans"""
        return [plan for plan in self.plans if plan["is_active"]]
    
    def get_plan_by_id(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific plan by ID"""
        for plan in self.plans:
            if plan["id"] == plan_id:
                return plan
        return None
    
    def get_plan_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a specific plan by name"""
        for plan in self.plans:
            if plan["name"].lower() == name.lower():
                return plan
        return None

# Global instance
mock_plans_service = MockPlansService()