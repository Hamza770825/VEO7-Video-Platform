#!/usr/bin/env python3
"""
Apply database fix directly to PostgreSQL
This script connects directly to the PostgreSQL database and applies the schema fix
"""

import os
import sys
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

def apply_database_fix_direct():
    """Apply the database fix SQL directly to PostgreSQL"""
    
    # Get database URL
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ Error: DATABASE_URL must be set in .env file")
        return False
    
    try:
        # Parse the database URL
        parsed = urlparse(database_url)
        
        # Connect to PostgreSQL
        print("🔄 Connecting to PostgreSQL database...")
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],  # Remove leading slash
            user=parsed.username,
            password=parsed.password,
            sslmode='require'
        )
        
        # Set autocommit to handle DDL statements
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Read the database fix SQL file
        sql_file_path = Path(__file__).parent / "database_fix_complete.sql"
        
        if not sql_file_path.exists():
            print(f"❌ Error: SQL file not found at {sql_file_path}")
            return False
        
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print("🔄 Applying database fix...")
        
        # Execute the entire SQL content
        try:
            cursor.execute(sql_content)
            print("✅ Database fix applied successfully!")
        except Exception as e:
            print(f"❌ Error executing SQL: {e}")
            return False
        
        # Test the fix by checking if plans table exists
        try:
            cursor.execute("SELECT COUNT(*) FROM plans;")
            count = cursor.fetchone()[0]
            print(f"✅ Plans table is accessible with {count} records")
            
            # Check other important tables
            tables_to_check = ['users', 'projects', 'jobs', 'comments', 'ratings', 'subscriptions']
            for table in tables_to_check:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table};")
                    count = cursor.fetchone()[0]
                    print(f"✅ {table} table: {count} records")
                except Exception as e:
                    print(f"⚠️  {table} table: {e}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: Plans table still not accessible: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return False
    
    finally:
        if 'conn' in locals():
            conn.close()

def main():
    """Main function"""
    print("🚀 VEO7 Database Fix Application (Direct Connection)")
    print("=" * 60)
    
    # Apply the database fix
    success = apply_database_fix_direct()
    
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