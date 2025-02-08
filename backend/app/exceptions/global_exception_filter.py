import logging

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError


# Global exception handler
async def global_exception_handler(request: Request, exc: Exception):
    # Log the error
    logging.error(f"Exception occurred: {str(exc)}")

    # Handle specific exceptions
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail},
        )

    elif isinstance(exc, ValueError):
        return JSONResponse(
            status_code=400,
            content={"error": "Bad request", "details": str(exc)},
        )

    elif isinstance(exc, ValidationError):
        return JSONResponse(
            status_code=422,
            content={"error": "Validation error", "details": exc.errors()},
        )
    # Fallback for all other exceptions
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )
