#!/usr/bin/env python3
"""
Apply plans table fix using Supabase REST API
This script creates the plans table using HTTP requests
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def apply_plans_fix():
    """Apply the plans table fix using Supabase REST API"""
    
    # Get Supabase credentials
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not service_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env file")
        return False
    
    try:
        # Read the plans SQL file
        sql_file_path = Path(__file__).parent / "create_plans_table.sql"
        
        if not sql_file_path.exists():
            print(f"❌ Error: SQL file not found at {sql_file_path}")
            return False
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print("🔄 Applying plans table fix to Supabase...")
        
        # Use Supabase REST API to execute SQL
        headers = {
            'apikey': service_key,
            'Authorization': f'Bearer {service_key}',
            'Content-Type': 'application/json'
        }
        
        # Execute SQL using the rpc endpoint
        rpc_url = f"{url}/rest/v1/rpc/exec_sql"
        
        # Try to execute the SQL
        response = requests.post(
            rpc_url,
            headers=headers,
            json={'sql': sql_content},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Plans table created successfully!")
        else:
            print(f"⚠️  SQL execution response: {response.status_code} - {response.text}")
            # Continue to test if table exists
        
        # Test if plans table is accessible
        plans_url = f"{url}/rest/v1/plans?select=count"
        test_response = requests.get(plans_url, headers=headers, timeout=10)
        
        if test_response.status_code == 200:
            print("✅ Plans table is accessible")
            
            # Get actual plans data
            plans_data_url = f"{url}/rest/v1/plans?select=*"
            data_response = requests.get(plans_data_url, headers=headers, timeout=10)
            
            if data_response.status_code == 200:
                plans = data_response.json()
                print(f"✅ Found {len(plans)} plans in the database")
                for plan in plans:
                    print(f"  - {plan.get('name', 'Unknown')}: ${plan.get('price', 0)}")
            
            return True
        else:
            print(f"❌ Error: Plans table still not accessible: {test_response.status_code} - {test_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error applying plans fix: {e}")
        return False

def create_minimal_tables():
    """Create minimal required tables"""
    
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not service_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
        return False
    
    headers = {
        'apikey': service_key,
        'Authorization': f'Bearer {service_key}',
        'Content-Type': 'application/json'
    }
    
    # Create tables using direct SQL execution via HTTP
    tables_sql = """
    -- Enable required extensions
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
    
    -- Create plans table
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
    
    -- Insert default plans if not exists
    INSERT INTO plans (name, description, price, duration_days, features, max_projects, max_videos_per_month, max_storage_gb, is_active) 
    SELECT 'Free', 'خطة مجانية للمبتدئين', 0.00, 30, '["إنشاء 5 فيديوهات شهرياً", "جودة HD", "دعم أساسي"]'::jsonb, 3, 5, 1, true
    WHERE NOT EXISTS (SELECT 1 FROM plans WHERE name = 'Free');
    
    INSERT INTO plans (name, description, price, duration_days, features, max_projects, max_videos_per_month, max_storage_gb, is_active) 
    SELECT 'Basic', 'خطة أساسية للاستخدام الشخصي', 9.99, 30, '["إنشاء 25 فيديو شهرياً", "جودة Full HD", "دعم عبر البريد الإلكتروني", "إزالة العلامة المائية"]'::jsonb, 10, 25, 5, true
    WHERE NOT EXISTS (SELECT 1 FROM plans WHERE name = 'Basic');
    
    INSERT INTO plans (name, description, price, duration_days, features, max_projects, max_videos_per_month, max_storage_gb, is_active) 
    SELECT 'Pro', 'خطة احترافية للمبدعين', 29.99, 30, '["إنشاء 100 فيديو شهرياً", "جودة 4K", "دعم أولوية", "تحليلات متقدمة", "تصدير بصيغ متعددة"]'::jsonb, 50, 100, 20, true
    WHERE NOT EXISTS (SELECT 1 FROM plans WHERE name = 'Pro');
    """
    
    try:
        print("🔄 Creating minimal required tables...")
        
        # Try using the SQL editor endpoint
        sql_url = f"{url}/rest/v1/rpc/exec_sql"
        
        response = requests.post(
            sql_url,
            headers=headers,
            json={'sql': tables_sql},
            timeout=30
        )
        
        print(f"📝 SQL execution response: {response.status_code}")
        if response.text:
            print(f"📄 Response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def main():
    """Main function"""
    print("🚀 VEO7 Plans Table Fix")
    print("=" * 40)
    
    # Try to create minimal tables first
    create_minimal_tables()
    
    # Apply the plans fix
    success = apply_plans_fix()
    
    if success:
        print("\n🎉 Plans table fix completed successfully!")
        print("You can now test the /api/plans endpoint.")
    else:
        print("\n❌ Plans table fix failed!")
        print("Please apply the SQL manually in Supabase Dashboard:")
        print("1. Go to https://supabase.com/dashboard")
        print("2. Open SQL Editor")
        print("3. Copy and paste the content of create_plans_table.sql")
        print("4. Run the SQL")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)