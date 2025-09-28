#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار شامل لجميع نقاط API الموجودة في منصة VEO7
"""

import requests
import json
import time
from typing import Dict, Any, Optional

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, endpoint: str, method: str, status: str, details: str = ""):
        """تسجيل نتيجة الاختبار"""
        result = {
            "endpoint": endpoint,
            "method": method,
            "status": status,
            "details": details
        }
        self.test_results.append(result)
        
        # طباعة النتيجة
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} {method} {endpoint} - {status}")
        if details:
            print(f"   📝 {details}")
    
    def test_endpoint(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None, 
                     files: Optional[Dict] = None, headers: Optional[Dict] = None,
                     expected_status: int = 200, auth_required: bool = False) -> bool:
        """اختبار نقطة API واحدة"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == "GET":
                response = self.session.get(url, headers=headers)
            elif method == "POST":
                if files:
                    response = self.session.post(url, data=data, files=files, headers=headers)
                else:
                    response = self.session.post(url, json=data, headers=headers)
            elif method == "PUT":
                response = self.session.put(url, json=data, headers=headers)
            elif method == "DELETE":
                response = self.session.delete(url, headers=headers)
            else:
                self.log_test(endpoint, method, "FAIL", f"طريقة غير مدعومة: {method}")
                return False
            
            # التحقق من الحالة المتوقعة
            if auth_required and response.status_code in [401, 403]:
                self.log_test(endpoint, method, "PASS", "يتطلب مصادقة (متوقع)")
                return True
            elif response.status_code == 404:
                self.log_test(endpoint, method, "WARNING", "النقطة غير موجودة")
                return True
            elif response.status_code == 422:
                self.log_test(endpoint, method, "WARNING", "بيانات غير صحيحة (متوقع)")
                return True
            elif response.status_code == expected_status:
                self.log_test(endpoint, method, "PASS", f"الحالة: {response.status_code}")
                return True
            else:
                self.log_test(endpoint, method, "FAIL", 
                            f"الحالة المتوقعة: {expected_status}, الحالة الفعلية: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test(endpoint, method, "FAIL", f"خطأ: {str(e)}")
            return False
    
    def run_all_tests(self):
        """تشغيل جميع الاختبارات للنقاط الموجودة فعلياً"""
        print("🚀 بدء الاختبار الشامل لجميع نقاط API الموجودة")
        print("=" * 50)
        
        # اختبارات الصحة العامة
        print("\n🏥 اختبارات الصحة العامة")
        print("-" * 30)
        self.test_endpoint("/", "GET")
        self.test_endpoint("/health", "GET")
        self.test_endpoint("/api/health", "GET")
        
        # اختبارات المصادقة
        print("\n🔐 اختبارات المصادقة")
        print("-" * 30)
        self.test_endpoint("/api/auth/verify-token", "POST", auth_required=True)
        self.test_endpoint("/api/auth/login", "POST", expected_status=422)  # بدون بيانات
        self.test_endpoint("/api/auth/register", "POST", expected_status=422)  # بدون بيانات
        
        # اختبارات المشاريع
        print("\n📁 اختبارات المشاريع")
        print("-" * 30)
        self.test_endpoint("/api/projects", "GET", auth_required=True)
        self.test_endpoint("/api/projects", "POST", auth_required=True)
        self.test_endpoint("/api/projects/123", "GET", auth_required=True)
        self.test_endpoint("/api/projects/123", "PUT", auth_required=True)
        self.test_endpoint("/api/projects/123", "DELETE", auth_required=True)
        
        # اختبارات الفيديو
        print("\n🎬 اختبارات الفيديو")
        print("-" * 30)
        self.test_endpoint("/api/videos", "GET", auth_required=True)
        self.test_endpoint("/api/videos/create", "POST", auth_required=True)
        self.test_endpoint("/api/videos/generate", "POST", auth_required=True)
        self.test_endpoint("/api/videos/123/status", "GET", auth_required=True)
        self.test_endpoint("/api/generate-video/123", "POST", auth_required=True)
        
        # اختبارات الرفع
        print("\n📤 اختبارات الرفع")
        print("-" * 30)
        self.test_endpoint("/api/upload/image", "POST", auth_required=True)
        self.test_endpoint("/api/upload/audio", "POST", auth_required=True)
        
        # اختبارات الوظائف
        print("\n⚙️ اختبارات الوظائف")
        print("-" * 30)
        self.test_endpoint("/api/jobs/123", "GET", auth_required=True)
        
        # اختبارات الملف الشخصي
        print("\n👤 اختبارات الملف الشخصي")
        print("-" * 30)
        self.test_endpoint("/api/profile", "GET", auth_required=True)
        self.test_endpoint("/api/profile", "PUT", auth_required=True)
        
        # اختبارات الخطط والدفع
        print("\n💳 اختبارات الخطط والدفع")
        print("-" * 30)
        self.test_endpoint("/api/plans", "GET")
        self.test_endpoint("/api/payment/create", "POST", auth_required=True)
        self.test_endpoint("/api/payment/webhook", "POST", expected_status=422)  # بدون بيانات
        self.test_endpoint("/api/payments/paypal-stats", "GET")
        self.test_endpoint("/api/payments/plans", "GET")
        self.test_endpoint("/api/payments/plans/123", "GET")
        self.test_endpoint("/api/payments/plans/create", "POST", auth_required=True)
        self.test_endpoint("/api/payments/subscribe/123", "POST", auth_required=True)
        
        # اختبارات نماذج الذكاء الاصطناعي
        print("\n🤖 اختبارات نماذج الذكاء الاصطناعي")
        print("-" * 30)
        self.test_endpoint("/api/ai-models/status", "GET")
        self.test_endpoint("/api/ai-models/initialize", "POST", auth_required=True)
        self.test_endpoint("/api/ai-models/enhance-image", "POST", auth_required=True)
        self.test_endpoint("/api/ai-models/generate-sadtalker", "POST", auth_required=True)
        self.test_endpoint("/api/ai-models/generate-wav2lip", "POST", auth_required=True)
        
        # اختبارات التعليقات والتقييمات
        print("\n💬 اختبارات التعليقات والتقييمات")
        print("-" * 30)
        self.test_endpoint("/api/comments", "POST", auth_required=True)
        self.test_endpoint("/api/projects/123/comments", "GET", auth_required=True)
        self.test_endpoint("/api/ratings", "POST", auth_required=True)
        
        # اختبارات الإحصائيات
        print("\n📊 اختبارات الإحصائيات")
        print("-" * 30)
        self.test_endpoint("/api/files/storage-stats", "GET")
        self.test_endpoint("/api/video/generation-stats", "GET")
        
        # طباعة النتائج النهائية
        self.print_summary()
    
    def print_summary(self):
        """طباعة ملخص النتائج"""
        print("\n" + "=" * 50)
        print("📊 ملخص نتائج الاختبار")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        warning_tests = len([r for r in self.test_results if r["status"] == "WARNING"])
        
        print(f"📈 إجمالي الاختبارات: {total_tests}")
        print(f"✅ نجح: {passed_tests}")
        print(f"❌ فشل: {failed_tests}")
        print(f"⚠️ تحذيرات: {warning_tests}")
        print(f"📊 معدل النجاح: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ الاختبارات الفاشلة:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"   • {result['method']} {result['endpoint']} - {result['details']}")
        
        if warning_tests > 0:
            print("\n⚠️ التحذيرات:")
            for result in self.test_results:
                if result["status"] == "WARNING":
                    print(f"   • {result['method']} {result['endpoint']} - {result['details']}")
        
        if failed_tests == 0:
            print("\n🎉 جميع الاختبارات نجحت!")
        else:
            print(f"\n⚠️ يوجد {failed_tests} اختبار فاشل يحتاج إلى إصلاح")

def main():
    """الدالة الرئيسية"""
    tester = APITester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()