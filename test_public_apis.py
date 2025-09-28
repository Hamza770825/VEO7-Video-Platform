#!/usr/bin/env python3
"""
اختبار نقاط API العامة في منصة VEO7
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_public_endpoints():
    """اختبار نقاط API العامة"""
    print("🔍 اختبار نقاط API العامة...")
    
    endpoints = [
        ("/", "الصفحة الرئيسية"),
        ("/docs", "وثائق API"),
        ("/redoc", "وثائق ReDoc"),
        ("/api/video/generation-stats", "إحصائيات إنشاء الفيديو"),
    ]
    
    results = []
    
    for endpoint, description in endpoints:
        try:
            print(f"\n📡 اختبار: {description} ({endpoint})")
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {description} - يعمل بشكل صحيح")
                results.append((endpoint, True, response.status_code))
            else:
                print(f"⚠️ {description} - رمز الاستجابة: {response.status_code}")
                results.append((endpoint, False, response.status_code))
                
        except Exception as e:
            print(f"❌ {description} - خطأ: {e}")
            results.append((endpoint, False, str(e)))
    
    return results

def test_protected_endpoints():
    """اختبار نقاط API المحمية (يجب أن ترجع 401/403)"""
    print("\n🔒 اختبار نقاط API المحمية...")
    
    protected_endpoints = [
        ("/api/projects", "GET", "قائمة المشاريع"),
        ("/api/projects", "POST", "إنشاء مشروع"),
        ("/api/user/profile", "GET", "ملف المستخدم"),
    ]
    
    results = []
    
    for endpoint, method, description in protected_endpoints:
        try:
            print(f"\n🔐 اختبار: {description} ({method} {endpoint})")
            
            if method == "GET":
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            elif method == "POST":
                response = requests.post(f"{BASE_URL}{endpoint}", json={}, timeout=10)
            
            if response.status_code in [401, 403]:
                print(f"✅ {description} - محمي بشكل صحيح (رمز: {response.status_code})")
                results.append((endpoint, True, response.status_code))
            else:
                print(f"⚠️ {description} - رمز غير متوقع: {response.status_code}")
                results.append((endpoint, False, response.status_code))
                
        except Exception as e:
            print(f"❌ {description} - خطأ: {e}")
            results.append((endpoint, False, str(e)))
    
    return results

def test_cors_headers():
    """اختبار إعدادات CORS"""
    print("\n🌐 اختبار إعدادات CORS...")
    
    try:
        response = requests.options(f"{BASE_URL}/api/projects", headers={
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Authorization'
        })
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        
        print("📋 إعدادات CORS:")
        for header, value in cors_headers.items():
            if value:
                print(f"   ✅ {header}: {value}")
            else:
                print(f"   ❌ {header}: غير موجود")
        
        return cors_headers
        
    except Exception as e:
        print(f"❌ خطأ في اختبار CORS: {e}")
        return {}

def main():
    """تشغيل جميع الاختبارات"""
    print("🚀 بدء اختبار نقاط API العامة لمنصة VEO7")
    print("=" * 60)
    
    # اختبار النقاط العامة
    public_results = test_public_endpoints()
    
    # اختبار النقاط المحمية
    protected_results = test_protected_endpoints()
    
    # اختبار CORS
    cors_results = test_cors_headers()
    
    # تلخيص النتائج
    print("\n" + "=" * 60)
    print("📊 ملخص النتائج:")
    
    public_passed = sum(1 for _, success, _ in public_results if success)
    protected_passed = sum(1 for _, success, _ in protected_results if success)
    
    print(f"🌍 النقاط العامة: {public_passed}/{len(public_results)} نجحت")
    print(f"🔒 النقاط المحمية: {protected_passed}/{len(protected_results)} محمية بشكل صحيح")
    print(f"🌐 CORS: {'✅ مُعد' if cors_results else '❌ غير مُعد'}")
    
    total_tests = len(public_results) + len(protected_results) + (1 if cors_results else 0)
    total_passed = public_passed + protected_passed + (1 if cors_results else 0)
    
    print(f"\n🎯 النتيجة الإجمالية: {total_passed}/{total_tests} اختبارات نجحت")
    
    if total_passed == total_tests:
        print("🎉 جميع الاختبارات نجحت! API يعمل بشكل مثالي")
        return True
    else:
        print("⚠️ بعض الاختبارات فشلت، يرجى المراجعة")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)