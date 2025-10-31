"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.routers import categories, products, list, purchase, sync, meals, shopping_events, supermarkets

load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Groceries API",
    description="REST API for managing shopping lists and products",
    version="1.0.0"
)

# Configure CORS
origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://192.168.178.123:5173,https://shopping.dromsjelhome.com"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(supermarkets.router, prefix="/api/supermarkets", tags=["supermarkets"])
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(list.router)
app.include_router(purchase.router)
app.include_router(sync.router)
app.include_router(meals.router)
app.include_router(shopping_events.router)


@app.get("/health")
def health_check():
    """Health check endpoint for Docker healthcheck."""
    return {"status": "healthy"}


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Groceries API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8080"))
    reload = os.getenv("API_RELOAD", "false").lower() == "true"
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload
    )
