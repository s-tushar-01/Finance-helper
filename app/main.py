from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.exceptions import setup_exception_handlers
from app.db.database import engine, Base

from app.routes import auth, users, categories, transactions, analytics, graphql

# Initialize DB tables (for real-world, use Alembic migrations)
Base.metadata.create_all(bind=engine)

# Setup Logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize FastAPI App
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Finance Backend API with strict RBAC, data ownership and advanced queries.",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
setup_exception_handlers(app)

# Include Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(analytics.router)
app.include_router(graphql.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "app": settings.PROJECT_NAME}

logger.info("Application started and routes registered.")
