"""
PayPal Service for VEO7 Video Platform
Handles PayPal payments, subscriptions, and webhooks
"""

import os
import json
import base64
import logging
import uuid
from typing import Dict, Any, Optional
import aiohttp
from datetime import datetime, timedelta
from .supabase_service import SupabaseService

logger = logging.getLogger(__name__)

class PayPalService:
    def __init__(self):
        """Initialize PayPal service"""
        self.client_id = os.getenv("PAYPAL_CLIENT_ID")
        self.client_secret = os.getenv("PAYPAL_CLIENT_SECRET")
        self.merchant_email = os.getenv("PAYPAL_MERCHANT_EMAIL", "hmhhmhhmh55@gmail.com")
        self.environment = os.getenv("PAYPAL_ENVIRONMENT", "sandbox")  # Default to sandbox for safety
        
        # Check if using demo credentials
        self.is_demo_mode = (
            self.client_id == "demo_client_id" or 
            self.client_secret == "demo_client_secret" or
            not self.client_id or 
            not self.client_secret
        )
        
        if self.is_demo_mode:
            logger.warning("PayPal service running in demo mode - payments will not work")
        elif not self.client_id or not self.client_secret:
            raise ValueError("PayPal credentials must be provided")
        
        # Set API URLs based on environment
        if self.environment == "live":
            self.base_url = "https://api-m.paypal.com"
            self.web_url = "https://www.paypal.com"
        else:
            self.base_url = "https://api-m.sandbox.paypal.com"
            self.web_url = "https://www.sandbox.paypal.com"
        
        self.supabase_service = SupabaseService()
        self._access_token = None
        self._token_expires_at = None
    
    async def health_check(self) -> str:
        """Check PayPal API health"""
        try:
            if self.is_demo_mode:
                return "demo_mode"
            
            token = await self._get_access_token()
            return "healthy" if token else "unhealthy"
        except Exception as e:
            logger.error(f"PayPal health check failed: {e}")
            return "unhealthy"
    
    async def _get_access_token(self) -> str:
        """Get PayPal access token"""
        try:
            if self.is_demo_mode:
                return "demo_token"
                
            # Check if current token is still valid
            if (self._access_token and self._token_expires_at and 
                datetime.now() < self._token_expires_at):
                return self._access_token
            
            # Get new token
            auth_string = f"{self.client_id}:{self.client_secret}"
            auth_bytes = auth_string.encode('ascii')
            auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
            
            headers = {
                'Authorization': f'Basic {auth_b64}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = 'grant_type=client_credentials'
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/v1/oauth2/token",
                    headers=headers,
                    data=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        self._access_token = result['access_token']
                        # Set expiration time (subtract 5 minutes for safety)
                        expires_in = result.get('expires_in', 3600)
                        self._token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)
                        return self._access_token
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to get PayPal token: {error_text}")
                        raise Exception("Failed to authenticate with PayPal")
                        
        except Exception as e:
            logger.error(f"Error getting PayPal access token: {e}")
            raise
    
    async def create_payment(self, plan: Dict[str, Any], user_id: str) -> str:
        """Create PayPal payment"""
        try:
            token = await self._get_access_token()
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # Determine if it's a subscription or one-time payment
            if plan['type'] == 'subscription':
                return await self._create_subscription(plan, user_id, headers)
            else:
                return await self._create_one_time_payment(plan, user_id, headers)
                
        except Exception as e:
            logger.error(f"Error creating PayPal payment: {e}")
            raise
    
    async def _create_one_time_payment(self, plan: Dict[str, Any], user_id: str, headers: Dict[str, str]) -> str:
        """Create one-time payment for coins"""
        try:
            payment_data = {
                "intent": "CAPTURE",
                "purchase_units": [{
                    "amount": {
                        "currency_code": "USD",
                        "value": str(plan['price'])
                    },
                    "description": plan['description'],
                    "custom_id": f"user_{user_id}_plan_{plan['id']}"
                }],
                "payment_source": {
                    "paypal": {
                        "experience_context": {
                            "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED",
                            "brand_name": "VideoGeneratorSite",
                            "locale": "en-US",
                            "landing_page": "LOGIN",
                            "shipping_preference": "NO_SHIPPING",
                            "user_action": "PAY_NOW",
                            "return_url": f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/payment/success",
                            "cancel_url": f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/payment/cancel"
                        }
                    }
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/v2/checkout/orders",
                    headers=headers,
                    json=payment_data
                ) as response:
                    if response.status == 201:
                        result = await response.json()
                        
                        # Find approval URL
                        approval_url = None
                        for link in result.get('links', []):
                            if link['rel'] == 'approve':
                                approval_url = link['href']
                                break
                        
                        if approval_url:
                            # Store payment info in database
                            await self._store_payment_info(result['id'], user_id, plan, 'one_time')
                            return approval_url
                        else:
                            raise Exception("No approval URL found in PayPal response")
                    else:
                        error_text = await response.text()
                        logger.error(f"PayPal payment creation failed: {error_text}")
                        raise Exception("Failed to create PayPal payment")
                        
        except Exception as e:
            logger.error(f"Error creating one-time payment: {e}")
            raise
    
    async def _create_subscription(self, plan: Dict[str, Any], user_id: str, headers: Dict[str, str]) -> str:
        """Create subscription payment"""
        try:
            # First, create or get the subscription plan in PayPal
            paypal_plan_id = await self._get_or_create_paypal_plan(plan, headers)
            
            subscription_data = {
                "plan_id": paypal_plan_id,
                "subscriber": {
                    "name": {
                        "given_name": "User",
                        "surname": f"ID_{user_id}"
                    }
                },
                "application_context": {
                    "brand_name": "VideoGeneratorSite",
                    "locale": "en-US",
                    "shipping_preference": "NO_SHIPPING",
                    "user_action": "SUBSCRIBE_NOW",
                    "payment_method": {
                        "payer_selected": "PAYPAL",
                        "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
                    },
                    "return_url": f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/payment/success",
                    "cancel_url": f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/payment/cancel"
                },
                "custom_id": f"user_{user_id}_plan_{plan['id']}"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/v1/billing/subscriptions",
                    headers=headers,
                    json=subscription_data
                ) as response:
                    if response.status == 201:
                        result = await response.json()
                        
                        # Find approval URL
                        approval_url = None
                        for link in result.get('links', []):
                            if link['rel'] == 'approve':
                                approval_url = link['href']
                                break
                        
                        if approval_url:
                            # Store subscription info in database
                            await self._store_payment_info(result['id'], user_id, plan, 'subscription')
                            return approval_url
                        else:
                            raise Exception("No approval URL found in PayPal response")
                    else:
                        error_text = await response.text()
                        logger.error(f"PayPal subscription creation failed: {error_text}")
                        raise Exception("Failed to create PayPal subscription")
                        
        except Exception as e:
            logger.error(f"Error creating subscription: {e}")
            raise
    
    async def _get_or_create_paypal_plan(self, plan: Dict[str, Any], headers: Dict[str, str]) -> str:
        """Get or create PayPal billing plan"""
        try:
            # Check if plan already exists in PayPal
            # For simplicity, we'll create a new plan each time
            # In production, you might want to cache plan IDs
            
            plan_data = {
                "product_id": await self._get_or_create_paypal_product(headers),
                "name": plan['name'],
                "description": plan['description'],
                "status": "ACTIVE",
                "billing_cycles": [{
                    "frequency": {
                        "interval_unit": "MONTH" if plan['billing_cycle'] == 'monthly' else "YEAR",
                        "interval_count": 1
                    },
                    "tenure_type": "REGULAR",
                    "sequence": 1,
                    "total_cycles": 0,  # Infinite
                    "pricing_scheme": {
                        "fixed_price": {
                            "value": str(plan['price']),
                            "currency_code": "USD"
                        }
                    }
                }],
                "payment_preferences": {
                    "auto_bill_outstanding": True,
                    "setup_fee": {
                        "value": "0",
                        "currency_code": "USD"
                    },
                    "setup_fee_failure_action": "CONTINUE",
                    "payment_failure_threshold": 3
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/v1/billing/plans",
                    headers=headers,
                    json=plan_data
                ) as response:
                    if response.status == 201:
                        result = await response.json()
                        return result['id']
                    else:
                        error_text = await response.text()
                        logger.error(f"PayPal plan creation failed: {error_text}")
                        raise Exception("Failed to create PayPal plan")
                        
        except Exception as e:
            logger.error(f"Error creating PayPal plan: {e}")
            raise
    
    async def _get_or_create_paypal_product(self, headers: Dict[str, str]) -> str:
        """Get or create PayPal product"""
        try:
            product_data = {
                "name": "VEO7 Video Generation Services",
                "description": "AI-powered video generation platform services",
                "type": "SERVICE",
                "category": "SOFTWARE"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/v1/catalogs/products",
                    headers=headers,
                    json=product_data
                ) as response:
                    if response.status == 201:
                        result = await response.json()
                        return result['id']
                    else:
                        error_text = await response.text()
                        logger.error(f"PayPal product creation failed: {error_text}")
                        raise Exception("Failed to create PayPal product")
                        
        except Exception as e:
            logger.error(f"Error creating PayPal product: {e}")
            raise
    
    async def _store_payment_info(self, paypal_id: str, user_id: str, plan: Dict[str, Any], payment_type: str):
        """Store payment information in database"""
        try:
            if payment_type == 'subscription':
                # Store subscription
                subscription_data = {
                    "user_id": user_id,
                    "plan_id": plan['id'],
                    "paypal_subscription_id": paypal_id,
                    "status": "pending",
                    "start_date": datetime.now().isoformat(),
                    "next_billing_date": (datetime.now() + timedelta(days=30 if plan['billing_cycle'] == 'monthly' else 365)).isoformat()
                }
                await self.supabase_service.create_subscription(subscription_data)
            else:
                # Store one-time payment info (you might want a separate table for this)
                pass
                
        except Exception as e:
            logger.error(f"Error storing payment info: {e}")
            raise
    
    async def handle_webhook(self, webhook_data: Dict[str, Any]):
        """Handle PayPal webhooks"""
        try:
            event_type = webhook_data.get('event_type')
            resource = webhook_data.get('resource', {})
            
            logger.info(f"Received PayPal webhook: {event_type}")
            
            if event_type == 'PAYMENT.CAPTURE.COMPLETED':
                await self._handle_payment_completed(resource)
            elif event_type == 'BILLING.SUBSCRIPTION.ACTIVATED':
                await self._handle_subscription_activated(resource)
            elif event_type == 'BILLING.SUBSCRIPTION.CANCELLED':
                await self._handle_subscription_cancelled(resource)
            elif event_type == 'BILLING.SUBSCRIPTION.PAYMENT.COMPLETED':
                await self._handle_subscription_payment_completed(resource)
            else:
                logger.info(f"Unhandled webhook event: {event_type}")
                
        except Exception as e:
            logger.error(f"Error handling PayPal webhook: {e}")
            raise
    
    async def _handle_payment_completed(self, resource: Dict[str, Any]):
        """Handle completed one-time payment"""
        try:
            custom_id = resource.get('custom_id', '')
            amount = float(resource.get('amount', {}).get('value', 0))
            
            # Extract user_id and plan_id from custom_id
            if custom_id.startswith('user_'):
                parts = custom_id.split('_')
                if len(parts) >= 4:
                    user_id = parts[1]
                    plan_id = parts[3]
                    
                    # Get plan details
                    plan = await self.supabase_service.get_plan(plan_id)
                    if plan and plan['type'] == 'coins':
                        # Add coins to user account
                        await self.supabase_service.add_user_coins(
                            user_id, 
                            plan['coins'], 
                            'purchase', 
                            f"Purchased {plan['coins']} coins via PayPal"
                        )
                        logger.info(f"Added {plan['coins']} coins to user {user_id}")
                        
        except Exception as e:
            logger.error(f"Error handling payment completed: {e}")
            raise
    
    async def _handle_subscription_activated(self, resource: Dict[str, Any]):
        """Handle subscription activation"""
        try:
            subscription_id = resource.get('id')
            custom_id = resource.get('custom_id', '')
            
            # Extract user_id from custom_id
            if custom_id.startswith('user_'):
                parts = custom_id.split('_')
                if len(parts) >= 2:
                    user_id = parts[1]
                    
                    # Update subscription status
                    await self.supabase_service.update_subscription(subscription_id, {
                        "status": "active",
                        "activated_at": datetime.now().isoformat()
                    })
                    
                    logger.info(f"Activated subscription {subscription_id} for user {user_id}")
                    
        except Exception as e:
            logger.error(f"Error handling subscription activated: {e}")
            raise
    
    async def _handle_subscription_cancelled(self, resource: Dict[str, Any]):
        """Handle subscription cancellation"""
        try:
            subscription_id = resource.get('id')
            
            # Update subscription status
            await self.supabase_service.update_subscription(subscription_id, {
                "status": "cancelled",
                "cancelled_at": datetime.now().isoformat()
            })
            
            logger.info(f"Cancelled subscription {subscription_id}")
            
        except Exception as e:
            logger.error(f"Error handling subscription cancelled: {e}")
            raise
    
    async def _handle_subscription_payment_completed(self, resource: Dict[str, Any]):
        """Handle subscription payment completion"""
        try:
            subscription_id = resource.get('billing_agreement_id')
            amount = float(resource.get('amount', {}).get('total', 0))
            
            # Get subscription details
            subscription = await self.supabase_service.get_user_subscription(subscription_id)
            if subscription:
                plan = subscription.get('plans')
                if plan and plan['type'] == 'subscription':
                    # Add monthly/yearly coins
                    await self.supabase_service.add_user_coins(
                        subscription['user_id'],
                        plan['coins'],
                        'subscription',
                        f"Monthly/Yearly subscription coins: {plan['name']}"
                    )
                    
                    # Update next billing date
                    next_billing = datetime.now() + timedelta(
                        days=30 if plan['billing_cycle'] == 'monthly' else 365
                    )
                    await self.supabase_service.update_subscription(subscription_id, {
                        "next_billing_date": next_billing.isoformat(),
                        "last_payment_date": datetime.now().isoformat()
                    })
                    
                    logger.info(f"Processed subscription payment for {subscription['user_id']}")
                    
        except Exception as e:
            logger.error(f"Error handling subscription payment: {e}")
            raise
    
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create PayPal product for subscription plans"""
        try:
            token = await self._get_access_token()
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'PayPal-Request-Id': f"product-{uuid.uuid4()}"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/v1/catalogs/products",
                    headers=headers,
                    json=product_data
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        logger.info(f"Created PayPal product: {result.get('id')}")
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to create PayPal product: {error_text}")
                        return {}
                        
        except Exception as e:
            logger.error(f"Error creating PayPal product: {e}")
            return {}
    
    async def create_billing_plan(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create PayPal billing plan for subscriptions"""
        try:
            token = await self._get_access_token()
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'PayPal-Request-Id': f"plan-{uuid.uuid4()}"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/v1/billing/plans",
                    headers=headers,
                    json=plan_data
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        logger.info(f"Created PayPal billing plan: {result.get('id')}")
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to create PayPal billing plan: {error_text}")
                        return {}
                        
        except Exception as e:
            logger.error(f"Error creating PayPal billing plan: {e}")
            return {}
    
    async def create_subscription(self, plan_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create PayPal subscription"""
        try:
            token = await self._get_access_token()
            
            subscription_data = {
                "plan_id": plan_id,
                "start_time": (datetime.now() + timedelta(minutes=1)).isoformat() + "Z",
                "subscriber": {
                    "name": {
                        "given_name": user_data.get("first_name", "User"),
                        "surname": user_data.get("last_name", "VEO7")
                    },
                    "email_address": user_data.get("email", "user@veo7.com")
                },
                "application_context": {
                    "brand_name": "VEO7 Video Platform",
                    "locale": "en-US",
                    "shipping_preference": "NO_SHIPPING",
                    "user_action": "SUBSCRIBE_NOW",
                    "payment_method": {
                        "payer_selected": "PAYPAL",
                        "payee_preferred": "IMMEDIATE_PAYMENT_REQUIRED"
                    },
                    "return_url": f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/subscription/success",
                    "cancel_url": f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/subscription/cancel"
                }
            }
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'PayPal-Request-Id': f"subscription-{uuid.uuid4()}"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/v1/billing/subscriptions",
                    headers=headers,
                    json=subscription_data
                ) as response:
                    if response.status in [200, 201]:
                        result = await response.json()
                        logger.info(f"Created PayPal subscription: {result.get('id')}")
                        return result
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to create PayPal subscription: {error_text}")
                        return {}
                        
        except Exception as e:
            logger.error(f"Error creating PayPal subscription: {e}")
            return {}