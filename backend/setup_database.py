#!/usr/bin/env python3
"""
VEO7 Database Setup Script
Automatically sets up the database schema in Supabase
"""

import asyncio
import os
import sys
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_supabase_client() -> Client:
    """Create Supabase client with service role key"""
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    if not url or not service_key:
        raise ValueError(
            "❌ SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env file\n"
            "📖 Please check SUPABASE_SETUP_GUIDE.md for setup instructions"
        )
    
    if url == "https://your-project.supabase.co" or service_key == "your-service-key-here":
        raise ValueError(
            "❌ Please update .env file with your actual Supabase credentials\n"
            "📖 Check SUPABASE_SETUP_GUIDE.md for setup instructions"
        )
    
    return create_client(url, service_key)

def read_sql_file(file_path: str) -> list:
    """Read SQL file and split into individual statements"""
    sql_path = Path(file_path)
    if not sql_path.exists():
        raise FileNotFoundError(f"❌ SQL file not found: {file_path}")
    
    with open(sql_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into statements and clean them
    statements = []
    current_statement = ""
    
    for line in content.split('\n'):
        line = line.strip()
        # Skip comments and empty lines
        if not line or line.startswith('--'):
            continue
        
        current_statement += line + " "
        
        # End of statement
        if line.endswith(';'):
            statement = current_statement.strip()
            if statement and statement != ';':
                statements.append(statement[:-1])  # Remove semicolon
            current_statement = ""
    
    return statements

async def execute_sql_statements(client: Client, statements: list) -> bool:
    """Execute SQL statements one by one"""
    success_count = 0
    total_count = len(statements)
    
    print(f"📊 Found {total_count} SQL statements to execute")
    print("🔄 Starting database setup...\n")
    
    for i, statement in enumerate(statements, 1):
        try:
            print(f"📝 Executing statement {i}/{total_count}...")
            
            # Execute SQL using Supabase RPC
            result = client.rpc('exec_sql', {'sql': statement}).execute()
            
            print(f"✅ Statement {i} executed successfully")
            success_count += 1
            
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️ Statement {i} failed: {error_msg}")
            
            # Check if it's a "already exists" error (which is OK)
            if any(keyword in error_msg.lower() for keyword in [
                'already exists', 'duplicate', 'relation already exists'
            ]):
                print(f"   ℹ️ This is expected if running setup multiple times")
                success_count += 1
            else:
                print(f"   ❌ Unexpected error, continuing with next statement")
    
    print(f"\n📈 Setup completed: {success_count}/{total_count} statements executed successfully")
    return success_count > 0

async def verify_setup(client: Client) -> bool:
    """Verify that the database setup was successful"""
    print("\n🔍 Verifying database setup...")
    
    required_tables = ['users', 'profiles', 'videos', 'user_stats']
    
    for table in required_tables:
        try:
            result = client.table(table).select('*').limit(1).execute()
            print(f"✅ Table '{table}' exists and is accessible")
        except Exception as e:
            print(f"❌ Table '{table}' verification failed: {str(e)}")
            return False
    
    print("✅ All required tables verified successfully!")
    return True

async def main():
    """Main setup function"""
    print("🚀 VEO7 Database Setup")
    print("=" * 50)
    
    try:
        # Create Supabase client
        print("🔗 Connecting to Supabase...")
        client = get_supabase_client()
        print("✅ Connected to Supabase successfully")
        
        # Read SQL file
        sql_file = "../fix_database.sql"
        print(f"📖 Reading SQL file: {sql_file}")
        statements = read_sql_file(sql_file)
        
        # Execute statements
        success = await execute_sql_statements(client, statements)
        
        if success:
            # Verify setup
            verification_success = await verify_setup(client)
            
            if verification_success:
                print("\n🎉 Database setup completed successfully!")
                print("✅ Your VEO7 platform is ready to use!")
            else:
                print("\n⚠️ Setup completed but verification failed")
                print("🔧 Please check your Supabase dashboard manually")
        else:
            print("\n❌ Database setup failed")
            print("📖 Please check SUPABASE_SETUP_GUIDE.md for troubleshooting")
            
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        print("📖 Please check SUPABASE_SETUP_GUIDE.md for setup instructions")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())