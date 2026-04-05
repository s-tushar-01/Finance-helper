import graphene
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.deps import get_current_user
from app.services.analytics_service import AnalyticsService

# Defined Graphene Object Types
class CategoryBreakdown(graphene.ObjectType):
    category = graphene.String()
    amount = graphene.Float()

class MonthlyTotal(graphene.ObjectType):
    month = graphene.String()
    income = graphene.Float()
    expense = graphene.Float()

class TransactionActivity(graphene.ObjectType):
    id = graphene.Int()
    amount = graphene.Float()
    type = graphene.String()
    date = graphene.String()
    notes = graphene.String()

class AnalyticsSummary(graphene.ObjectType):
    totalIncome = graphene.Float()
    totalExpenses = graphene.Float()
    balance = graphene.Float()
    categoryBreakdown = graphene.List(CategoryBreakdown)
    monthlyTotals = graphene.List(MonthlyTotal)
    recentActivity = graphene.List(TransactionActivity)

class Query(graphene.ObjectType):
    analytics = graphene.Field(AnalyticsSummary)

    def resolve_analytics(self, info):
        # We enforce authentication through FastAPI dependency before reaching root resolver.
        # Request context is passed via info.context
        request: Request = info.context["request"]
        user = info.context["user"]
        db = info.context["db"]
        
        if user.role not in ["analyst", "admin"]:
            raise Exception("Unauthorized role for analytics")
            
        summary = AnalyticsService.get_summary(db, user.id)
        
        return AnalyticsSummary(
            totalIncome=summary["total_income"],
            totalExpenses=summary["total_expenses"],
            balance=summary["current_balance"],
            categoryBreakdown=[CategoryBreakdown(**cb) for cb in summary["category_breakdown"]],
            monthlyTotals=[MonthlyTotal(**mt) for mt in summary["monthly_totals"]],
            recentActivity=[TransactionActivity(**ra) for ra in summary["recent_activity"]]
            # converting datetime to string if needed, auto-handled by graphql-core generally or we might need serialization
        )

schema = graphene.Schema(query=Query)

router = APIRouter(tags=["GraphQL"])

# Simple GraphQL endpoint handler
@router.post("/graphql")
async def graphql_endpoint(
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role not in ["analyst", "admin"]:
        raise HTTPException(status_code=403, detail="Unauthorized")
        
    data = await request.json()
    query = data.get("query")
    variables = data.get("variables")
    
    context = {"request": request, "user": current_user, "db": db}
    result = await schema.execute_async(query, context_value=context, variable_values=variables)
    
    response = {"data": result.data}
    if result.errors:
        response["errors"] = [str(err) for err in result.errors]
        
    return response

@router.get("/graphql")
async def graphql_playground():
    # Typically would render GraphiQL, simplified for this scope.
    return {"message": "Use POST for GraphQL execution. Provide JWT in Authorization header."}
