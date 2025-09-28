#!/usr/bin/env python3
"""
VEO7 Authentication Testing Script
Tests all authentication endpoints and functionality
"""

import asyncio
import aiohttp
import json
import sys
from datetime import datetime
from typing import Dict, Any

# API Base URL
API_BASE = "http://localhost:8000"

class AuthTester:
    def __init__(self):
        self.session = None
        self.test_user_email = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com"
        self.test_user_password = "TestPassword123!"
        self.test_user_name = "Test User"
        self.user_id = None
        self.access_token = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None) -> Dict:
        """Make HTTP request to API"""
        url = f"{API_BASE}{endpoint}"
        
        try:
            if method.upper() == "GET":
                async with self.session.get(url, headers=headers) as response:
                    result = await response.json()
                    return {"status": response.status, "data": result}
            elif method.upper() == "POST":
                async with self.session.post(url, json=data, headers=headers) as response:
                    result = await response.json()
                    return {"status": response.status, "data": result}
            elif method.upper() == "PUT":
                async with self.session.put(url, json=data, headers=headers) as response:
                    result = await response.json()
                    return {"status": response.status, "data": result}
        except Exception as e:
            return {"status": 0, "error": str(e)}
    
    def print_test_result(self, test_name: str, success: bool, details: str = ""):
        """Print formatted test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   📝 {details}")
        print()
    
    async def test_health_check(self) -> bool:
        """Test API health check"""
        print("🔍 Testing API Health Check...")
        
        result = await self.make_request("GET", "/health")
        
        if result["status"] == 200:
            data = result["data"]
            success = data.get("status") in ["healthy", "degraded"]
            details = f"Status: {data.get('status')}, Database: {data.get('services', {}).get('database', 'unknown')}"
            self.print_test_result("Health Check", success, details)
            return success
        else:
            self.print_test_result("Health Check", False, f"HTTP {result['status']}")
            return False
    
    async def test_user_registration(self) -> bool:
        """Test user registration"""
        print("🔍 Testing User Registration...")
        
        data = {
            "email": self.test_user_email,
            "password": self.test_user_password,
            "full_name": self.test_user_name
        }
        
        result = await self.make_request("POST", "/api/auth/register", data)
        
        if result["status"] == 200:
            response_data = result["data"]
            success = response_data.get("success", False)
            
            if success and "user" in response_data:
                user_data = response_data["user"]
                self.user_id = user_data.get("id")
                details = f"User ID: {self.user_id}, Email confirmed: {user_data.get('email_confirmed', False)}"
            else:
                details = f"Response: {response_data}"
            
            self.print_test_result("User Registration", success, details)
            return success
        else:
            error_msg = result.get("data", {}).get("detail", "Unknown error")
            self.print_test_result("User Registration", False, f"HTTP {result['status']}: {error_msg}")
            return False
    
    async def test_user_login(self) -> bool:
        """Test user login"""
        print("🔍 Testing User Login...")
        
        data = {
            "email": self.test_user_email,
            "password": self.test_user_password
        }
        
        result = await self.make_request("POST", "/api/auth/login", data)
        
        if result["status"] == 200:
            response_data = result["data"]
            success = response_data.get("success", False)
            
            if success and "session" in response_data:
                session_data = response_data["session"]
                self.access_token = session_data.get("access_token")
                details = f"Access token received: {bool(self.access_token)}"
            else:
                details = f"Response: {response_data}"
            
            self.print_test_result("User Login", success, details)
            return success
        else:
            error_msg = result.get("data", {}).get("detail", "Unknown error")
            self.print_test_result("User Login", False, f"HTTP {result['status']}: {error_msg}")
            return False
    
    async def test_get_user_profile(self) -> bool:
        """Test getting user profile"""
        print("🔍 Testing Get User Profile...")
        
        if not self.user_id:
            self.print_test_result("Get User Profile", False, "No user ID available")
            return False
        
        headers = {}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        result = await self.make_request("GET", f"/api/auth/profile/{self.user_id}", headers=headers)
        
        if result["status"] == 200:
            response_data = result["data"]
            success = response_data.get("success", False)
            
            if success and "profile" in response_data:
                profile = response_data["profile"]
                details = f"Profile loaded: {profile.get('full_name', 'Unknown')}"
            else:
                details = f"Response: {response_data}"
            
            self.print_test_result("Get User Profile", success, details)
            return success
        else:
            error_msg = result.get("data", {}).get("detail", "Unknown error")
            self.print_test_result("Get User Profile", False, f"HTTP {result['status']}: {error_msg}")
            return False
    
    async def test_update_user_profile(self) -> bool:
        """Test updating user profile"""
        print("🔍 Testing Update User Profile...")
        
        if not self.user_id:
            self.print_test_result("Update User Profile", False, "No user ID available")
            return False
        
        data = {
            "full_name": f"{self.test_user_name} Updated"
        }
        
        headers = {}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        result = await self.make_request("PUT", f"/api/auth/profile/{self.user_id}", data, headers)
        
        if result["status"] == 200:
            response_data = result["data"]
            success = response_data.get("success", False)
            details = f"Profile updated: {success}"
            
            self.print_test_result("Update User Profile", success, details)
            return success
        else:
            error_msg = result.get("data", {}).get("detail", "Unknown error")
            self.print_test_result("Update User Profile", False, f"HTTP {result['status']}: {error_msg}")
            return False
    
    async def test_resend_verification(self) -> bool:
        """Test resending verification email"""
        print("🔍 Testing Resend Verification Email...")
        
        data = {
            "email": self.test_user_email
        }
        
        result = await self.make_request("POST", "/api/auth/resend-verification", data)
        
        if result["status"] == 200:
            response_data = result["data"]
            success = response_data.get("success", False)
            details = f"Verification email sent: {success}"
            
            self.print_test_result("Resend Verification Email", success, details)
            return success
        else:
            error_msg = result.get("data", {}).get("detail", "Unknown error")
            self.print_test_result("Resend Verification Email", False, f"HTTP {result['status']}: {error_msg}")
            return False
    
    async def test_user_stats(self) -> bool:
        """Test getting user statistics"""
        print("🔍 Testing Get User Stats...")
        
        if not self.user_id:
            self.print_test_result("Get User Stats", False, "No user ID available")
            return False
        
        headers = {}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        result = await self.make_request("GET", f"/api/stats/user/{self.user_id}", headers=headers)
        
        if result["status"] == 200:
            response_data = result["data"]
            success = response_data.get("success", False)
            
            if success and "stats" in response_data:
                stats = response_data["stats"]
                details = f"Stats loaded: {len(stats)} fields"
            else:
                details = f"Response: {response_data}"
            
            self.print_test_result("Get User Stats", success, details)
            return success
        else:
            error_msg = result.get("data", {}).get("detail", "Unknown error")
            self.print_test_result("Get User Stats", False, f"HTTP {result['status']}: {error_msg}")
            return False
    
    async def run_all_tests(self):
        """Run all authentication tests"""
        print("🚀 VEO7 Authentication Testing")
        print("=" * 50)
        print(f"📧 Test Email: {self.test_user_email}")
        print(f"🔑 Test Password: {self.test_user_password}")
        print("=" * 50)
        print()
        
        tests = [
            ("API Health Check", self.test_health_check),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Get User Profile", self.test_get_user_profile),
            ("Update User Profile", self.test_update_user_profile),
            ("Resend Verification", self.test_resend_verification),
            ("Get User Stats", self.test_user_stats),
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                result = await test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ FAIL {test_name}")
                print(f"   🚨 Exception: {str(e)}")
                print()
                results.append((test_name, False))
        
        # Summary
        print("📊 Test Summary")
        print("=" * 50)
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print("=" * 50)
        print(f"📈 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! Authentication system is working correctly.")
        else:
            print("⚠️ Some tests failed. Please check the issues above.")
            
            if passed == 0:
                print("💡 Tip: Make sure the backend server is running and Supabase is configured correctly.")
                print("📖 Check SUPABASE_SETUP_GUIDE.md for setup instructions.")

async def main():
    """Main function"""
    try:
        async with AuthTester() as tester:
            await tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n⏹️ Testing interrupted by user")
    except Exception as e:
        print(f"\n🚨 Testing failed with error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())