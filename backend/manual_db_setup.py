#!/usr/bin/env python3
"""
Manual Database Setup for VEO7
This script manually creates the required data in Supabase
"""

import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_plans_data():
    """Setup plans data manually"""
    
    # Get Supabase credentials
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not service_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env file")
        return False
    
    try:
        # Create Supabase client with service role key
        supabase: Client = create_client(url, service_key)
        
        print("🔄 Setting up plans data...")
        
        # Define plans data
        plans_data = [
            {
                "name": "Free",
                "description": "خطة مجانية للمبتدئين",
                "price": 0.00,
                "currency": "USD",
                "duration_days": 30,
                "features": ["إنشاء 5 فيديوهات شهرياً", "جودة HD", "دعم أساسي"],
                "max_projects": 3,
                "max_videos_per_month": 5,
                "max_storage_gb": 1,
                "is_active": True
            },
            {
                "name": "Basic",
                "description": "خطة أساسية للاستخدام الشخصي",
                "price": 9.99,
                "currency": "USD",
                "duration_days": 30,
                "features": ["إنشاء 25 فيديو شهرياً", "جودة Full HD", "دعم عبر البريد الإلكتروني", "إزالة العلامة المائية"],
                "max_projects": 10,
                "max_videos_per_month": 25,
                "max_storage_gb": 5,
                "is_active": True
            },
            {
                "name": "Pro",
                "description": "خطة احترافية للمبدعين",
                "price": 29.99,
                "currency": "USD",
                "duration_days": 30,
                "features": ["إنشاء 100 فيديو شهرياً", "جودة 4K", "دعم أولوية", "تحليلات متقدمة", "تصدير بصيغ متعددة"],
                "max_projects": 50,
                "max_videos_per_month": 100,
                "max_storage_gb": 20,
                "is_active": True
            },
            {
                "name": "Enterprise",
                "description": "خطة للشركات والمؤسسات",
                "price": 99.99,
                "currency": "USD",
                "duration_days": 30,
                "features": ["فيديوهات غير محدودة", "جودة 4K+", "دعم مخصص 24/7", "API مخصص", "تكامل مع الأنظمة", "تدريب فريق العمل"],
                "max_projects": -1,
                "max_videos_per_month": -1,
                "max_storage_gb": 100,
                "is_active": True
            }
        ]
        
        # Try to insert plans data
        try:
            # First, check if plans table exists by trying to select from it
            result = supabase.table("plans").select("*").limit(1).execute()
            print("✅ Plans table exists")
            
            # Check if we already have plans
            existing_plans = supabase.table("plans").select("name").execute()
            existing_plan_names = [plan["name"] for plan in existing_plans.data]
            
            # Insert only new plans
            new_plans = [plan for plan in plans_data if plan["name"] not in existing_plan_names]
            
            if new_plans:
                insert_result = supabase.table("plans").insert(new_plans).execute()
                print(f"✅ Inserted {len(new_plans)} new plans")
            else:
                print("ℹ️  All plans already exist")
            
            # Verify plans
            all_plans = supabase.table("plans").select("*").execute()
            print(f"✅ Total plans in database: {len(all_plans.data)}")
            
            for plan in all_plans.data:
                print(f"  - {plan['name']}: ${plan['price']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error with plans table: {e}")
            print("ℹ️  The plans table may not exist yet. Please create it manually in Supabase Dashboard.")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Supabase: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints after setup"""
    
    import requests
    
    print("\n🔄 Testing API endpoints...")
    
    try:
        # Test health endpoint
        health_response = requests.get("http://localhost:8000/api/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"⚠️  Health endpoint: {health_response.status_code}")
        
        # Test plans endpoint
        plans_response = requests.get("http://localhost:8000/api/plans", timeout=5)
        if plans_response.status_code == 200:
            plans = plans_response.json()
            print(f"✅ Plans endpoint working - {len(plans)} plans found")
        else:
            print(f"❌ Plans endpoint failed: {plans_response.status_code} - {plans_response.text}")
        
    except Exception as e:
        print(f"❌ Error testing endpoints: {e}")

def main():
    """Main function"""
    print("🚀 VEO7 Manual Database Setup")
    print("=" * 50)
    
    # Setup plans data
    success = setup_plans_data()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        
        # Test API endpoints
        test_api_endpoints()
        
    else:
        print("\n❌ Database setup failed!")
        print("\nManual steps to fix:")
        print("1. Go to https://supabase.com/dashboard")
        print("2. Open SQL Editor")
        print("3. Run the following SQL:")
        print("""
CREATE TABLE IF NOT EXISTS plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    duration_days INTEGER NOT NULL DEFAULT 30,
    features JSONB DEFAULT '[]'::jsonb,
    max_projects INTEGER DEFAULT 10,
    max_videos_per_month INTEGER DEFAULT 50,
    max_storage_gb INTEGER DEFAULT 5,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
        """)
        print("4. Then run this script again")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)