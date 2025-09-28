#!/usr/bin/env python3
"""
فحص الطرق المتاحة في Supabase Auth Client
"""

import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

try:
    from supabase import create_client
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    if url and key and "demo" not in url.lower():
        client = create_client(url, key)
        auth_methods = [method for method in dir(client.auth) if not method.startswith('_')]
        print("🔍 الطرق المتاحة في client.auth:")
        for method in sorted(auth_methods):
            print(f"  - {method}")
        
        # فحص إذا كانت طريقة resend موجودة
        if hasattr(client.auth, 'resend'):
            print("\n✅ طريقة resend موجودة")
            # محاولة فحص signature
            import inspect
            try:
                sig = inspect.signature(client.auth.resend)
                print(f"   التوقيع: {sig}")
            except:
                print("   لا يمكن الحصول على التوقيع")
        else:
            print("\n❌ طريقة resend غير موجودة")
            
        # فحص طرق أخرى محتملة
        potential_methods = ['resend_confirmation', 'resend_email', 'send_verification']
        for method in potential_methods:
            if hasattr(client.auth, method):
                print(f"✅ طريقة {method} موجودة")
            else:
                print(f"❌ طريقة {method} غير موجودة")
                
    else:
        print("❌ لا يمكن الاتصال بـ Supabase - استخدام وضع العرض التوضيحي")
        
except Exception as e:
    print(f"❌ خطأ: {e}")