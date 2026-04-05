from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.api.deps import require_analyst
from app.services.analytics_service import AnalyticsService
from app.schemas.common import ResponseModel

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/summary")
# Note: Defining a specific schema model for standard analytics structure is best for docs, 
# for brevity here relying on dict through ResponseModel.
def get_analytics_summary(db: Session = Depends(get_db), current_user: User = Depends(require_analyst)):
    data = AnalyticsService.get_summary(db, current_user.id)
    return ResponseModel(data=data)
