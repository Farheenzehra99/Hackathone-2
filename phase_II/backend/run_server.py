import uvicorn
import asyncio
import sys
import os

# Add the backend directory to the path so we can import from app
sys.path.append(os.path.join(os.path.dirname(__file__)))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )