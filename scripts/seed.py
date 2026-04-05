import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from app.db.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.category import Category
from app.models.transaction import Transaction
from app.core.security import get_password_hash

def seed_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        if db.query(User).count() > 0:
            print("Database already contains Data. Skipping seed.")
            return

        print("Creating users...")
        users_data = [
            {"email": "admin@example.com", "username": "Admin", "password": "password123", "role": "admin"},
            {"email": "analyst@example.com", "username": "Analyst", "password": "password123", "role": "analyst"},
            {"email": "viewer@example.com", "username": "Viewer", "password": "password123", "role": "viewer"},
        ]
        
        users = []
        for u in users_data:
            user = User(
                email=u["email"],
                username=u["username"],
                password_hash=get_password_hash(u["password"]),
                role=u["role"]
            )
            db.add(user)
            users.append(user)
        
        db.commit()
        for u in users:
            db.refresh(u)
        
        print("Creating default categories and transactions for Admin user...")
        admin = users[0]
        categories_data = ["Salary", "Food", "Rent", "Entertainment"]
        categories = []
        
        for name in categories_data:
            cat = Category(user_id=admin.id, name=name)
            db.add(cat)
            categories.append(cat)
        
        db.commit()
        for c in categories:
            db.refresh(c)
            
        print("Adding sample transactions...")
        txns = [
            Transaction(user_id=admin.id, category_id=categories[0].id, amount=5000.0, type="income", date=datetime.now() - timedelta(days=10), notes="Monthly Salary"),
            Transaction(user_id=admin.id, category_id=categories[2].id, amount=1200.0, type="expense", date=datetime.now() - timedelta(days=8), notes="Rent"),
            Transaction(user_id=admin.id, category_id=categories[1].id, amount=150.0, type="expense", date=datetime.now() - timedelta(days=5), notes="Groceries"),
            Transaction(user_id=admin.id, category_id=categories[3].id, amount=60.0, type="expense", date=datetime.now() - timedelta(days=2), notes="Movie tickets")
        ]
        
        db.bulk_save_objects(txns)
        db.commit()
        
        print("Database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
