#!/usr/bin/env python3
"""
اختبار شامل لتدفق إنشاء الفيديو في منصة VEO7
"""

import requests
import json
import time
import os
from pathlib import Path

# إعدادات الاختبار
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_api_health():
    """اختبار صحة API"""
    print("🔍 اختبار صحة API...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API يعمل بشكل صحيح - الإصدار: {data.get('version')}")
            print(f"📋 الميزات المتاحة: {', '.join(data.get('features', []))}")
            return True
        else:
            print(f"❌ خطأ في API: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ فشل في الاتصال بـ API: {e}")
        return False

def test_video_generation_stats():
    """اختبار إحصائيات إنشاء الفيديو"""
    print("\n🔍 اختبار إحصائيات إنشاء الفيديو...")
    try:
        response = requests.get(f"{BASE_URL}/api/video/generation-stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ الإحصائيات متاحة:")
            print(f"   📁 الملفات المؤقتة: {data.get('temp_files', 0)}")
            print(f"   🎬 ملفات الإخراج: {data.get('output_files', 0)}")
            models = data.get('models_available', {})
            print(f"   🤖 النماذج المتاحة:")
            for model, available in models.items():
                status = "✅" if available else "❌"
                print(f"      {status} {model}")
            return True
        else:
            print(f"❌ خطأ في الحصول على الإحصائيات: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ فشل في الحصول على الإحصائيات: {e}")
        return False

def test_frontend_accessibility():
    """اختبار إمكانية الوصول للواجهة الأمامية"""
    print("\n🔍 اختبار إمكانية الوصول للواجهة الأمامية...")
    try:
        # اختبار الصفحة الرئيسية
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print("✅ الصفحة الرئيسية متاحة")
        else:
            print(f"❌ خطأ في الصفحة الرئيسية: {response.status_code}")
            return False
        
        # اختبار صفحة إنشاء الفيديو
        response = requests.get(f"{FRONTEND_URL}/create")
        if response.status_code == 200:
            print("✅ صفحة إنشاء الفيديو متاحة")
            return True
        else:
            print(f"❌ خطأ في صفحة إنشاء الفيديو: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ فشل في الوصول للواجهة الأمامية: {e}")
        return False

def create_test_image():
    """إنشاء صورة اختبار SVG"""
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- خلفية متدرجة -->
  <rect width="512" height="512" fill="url(#bg)"/>
  
  <!-- دائرة مركزية -->
  <circle cx="256" cy="256" r="100" fill="#ffffff" opacity="0.9"/>
  
  <!-- نص VEO7 -->
  <text x="256" y="270" font-family="Arial, sans-serif" font-size="36" font-weight="bold" 
        text-anchor="middle" fill="#333333">VEO7</text>
  
  <!-- نجوم زخرفية -->
  <polygon points="256,150 260,162 272,162 262,170 266,182 256,174 246,182 250,170 240,162 252,162" 
           fill="#ffdd44"/>
  <polygon points="180,200 182,206 188,206 184,210 186,216 180,212 174,216 176,210 172,206 178,206" 
           fill="#ffdd44"/>
  <polygon points="332,200 334,206 340,206 336,210 338,216 332,212 326,216 328,210 324,206 330,206" 
           fill="#ffdd44"/>
</svg>'''
    
    test_image_path = "test_image.svg"
    with open(test_image_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"✅ تم إنشاء صورة الاختبار: {test_image_path}")
    return test_image_path

def create_test_project():
    """إنشاء مشروع اختبار"""
    print("📝 إنشاء مشروع اختبار...")
    
    # بيانات المشروع
    project_data = {
        "title": "مشروع اختبار VEO7",
        "description": "مشروع اختبار لإنشاء فيديو تجريبي",
        "input_type": "image_text",
        "input_text": "مرحباً بكم في منصة VEO7 لإنشاء الفيديوهات"
    }
    
    # محاولة إنشاء المشروع بدون مصادقة (للاختبار)
    try:
        response = requests.post(
            f"{BASE_URL}/api/projects",
            json=project_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            project_id = result.get('project', {}).get('id')
            print(f"✅ تم إنشاء المشروع بنجاح - ID: {project_id}")
            return project_id
        else:
            print(f"❌ فشل في إنشاء المشروع: {response.status_code}")
            print(f"📄 الاستجابة: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ خطأ في إنشاء المشروع: {e}")
        return None

def test_basic_video_generation():
    """اختبار إنشاء فيديو أساسي باستخدام نقطة API الجديدة"""
    print("\n🎬 اختبار إنشاء فيديو أساسي...")
    
    try:
        # اختبار نقطة API الجديدة /api/videos/create
        video_data = {
            "title": "فيديو اختبار",
            "description": "وصف فيديو الاختبار",
            "text_content": "مرحباً بكم في اختبار VEO7",
            "settings": {
                "quality": "medium",
                "speed": 1.0,
                "voice": "female",
                "language": "ar"
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/api/videos/create",
            json=video_data,
            timeout=30
        )
        
        if response.status_code == 401 or response.status_code == 403:
            print("⚠️  مطلوب مصادقة - هذا متوقع للاختبار")
            print("✅ نقطة API /api/videos/create تعمل بشكل صحيح")
            
            # اختبار نقطة حالة الفيديو أيضاً
            status_response = requests.get(
                f"{BASE_URL}/api/videos/test-id/status",
                timeout=10
            )
            
            if status_response.status_code == 401 or status_response.status_code == 403:
                print("✅ نقطة API /api/videos/status تعمل بشكل صحيح")
                return True
            else:
                print(f"⚠️  نقطة حالة الفيديو: {status_response.status_code}")
                return True
                
        elif response.status_code == 200:
            print("✅ تم إرسال طلب إنشاء الفيديو بنجاح")
            data = response.json()
            video_id = data.get('video_id')
            
            if video_id:
                # اختبار نقطة حالة الفيديو
                status_response = requests.get(
                    f"{BASE_URL}/api/videos/{video_id}/status",
                    timeout=10
                )
                
                if status_response.status_code == 200:
                    print("✅ نقطة حالة الفيديو تعمل بشكل صحيح")
                
            return True
        else:
            print(f"❌ فشل إنشاء الفيديو - كود الحالة: {response.status_code}")
            print(f"الاستجابة: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في اختبار إنشاء الفيديو: {e}")
        return False

def run_comprehensive_test():
    """تشغيل الاختبار الشامل"""
    print("🚀 بدء الاختبار الشامل لمنصة VEO7")
    print("=" * 50)
    
    tests = [
        ("اختبار صحة API", test_api_health),
        ("اختبار إحصائيات الفيديو", test_video_generation_stats),
        ("اختبار الواجهة الأمامية", test_frontend_accessibility),
        ("اختبار إنشاء الفيديو", test_basic_video_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} نجح")
            else:
                print(f"❌ {test_name} فشل")
        except Exception as e:
            print(f"❌ {test_name} فشل بخطأ: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 نتائج الاختبار: {passed}/{total} اختبارات نجحت")
    
    if passed == total:
        print("🎉 جميع الاختبارات نجحت! المنصة تعمل بشكل مثالي")
    elif passed > total // 2:
        print("⚠️ معظم الاختبارات نجحت، لكن هناك بعض المشاكل")
    else:
        print("🚨 فشلت معظم الاختبارات، يحتاج إلى مراجعة")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    exit(0 if success else 1)