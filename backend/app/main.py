from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.api.v1.auth import router as auth_router
from app.api.v1.consents import router as consent_router
from app.api.v1.alerts import router as alert_router # NEW
from app.tasks.notification_tasks import send_test_email_task

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.connect() as conn:
            print("✅ Successfully connected to PostgreSQL!")
    except Exception as e:
        print(f"❌ Failed to connect to PostgreSQL: {e}")
    yield
    await engine.dispose()

app = FastAPI(
    title="Kinetic Guard API",
    version="3.0.0",
    description="Backend for the Kinetic Guard Safety System",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(consent_router, prefix="/api/v1")
app.include_router(alert_router, prefix="/api/v1") # NEW

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "3.0.0"}

@app.post("/api/test-celery")
async def trigger_celery_test(email: str = "test@example.com"):
    task = send_test_email_task.delay(email)
    return {"message": "Task sent to mailroom!", "task_id": task.id}