#!/usr/bin/env python3
"""
Get Supabase Database URL
This script helps construct the correct DATABASE_URL for Supabase
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_supabase_db_url():
    """Construct Supabase DATABASE_URL from SUPABASE_URL"""
    
    supabase_url = os.getenv("SUPABASE_URL")
    
    if not supabase_url:
        print("❌ Error: SUPABASE_URL not found in .env file")
        return None
    
    # Extract project reference from Supabase URL
    # Format: https://PROJECT_REF.supabase.co
    if "supabase.co" in supabase_url:
        project_ref = supabase_url.replace("https://", "").replace(".supabase.co", "")
        
        # Construct the database URL
        # Format: postgresql://postgres:[YOUR-PASSWORD]@db.PROJECT_REF.supabase.co:5432/postgres
        db_url = f"postgresql://postgres:[YOUR-PASSWORD]@db.{project_ref}.supabase.co:5432/postgres"
        
        print("🔍 Supabase Project Reference:", project_ref)
        print("📝 Database URL Template:", db_url)
        print("\n⚠️  Important: Replace [YOUR-PASSWORD] with your actual database password")
        print("You can find your database password in Supabase Dashboard > Settings > Database")
        
        return db_url
    else:
        print("❌ Error: Invalid SUPABASE_URL format")
        return None

def main():
    """Main function"""
    print("🚀 Supabase Database URL Generator")
    print("=" * 50)
    
    db_url = get_supabase_db_url()
    
    if db_url:
        print("\n✅ Database URL template generated successfully!")
        print("\nNext steps:")
        print("1. Go to Supabase Dashboard > Settings > Database")
        print("2. Copy your database password")
        print("3. Replace [YOUR-PASSWORD] in the URL above")
        print("4. Update DATABASE_URL in your .env file")
    else:
        print("\n❌ Failed to generate database URL")

if __name__ == "__main__":
    main()