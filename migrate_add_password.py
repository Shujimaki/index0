"""
Migration script to add password_hash field to existing users
and set a default password for existing users without one
"""
from app import build_application, database
from app.models import User
from werkzeug.security import generate_password_hash

def migrate():
    app = build_application()
    
    with app.app_context():
        # Check if password_hash column exists
        from sqlalchemy import inspect
        inspector = inspect(database.engine)
        columns = [col['name'] for col in inspector.get_columns('users')]
        
        if 'password_hash' not in columns:
            print("Adding password_hash column to users table...")
            from sqlalchemy import text
            with database.engine.connect() as conn:
                conn.execute(text('ALTER TABLE users ADD COLUMN password_hash VARCHAR(256)'))
                conn.commit()
            print("✅ Column added successfully!")
        else:
            print("✅ password_hash column already exists")
        
        # Set default password for users without password_hash
        users = User.query.all()
        default_password = "password123"  # Users should change this
        
        for user in users:
            if not user.password_hash or user.password_hash == '':
                user.set_password(default_password)
                print(f"✅ Set default password for user: {user.full_name}")
        
        database.session.commit()
        print(f"\n✅ Migration complete!")
        print(f"   {len(users)} users processed")
        print(f"   Default password for existing users: {default_password}")
        print(f"   ⚠️  Users should change their password after logging in")

if __name__ == '__main__':
    migrate()
