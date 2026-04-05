from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.models.transaction import Transaction
from app.models.category import Category

class AnalyticsService:
    @staticmethod
    def get_summary(db: Session, user_id: int):
        # 1. Total income and expenses
        totals = db.query(
            Transaction.type, 
            func.sum(Transaction.amount).label("total")
        ).filter(Transaction.user_id == user_id).group_by(Transaction.type).all()
        
        total_income = 0.0
        total_expense = 0.0
        for t_type, t_total in totals:
            if t_type == "income":
                total_income = float(t_total)
            elif t_type == "expense":
                total_expense = float(t_total)
                
        balance = total_income - total_expense
        
        # 2. Category-wise breakdown (Expenses typically)
        cat_breakdown = db.query(
            Category.name, 
            func.sum(Transaction.amount).label("total")
        ).join(Transaction, Transaction.category_id == Category.id)\
         .filter(Transaction.user_id == user_id, Transaction.type == "expense")\
         .group_by(Category.name).all()
         
        category_data = [{"category": name, "amount": float(total)} for name, total in cat_breakdown]
        
        # 3. Monthly Totals
        monthly = db.query(
            extract('year', Transaction.date).label("year"),
            extract('month', Transaction.date).label("month"),
            Transaction.type,
            func.sum(Transaction.amount).label("total")
        ).filter(Transaction.user_id == user_id)\
         .group_by(extract('year', Transaction.date), extract('month', Transaction.date), Transaction.type).all()
         
        monthly_map = {}
        for y, m, t_type, t_total in monthly:
            month_str = f"{int(y)}-{int(m):02d}"
            if month_str not in monthly_map:
                monthly_map[month_str] = {"month": month_str, "income": 0.0, "expense": 0.0}
            if t_type == "income":
                monthly_map[month_str]["income"] = float(t_total)
            elif t_type == "expense":
                monthly_map[month_str]["expense"] = float(t_total)
                
        # 4. Recent Activity
        recent = db.query(Transaction).filter(Transaction.user_id == user_id)\
                   .order_by(Transaction.date.desc()).limit(10).all()
                   
        recent_data = []
        for r in recent:
            recent_data.append({
                "id": r.id,
                "amount": r.amount,
                "type": r.type,
                "date": r.date,
                "notes": r.notes
            })
            
        return {
            "total_income": total_income,
            "total_expenses": total_expense,
            "current_balance": balance,
            "category_breakdown": category_data,
            "monthly_totals": list(monthly_map.values()),
            "recent_activity": recent_data
        }
