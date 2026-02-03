from dotenv import load_dotenv
import os

# Load the .env file manually
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .api.v1.router import api_router
from .core.config import settings
from .utils.exceptions import AuthException, UserMismatchException, ResourceNotFoundException
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError
from .db.base import create_db_and_tables
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    await create_db_and_tables()
    yield
    # Cleanup on shutdown if needed

app = FastAPI(
    title="Todo API",
    description="FastAPI backend for the Todo application",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://hackathone2-tau.vercel.app",
        "https://hackathone2-kpsg7b73a-farheenzehra99s-projects.vercel.app",
        "https://hackathone2-2q98psw1t-farheenzehra99s-projects.vercel.app",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    # expose_headers=["Access-Control-Allow-Origin"]
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")
for route in app.routes:
    print(route.path)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.warning(f"HTTP error {exc.status_code}: {exc.detail}")

    error_code_map = {
        400: "VALIDATION_ERROR",
        401: "AUTH_INVALID_CREDENTIALS",
        403: "AUTH_INSUFFICIENT_PERMISSIONS",
        404: "RESOURCE_NOT_FOUND",
        409: "RESOURCE_CONFLICT",
        422: "VALIDATION_UNPROCESSABLE_ENTITY"
    }

    error_code = error_code_map.get(exc.status_code, f"HTTP_{exc.status_code}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": error_code,
                "message": exc.detail
            }
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors()
            }
        }
    )

@app.exception_handler(AuthException)
async def auth_exception_handler(request: Request, exc: AuthException):
    logger.warning(f"Auth error: {exc.message}")

    return JSONResponse(
        status_code=401,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )

@app.exception_handler(UserMismatchException)
async def user_mismatch_exception_handler(request: Request, exc: UserMismatchException):
    logger.warning(f"User mismatch error: {exc.message}")

    return JSONResponse(
        status_code=403,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message
            }
        }
    )

@app.exception_handler(ResourceNotFoundException)
async def resource_not_found_exception_handler(request: Request, exc: ResourceNotFoundException):
    logger.info(f"Resource not found: {exc.resource_type} with ID {exc.resource_id}")

    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.args[0]
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)

    # Log sensitive information only in development
    error_response = {
        "success": False,
        "error": {
            "code": "SYSTEM_INTERNAL_ERROR",
            "message": "An unexpected error occurred"
        }
    }

    # Include error details in development mode
    if settings.DEBUG:
        error_response["error"]["details"] = {
            "type": type(exc).__name__,
            "message": str(exc)
        }

    return JSONResponse(
        status_code=500,
        content=error_response
    )
