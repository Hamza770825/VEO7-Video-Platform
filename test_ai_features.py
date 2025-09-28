#!/usr/bin/env python3
"""
اختبار ميزات الذكاء الاصطناعي في منصة VEO7
Test AI Features for VEO7 Platform
"""

import requests
import json
import os
import time
from pathlib import Path

# إعدادات الاختبار
BASE_URL = "http://localhost:8000"
TEST_IMAGE_PATH = "test_image.svg"

def create_test_user():
    """إنشاء مستخدم اختبار والحصول على رمز المصادقة"""
    print("👤 إنشاء مستخدم اختبار...")
    
    # بيانات المستخدم
    user_data = {
        "email": "test@veo7.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    try:
        # محاولة تسجيل الدخول أولاً
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data={
                "username": user_data["email"],
                "password": user_data["password"]
            }
        )
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            print("✅ تم تسجيل الدخول بنجاح")
            return token_data.get("access_token")
        
        # إذا فشل تسجيل الدخول، نحاول إنشاء حساب جديد
        register_response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=user_data
        )
        
        if register_response.status_code == 201:
            print("✅ تم إنشاء المستخدم بنجاح")
            
            # تسجيل الدخول بعد الإنشاء
            login_response = requests.post(
                f"{BASE_URL}/api/auth/login",
                data={
                    "username": user_data["email"],
                    "password": user_data["password"]
                }
            )
            
            if login_response.status_code == 200:
                token_data = login_response.json()
                return token_data.get("access_token")
        
        print(f"❌ فشل في إنشاء المستخدم: {register_response.text}")
        return None
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء المستخدم: {e}")
        return None

def get_auth_headers(token):
    """الحصول على headers المصادقة"""
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def test_ai_models_status(token=None):
    """اختبار حالة نماذج الذكاء الاصطناعي"""
    print("🔍 اختبار حالة نماذج الذكاء الاصطناعي...")
    
    try:
        headers = get_auth_headers(token)
        response = requests.get(f"{BASE_URL}/api/ai-models/status", headers=headers)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ تم الحصول على حالة النماذج بنجاح:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ فشل في الحصول على حالة النماذج: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في الاتصال: {e}")
        return False

def test_basic_endpoints():
    """اختبار نقاط النهاية الأساسية"""
    print("\n🔗 اختبار نقاط النهاية الأساسية...")
    
    endpoints = [
        ("/api/health", "GET"),
        ("/api/videos", "GET"),
        ("/", "GET")
    ]
    
    results = {}
    
    for endpoint, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}")
            
            results[endpoint] = {
                "status_code": response.status_code,
                "success": response.status_code < 500  # قبول أي شيء أقل من 500
            }
            
            status_emoji = "✅" if response.status_code < 500 else "❌"
            print(f"{status_emoji} {endpoint}: {response.status_code}")
            
        except Exception as e:
            results[endpoint] = {
                "status_code": None,
                "success": False,
                "error": str(e)
            }
            print(f"❌ {endpoint}: {e}")
    
    return results

def test_video_generation_simple(token=None):
    """اختبار توليد فيديو بسيط"""
    print("\n🎬 اختبار توليد فيديو بسيط...")
    
    try:
        headers = get_auth_headers(token)
        headers["Content-Type"] = "application/json"
        
        data = {
            "text": "مرحبا بكم في منصة VEO7",
            "title": "فيديو اختبار",
            "description": "هذا فيديو اختبار للتأكد من عمل النظام"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/videos/generate",
            json=data,
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            print("✅ تم توليد الفيديو بنجاح:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ فشل في توليد الفيديو: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في توليد الفيديو: {e}")
        return False

def test_server_health():
    """اختبار صحة الخادم"""
    print("\n🏥 اختبار صحة الخادم...")
    
    try:
        # اختبار الاتصال الأساسي
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        
        if response.status_code == 200:
            print("✅ الخادم يعمل بشكل صحيح")
            return True
        else:
            print(f"⚠️ الخادم يستجيب ولكن بحالة: {response.status_code}")
            return True  # لا يزال يعتبر نجاحاً إذا كان يستجيب
            
    except requests.exceptions.ConnectionError:
        print("❌ لا يمكن الاتصال بالخادم")
        return False
    except Exception as e:
        print(f"❌ خطأ في اختبار الخادم: {e}")
        return False

def main():
    """تشغيل جميع الاختبارات"""
    print("🚀 بدء اختبار ميزات الذكاء الاصطناعي في منصة VEO7")
    print("=" * 60)
    
    # نتائج الاختبارات
    test_results = {
        "server_health": False,
        "user_authentication": False,
        "ai_models_status": False,
        "video_generation": False,
        "basic_endpoints": {}
    }
    
    # اختبار صحة الخادم أولاً
    test_results["server_health"] = test_server_health()
    
    if not test_results["server_health"]:
        print("\n❌ الخادم لا يعمل. يرجى التأكد من تشغيل الخادم الخلفي.")
        return
    
    # إنشاء مستخدم اختبار
    token = create_test_user()
    test_results["user_authentication"] = token is not None
    
    # تشغيل الاختبارات
    test_results["ai_models_status"] = test_ai_models_status(token)
    test_results["video_generation"] = test_video_generation_simple(token)
    test_results["basic_endpoints"] = test_basic_endpoints()
    
    # تقرير النتائج
    print("\n" + "=" * 60)
    print("📊 تقرير نتائج الاختبارات:")
    print("=" * 60)
    
    passed_tests = 0
    total_tests = 4
    
    for test_name, result in test_results.items():
        if test_name == "basic_endpoints":
            continue
        
        status = "✅ نجح" if result else "❌ فشل"
        print(f"{test_name}: {status}")
        if result:
            passed_tests += 1
    
    # نتائج نقاط النهاية
    endpoint_results = test_results["basic_endpoints"]
    successful_endpoints = sum(1 for r in endpoint_results.values() if r.get("success", False))
    total_endpoints = len(endpoint_results)
    
    print(f"\nنقاط النهاية الأساسية: {successful_endpoints}/{total_endpoints} تعمل بنجاح")
    
    # النتيجة الإجمالية
    overall_success = passed_tests / total_tests
    print(f"\nالنتيجة الإجمالية: {passed_tests}/{total_tests} ({overall_success:.1%})")
    
    if overall_success >= 0.5:
        print("🎉 معظم الاختبارات نجحت!")
    else:
        print("⚠️ العديد من الاختبارات فشلت، يرجى مراجعة الأخطاء أعلاه.")
    
    # حفظ النتائج
    with open("ai_features_test_report.json", "w", encoding="utf-8") as f:
        json.dump(test_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 تم حفظ تقرير مفصل في: ai_features_test_report.json")
    
    # توصيات
    print("\n💡 توصيات:")
    if not test_results["user_authentication"]:
        print("- تحقق من إعدادات قاعدة البيانات والمصادقة")
    if not test_results["ai_models_status"]:
        print("- تحقق من تثبيت مكتبات الذكاء الاصطناعي")
    if not test_results["video_generation"]:
        print("- تحقق من خدمة توليد الفيديو")

if __name__ == "__main__":
    main()