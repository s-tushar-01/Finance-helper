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
        categories_data = [
            # Incomes
            "Salary", "Freelance", 
            # Expenses
            "Rent", "Utilities", "Food & Dining", "Transport", "Entertainment", "Shopping"
        ]
        
        categories = []
        for name in categories_data:
            cat = Category(user_id=admin.id, name=name)
            db.add(cat)
            categories.append(cat)
        
        db.commit()
        for c in categories:
            db.refresh(c)
            
        print("Adding sample transactions...")
        import random
        
        txns = []
        
        # Consistent big incomes
        for i in range(3):
            # Salary once a month for the last 3 months
            date = datetime.now() - timedelta(days=(i * 30) + 2)
            txns.append(Transaction(user_id=admin.id, category_id=categories[0].id, amount=5500.0, type="income", date=date, notes="Monthly Salary"))
            
            # Rent once a month
            txns.append(Transaction(user_id=admin.id, category_id=categories[2].id, amount=1500.0, type="expense", date=date + timedelta(days=1), notes="Monthly Rent"))
            
            # Utilities once a month
            txns.append(Transaction(user_id=admin.id, category_id=categories[3].id, amount=random.uniform(90.0, 180.0), type="expense", date=date + timedelta(days=3), notes="Electric/Water Bill"))

        # Random freelance incomes
        for _ in range(5):
             date = datetime.now() - timedelta(days=random.randint(1, 90))
             txns.append(Transaction(user_id=admin.id, category_id=categories[1].id, amount=random.uniform(200.0, 1000.0), type="income", date=date, notes="Side Hustle / Client Work"))
             
        # Scrape expenses
        expense_cats = categories[4:] # Food, Transport, Entertainment, Shopping
        for _ in range(50):
            date = datetime.now() - timedelta(days=random.randint(1, 90))
            cat = random.choice(expense_cats)
            # Make the expenses realistic
            amount = random.uniform(10.0, 150.0) 
            notes = f"Random {cat.name} transaction"
            txns.append(Transaction(user_id=admin.id, category_id=cat.id, amount=round(amount, 2), type="expense", date=date, notes=notes))
        
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
