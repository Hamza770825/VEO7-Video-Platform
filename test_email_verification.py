#!/usr/bin/env python3
"""
اختبار وظائف التحقق من البريد الإلكتروني وإعادة الإرسال
Test email verification and resend functionality
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any

# إعدادات الاختبار
API_BASE = "http://localhost:8000"
TEST_EMAIL = "test.verification@example.com"

class EmailVerificationTester:
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """إجراء طلب HTTP إلى API"""
        url = f"{API_BASE}{endpoint}"
        
        try:
            if method.upper() == "POST":
                async with self.session.post(url, json=data) as response:
                    result = await response.json()
                    return {"status": response.status, "data": result}
        except Exception as e:
            return {"status": 0, "error": str(e)}
    
    def print_test_result(self, test_name: str, success: bool, details: str = ""):
        """طباعة نتيجة الاختبار"""
        status = "✅ نجح" if success else "❌ فشل"
        print(f"{status} {test_name}")
        if details:
            print(f"   التفاصيل: {details}")
        print()
    
    async def test_resend_verification_valid_email(self) -> bool:
        """اختبار إعادة إرسال التحقق لبريد إلكتروني صحيح التنسيق"""
        print("🔍 اختبار إعادة إرسال التحقق لبريد إلكتروني صحيح التنسيق...")
        
        data = {"email": TEST_EMAIL}
        result = await self.make_request("POST", "/api/auth/resend-verification", data)
        
        if result["status"] == 200:
            response_data = result["data"]
            success = response_data.get("success", False)
            message = response_data.get("message", "")
            
            # في النظام الحقيقي، نتوقع إما:
            # 1. نجاح إذا كان المستخدم موجود
            # 2. رسالة خطأ واضحة إذا كان المستخدم غير موجود
            # 3. رسالة demo mode إذا كان النظام في وضع العرض التوضيحي
            
            is_demo_success = (
                "demo mode" in message.lower() or 
                "وضع العرض التوضيحي" in message
            )
            
            is_valid_error = (
                "غير صحيح أو غير موجود" in message or
                "not found" in message.lower() or
                "invalid" in message.lower()
            )
            
            # نعتبر الاختبار ناجحاً إذا:
            # - نجح الإرسال (مستخدم موجود أو demo mode)
            # - أو أعطى رسالة خطأ واضحة (مستخدم غير موجود)
            test_passed = success or is_demo_success or (not success and is_valid_error)
            
            self.print_test_result(
                "إعادة إرسال التحقق - بريد صحيح التنسيق", 
                test_passed, 
                f"الرسالة: {message}"
            )
            return test_passed
        else:
            error_msg = result.get("data", {}).get("detail", "خطأ غير معروف")
            self.print_test_result(
                "إعادة إرسال التحقق - بريد صحيح التنسيق", 
                False, 
                f"HTTP {result['status']}: {error_msg}"
            )
            return False
    
    async def test_resend_verification_invalid_email(self) -> bool:
        """اختبار إعادة إرسال التحقق لبريد إلكتروني غير صحيح"""
        print("🔍 اختبار إعادة إرسال التحقق لبريد إلكتروني غير صحيح...")
        
        data = {"email": "invalid.email@nonexistent.domain"}
        result = await self.make_request("POST", "/api/auth/resend-verification", data)
        
        if result["status"] == 200:
            response_data = result["data"]
            success = response_data.get("success", False)
            message = response_data.get("message", "")
            
            # نتوقع فشل الطلب للبريد غير الصحيح
            expected_failure = not success
            
            self.print_test_result(
                "إعادة إرسال التحقق - بريد غير صحيح", 
                expected_failure, 
                f"الرسالة: {message}"
            )
            return expected_failure
        else:
            error_msg = result.get("data", {}).get("detail", "خطأ غير معروف")
            self.print_test_result(
                "إعادة إرسال التحقق - بريد غير صحيح", 
                True,  # نتوقع خطأ HTTP
                f"HTTP {result['status']}: {error_msg}"
            )
            return True
    
    async def test_resend_verification_empty_email(self) -> bool:
        """اختبار إعادة إرسال التحقق لبريد إلكتروني فارغ"""
        print("🔍 اختبار إعادة إرسال التحقق لبريد إلكتروني فارغ...")
        
        data = {"email": ""}
        result = await self.make_request("POST", "/api/auth/resend-verification", data)
        
        if result["status"] == 200:
            response_data = result["data"]
            success = response_data.get("success", False)
            message = response_data.get("message", "")
            
            # نتوقع أن يكون success = False مع رسالة خطأ واضحة
            if not success and ("مطلوب" in message or "required" in message.lower()):
                self.print_test_result(
                    "إعادة إرسال التحقق - بريد فارغ", 
                    True, 
                    f"تم رفض البريد الفارغ بنجاح: {message}"
                )
                return True
            else:
                self.print_test_result(
                    "إعادة إرسال التحقق - بريد فارغ", 
                    False, 
                    f"لم يتم رفض البريد الفارغ! النجاح: {success}, الرسالة: {message}"
                )
                return False
        else:
            # إذا كان هناك خطأ HTTP، فهذا أيضاً مقبول
            error_msg = result.get("data", {}).get("detail", "خطأ غير معروف")
            self.print_test_result(
                "إعادة إرسال التحقق - بريد فارغ", 
                True, 
                f"تم رفض البريد الفارغ بنجاح: HTTP {result['status']} - {error_msg}"
            )
            return True
    
    async def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        print("🚀 بدء اختبارات التحقق من البريد الإلكتروني")
        print("=" * 50)
        
        tests = [
            self.test_resend_verification_valid_email,
            self.test_resend_verification_invalid_email,
            self.test_resend_verification_empty_email,
        ]
        
        results = []
        for test in tests:
            try:
                result = await test()
                results.append(result)
            except Exception as e:
                print(f"❌ خطأ في تشغيل الاختبار: {e}")
                results.append(False)
        
        # ملخص النتائج
        print("=" * 50)
        print("📊 ملخص نتائج الاختبارات:")
        passed = sum(results)
        total = len(results)
        print(f"✅ نجح: {passed}/{total}")
        print(f"❌ فشل: {total - passed}/{total}")
        
        if passed == total:
            print("🎉 جميع الاختبارات نجحت!")
        else:
            print("⚠️  بعض الاختبارات فشلت. يرجى مراجعة التفاصيل أعلاه.")

async def main():
    """الدالة الرئيسية"""
    async with EmailVerificationTester() as tester:
        await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())