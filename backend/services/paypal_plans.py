"""
PayPal Plans Configuration for VEO7 Video Platform
Defines subscription plans and pricing for the platform
"""

import os
import json
import logging
from typing import Dict, List, Any
from .paypal_service import PayPalService

logger = logging.getLogger(__name__)

class PayPalPlansManager:
    def __init__(self, paypal_service: PayPalService):
        """Initialize PayPal Plans Manager"""
        self.paypal_service = paypal_service
        self.plans = self._define_plans()
    
    def _define_plans(self) -> Dict[str, Dict[str, Any]]:
        """Define subscription plans for VEO7 platform"""
        return {
            "basic": {
                "name": "VEO7 Basic Plan",
                "description": "خطة أساسية لتوليد الفيديوهات - 10 فيديوهات شهرياً",
                "price": "9.99",
                "currency": "USD",
                "interval": "MONTH",
                "interval_count": 1,
                "features": [
                    "10 فيديوهات شهرياً",
                    "جودة HD",
                    "دعم فني أساسي",
                    "تخزين 1GB"
                ],
                "video_limit": 10,
                "storage_limit": "1GB",
                "priority": "normal"
            },
            "pro": {
                "name": "VEO7 Pro Plan",
                "description": "خطة احترافية لتوليد الفيديوهات - 50 فيديو شهرياً",
                "price": "29.99",
                "currency": "USD",
                "interval": "MONTH",
                "interval_count": 1,
                "features": [
                    "50 فيديو شهرياً",
                    "جودة 4K",
                    "نماذج AI متقدمة",
                    "دعم فني متقدم",
                    "تخزين 10GB",
                    "أولوية في المعالجة"
                ],
                "video_limit": 50,
                "storage_limit": "10GB",
                "priority": "high",
                "ai_models": ["sadtalker", "wav2lip"]
            },
            "enterprise": {
                "name": "VEO7 Enterprise Plan",
                "description": "خطة المؤسسات - فيديوهات غير محدودة",
                "price": "99.99",
                "currency": "USD",
                "interval": "MONTH",
                "interval_count": 1,
                "features": [
                    "فيديوهات غير محدودة",
                    "جودة 8K",
                    "جميع نماذج AI",
                    "دعم فني مخصص 24/7",
                    "تخزين 100GB",
                    "أولوية قصوى",
                    "API مخصص",
                    "تقارير تحليلية"
                ],
                "video_limit": -1,  # Unlimited
                "storage_limit": "100GB",
                "priority": "highest",
                "ai_models": ["sadtalker", "wav2lip", "custom"],
                "api_access": True,
                "analytics": True
            }
        }
    
    async def create_paypal_plans(self) -> Dict[str, Dict[str, Any]]:
        """Create PayPal subscription plans"""
        # For demonstration purposes, return mock plan IDs
        # In production with valid PayPal credentials, this will create actual plans
        created_plans = {}
        
        # Check if PayPal service is properly configured
        if not self.paypal_service.client_id or not self.paypal_service.client_secret:
            logger.warning("PayPal credentials not configured. Returning mock plans.")
            return self._create_mock_plans()
        
        for plan_id, plan_data in self.plans.items():
            try:
                # Create product first
                product_data = {
                    "name": plan_data["name"],
                    "description": plan_data["description"],
                    "type": "SERVICE",
                    "category": "SOFTWARE"
                }
                
                product = await self.paypal_service.create_product(product_data)
                
                if product and "id" in product:
                    # Create billing plan
                    billing_plan_data = {
                        "product_id": product["id"],
                        "name": plan_data["name"],
                        "description": plan_data["description"],
                        "billing_cycles": [
                            {
                                "frequency": {
                                    "interval_unit": plan_data["interval"],
                                    "interval_count": plan_data["interval_count"]
                                },
                                "tenure_type": "REGULAR",
                                "sequence": 1,
                                "total_cycles": 0,  # Infinite
                                "pricing_scheme": {
                                    "fixed_price": {
                                        "value": plan_data["price"],
                                        "currency_code": plan_data["currency"]
                                    }
                                }
                            }
                        ],
                        "payment_preferences": {
                            "auto_bill_outstanding": True,
                            "setup_fee": {
                                "value": "0",
                                "currency_code": plan_data["currency"]
                            },
                            "setup_fee_failure_action": "CONTINUE",
                            "payment_failure_threshold": 3
                        },
                        "taxes": {
                            "percentage": "0",
                            "inclusive": False
                        }
                    }
                    
                    billing_plan = await self.paypal_service.create_billing_plan(billing_plan_data)
                    
                    if billing_plan and "id" in billing_plan:
                        created_plans[plan_id] = {
                            "product_id": product["id"],
                            "plan_id": billing_plan["id"],
                            "plan_data": plan_data,
                            "status": "active"
                        }
                        logger.info(f"Successfully created PayPal plan for {plan_id}")
                    else:
                        logger.error(f"Failed to create billing plan for {plan_id}")
                        # Fall back to mock plan
                        created_plans[plan_id] = self._create_mock_plan(plan_id, plan_data)
                else:
                    logger.error(f"Failed to create product for {plan_id}")
                    # Fall back to mock plan
                    created_plans[plan_id] = self._create_mock_plan(plan_id, plan_data)
                    
            except Exception as e:
                logger.error(f"Error creating PayPal plan {plan_id}: {e}")
                # Fall back to mock plan
                created_plans[plan_id] = self._create_mock_plan(plan_id, plan_data)
        
        return created_plans
    
    def _create_mock_plans(self) -> Dict[str, Dict[str, Any]]:
        """Create mock plans for demonstration"""
        mock_plans = {}
        for plan_id, plan_data in self.plans.items():
            mock_plans[plan_id] = self._create_mock_plan(plan_id, plan_data)
        return mock_plans
    
    def _create_mock_plan(self, plan_id: str, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a single mock plan"""
        import uuid
        return {
            "product_id": f"PROD-{uuid.uuid4().hex[:8].upper()}",
            "plan_id": f"P-{uuid.uuid4().hex[:8].upper()}",
            "plan_data": plan_data,
            "status": "mock",
            "note": "This is a mock plan. Configure valid PayPal credentials to create real plans."
        }
    
    def get_plan_details(self, plan_id: str) -> Dict[str, Any]:
        """Get plan details by plan ID"""
        return self.plans.get(plan_id, {})
    
    def get_all_plans(self) -> Dict[str, Dict[str, Any]]:
        """Get all available plans"""
        return self.plans
    
    def validate_plan_limits(self, plan_id: str, current_usage: Dict[str, Any]) -> Dict[str, bool]:
        """Validate if user is within plan limits"""
        plan = self.plans.get(plan_id, {})
        if not plan:
            return {"valid": False, "reason": "Invalid plan"}
        
        validation = {"valid": True}
        
        # Check video limit
        video_limit = plan.get("video_limit", 0)
        if video_limit > 0:  # -1 means unlimited
            current_videos = current_usage.get("videos_this_month", 0)
            if current_videos >= video_limit:
                validation["valid"] = False
                validation["video_limit_exceeded"] = True
        
        # Check storage limit
        storage_limit = plan.get("storage_limit", "0GB")
        current_storage = current_usage.get("storage_used", "0GB")
        # Add storage validation logic here
        
        return validation
    
    async def upgrade_plan(self, user_id: str, current_plan: str, new_plan: str) -> Dict[str, Any]:
        """Handle plan upgrade"""
        try:
            current_plan_data = self.plans.get(current_plan, {})
            new_plan_data = self.plans.get(new_plan, {})
            
            if not current_plan_data or not new_plan_data:
                return {"success": False, "error": "Invalid plan"}
            
            # Calculate prorated amount
            current_price = float(current_plan_data.get("price", "0"))
            new_price = float(new_plan_data.get("price", "0"))
            
            if new_price <= current_price:
                return {"success": False, "error": "Cannot downgrade to lower plan"}
            
            upgrade_data = {
                "user_id": user_id,
                "from_plan": current_plan,
                "to_plan": new_plan,
                "price_difference": new_price - current_price,
                "effective_date": "immediate"
            }
            
            return {"success": True, "upgrade_data": upgrade_data}
            
        except Exception as e:
            logger.error(f"Error upgrading plan: {e}")
            return {"success": False, "error": str(e)}