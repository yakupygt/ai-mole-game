from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import game

app = FastAPI(
    title="AI Mole Game API",
    description="Yapay Zeka Köstebek Oyunu Backend API",
    version="1.0.0"
)

# CORS for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://*.vercel.app",
        "*"  # For development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(game.router)


@app.get("/")
async def root():
    return {
        "message": "AI Mole Game API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
