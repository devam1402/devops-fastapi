from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.core.database import init_db

app = FastAPI(
    title="FastAPI DevOps App",
    description="Production-ready FastAPI application",
    version="1.0.0"
)

# ADD CORS MIDDLEWARE - This fixes the "Failed to fetch" error
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (restrict in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.on_event("startup")
def startup_event():
    print("🚀 Starting FastAPI application...")
    init_db()
    print("✅ Startup complete")

# Include API routes
app.include_router(router)

# Root endpoint (VERY IMPORTANT for quick testing)
@app.get("/")
def root():
    return {"message": "FastAPI DevOps App is running"}

# Health check (used by Docker / Kubernetes)
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
