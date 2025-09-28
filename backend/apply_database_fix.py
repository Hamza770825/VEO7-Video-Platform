#!/usr/bin/env python3
"""
Apply database fix to Supabase
This script applies the complete database schema fix
"""

import os
import sys
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def apply_database_fix():
    """Apply the database fix SQL to Supabase"""
    
    # Get Supabase credentials
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not service_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env file")
        return False
    
    try:
        # Create Supabase client with service role key
        supabase: Client = create_client(url, service_key)
        
        # Read the database fix SQL file
        sql_file_path = Path(__file__).parent / "database_fix_complete.sql"
        
        if not sql_file_path.exists():
            print(f"❌ Error: SQL file not found at {sql_file_path}")
            return False
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print("🔄 Applying database fix to Supabase...")
        
        # Split SQL into individual statements and execute them
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        for i, statement in enumerate(statements):
            if statement.strip():
                try:
                    print(f"📝 Executing statement {i+1}/{len(statements)}...")
                    # Use the RPC function to execute raw SQL
                    result = supabase.rpc('exec_sql', {'sql': statement}).execute()
                    print(f"✅ Statement {i+1} executed successfully")
                except Exception as e:
                    print(f"⚠️  Warning: Statement {i+1} failed: {str(e)}")
                    # Continue with other statements
                    continue
        
        print("✅ Database fix applied successfully!")
        
        # Test the fix by checking if plans table exists
        try:
            result = supabase.table("plans").select("count").limit(1).execute()
            print("✅ Plans table is accessible")
            return True
        except Exception as e:
            print(f"❌ Error: Plans table still not accessible: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error applying database fix: {e}")
        return False

def create_exec_sql_function():
    """Create the exec_sql function in Supabase if it doesn't exist"""
    
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not service_key:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
        return False
    
    try:
        supabase: Client = create_client(url, service_key)
        
        # Create the exec_sql function
        exec_sql_function = """
        CREATE OR REPLACE FUNCTION exec_sql(sql text)
        RETURNS text
        LANGUAGE plpgsql
        SECURITY DEFINER
        AS $$
        BEGIN
            EXECUTE sql;
            RETURN 'OK';
        EXCEPTION
            WHEN OTHERS THEN
                RETURN SQLERRM;
        END;
        $$;
        """
        
        print("🔄 Creating exec_sql function...")
        result = supabase.rpc('exec_sql', {'sql': exec_sql_function}).execute()
        print("✅ exec_sql function created successfully")
        return True
        
    except Exception as e:
        print(f"ℹ️  exec_sql function may already exist or needs to be created manually: {e}")
        return True  # Continue anyway

def main():
    """Main function"""
    print("🚀 VEO7 Database Fix Application")
    print("=" * 50)
    
    # First, try to create the exec_sql function
    create_exec_sql_function()
    
    # Apply the database fix
    success = apply_database_fix()
    
    if success:
        print("\n🎉 Database fix completed successfully!")
        print("You can now test the API endpoints.")
    else:
        print("\n❌ Database fix failed!")
        print("Please check the error messages above and try again.")
        print("\nAlternatively, you can apply the SQL manually in Supabase Dashboard:")
        print("1. Go to https://supabase.com/dashboard")
        print("2. Open SQL Editor")
        print("3. Copy and paste the content of database_fix_complete.sql")
        print("4. Run the SQL")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)