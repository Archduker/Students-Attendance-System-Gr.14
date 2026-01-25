
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from data.database import Database
from data.repositories import UserRepository
from services import SecurityService, SessionService, AuthService

def main():
    print("🚀 Running Login Debugger...")
    
    # 1. Initialize Dependencies
    db = Database()
    user_repo = UserRepository(db)
    security_service = SecurityService()
    session_service = SessionService(security_service)
    # Email service not needed for login check, pass None
    auth_service = AuthService(user_repo, security_service, session_service, None)
    
    # 2. List All Users
    print("\n📋 Checking Database for Users:")
    
    # We might not have a 'find_all' in repo, let's try direct query if needed, 
    # but first let's see if we can find by known usernames
    
    usernames_to_check = ["admin", "teacher", "student", "student1", "taipn3010"]
    
    found_users = []
    
    # Direct DB query to list all users
    try:
        rows = db.fetch_all("SELECT user_id, username, email, role, password_hash FROM users")
        
        if not rows:
            print("❌ No users found in database! You need to run 'python main.py --seed'")
            return
            
        print(f"✅ Found {len(rows)} users:")
        print("-" * 60)
        print(f"{'ID':<5} {'Username':<15} {'Email':<25} {'Role':<10}")
        print("-" * 60)
        
        for row in rows:
            # Row is a sqlite3.Row object, can access by index or key
            uid = row["user_id"]
            uname = row["username"]
            email = row["email"]
            role = row["role"]
            
            print(f"{uid:<5} {uname:<15} {email:<25} {role:<10}")
            found_users.append((uname, "password123")) # Assuming default password from seed
            
    except Exception as e:
        print(f"❌ Error querying database: {e}")
        return

    # 3. Test Login
    print("\n🔐 Testing Login for found users (trying default password 'password123'):")
    
    # Also test valid email login for the first user
    if found_users:
         first_uname = found_users[0][0]
         # Find email for this user from DB output logic (not easily accessible here without restructure)
         # Just relying on printed output or hardcoding a test email
         pass

    for username, password in found_users:
        print(f"\nAttempting login for '{username}'...")
        try:
            user, token = auth_service.login(username, password)
            print(f"✅ SUCCESS (Username)! Token: {token[:10]}...")
            print(f"   User: {user.full_name}, Role: {user.role}")
            
            # Additional test: Try login with EMAIL
            if user.email:
                print(f"   Now trying with EMAIL: {user.email}...")
                user_email, token_email = auth_service.login(user.email, password)
                print(f"   ✅ SUCCESS (Email)! Token: {token_email[:10]}...")
                
        except Exception as e:
            print(f"❌ FAILED: {e}")
            
            # Try another password '123456' which is common in seeds
            print(f"   Retrying with '123456'...")
            try:
                user, token = auth_service.login(username, "123456")
                print(f"   ✅ SUCCESS! Token: {token[:10]}...")
                
                # Try email with 123456
                if user.email:
                    print(f"   Now trying with EMAIL: {user.email}...")
                    user_email, token_email = auth_service.login(user.email, "123456")
                    print(f"   ✅ SUCCESS (Email)! Token: {token_email[:10]}...")
                    
            except Exception as e2:
                 print(f"   ❌ FAILED: {e2}")

if __name__ == "__main__":
    main()
