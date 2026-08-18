from fastapi import Request
from fastapi.responses import JSONResponse


# Exception handler must be async - Fastapi requirement 
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled error: {exc}") # Temporary
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})