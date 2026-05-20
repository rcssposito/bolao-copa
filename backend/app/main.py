from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import users, matches, bets, ranking, admin

# Create FastAPI app
app = FastAPI(
    title="Bolão Copa API",
    description="API para sistema de bolão da Copa do Mundo",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api")
app.include_router(matches.router, prefix="/api")
app.include_router(bets.router, prefix="/api")
app.include_router(ranking.router, prefix="/api")
app.include_router(admin.router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Bolão Copa API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# For Vercel serverless deployment
handler = app

# Made with Bob
