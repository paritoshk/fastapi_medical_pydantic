import sys
import json
import uuid
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

from loguru import logger
from fastapi import Request, Response
from fastapi.routing import APIRoute

from app.core.config import settings

# Configure loguru logger
def setup_logging():
    # Remove default handler
    logger.remove()
    
    # Add console handler with level from settings
    logger.add(
        sys.stderr,
        level=settings.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    # Add file handler for all logs
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)
    
    logger.add(
        log_path / "updoc.log",
        rotation="20 MB",
        retention="14 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    )
    
    # Add file handler for errors only
    logger.add(
        log_path / "errors.log",
        rotation="10 MB",
        retention="30 days",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    )
    
    return logger

# Custom route class to log requests and responses
class LoggingRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()
        
        async def custom_route_handler(request: Request) -> Response:
            request_id = str(uuid.uuid4())
            start_time = datetime.utcnow()
            
            # Create a log record that will be updated with response info
            log_record: Dict[str, Any] = {
                "request_id": request_id,
                "timestamp": start_time.isoformat(),
                "method": request.method,
                "path": request.url.path,
                "client_ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent", ""),
            }
            
            # Add query params and headers (excluding sensitive info)
            log_record["query_params"] = dict(request.query_params)
            
            # Log non-sensitive headers
            sanitized_headers = {}
            for key, value in request.headers.items():
                if key.lower() not in ["authorization", "cookie", "x-api-key"]:
                    sanitized_headers[key] = value
            log_record["headers"] = sanitized_headers
            
            # Try to log request body for specific content types, while avoiding binary data
            content_type = request.headers.get("content-type", "")
            if "application/json" in content_type:
                try:
                    body = await request.body()
                    if body:
                        log_record["request_body"] = json.loads(body)
                except Exception:
                    log_record["request_body"] = "Error parsing request body"
            
            logger.info(f"Incoming request: {request.method} {request.url.path} (ID: {request_id})")
            
            # Process the request and capture response
            try:
                response = await original_route_handler(request)
                status_code = response.status_code
                
                # Add response info to log record
                log_record["status_code"] = status_code
                log_record["response_time_ms"] = (datetime.utcnow() - start_time).total_seconds() * 1000
                
                # Log non-error responses at INFO level, errors at ERROR level
                if status_code < 400:
                    logger.info(f"Request {request_id} completed: {status_code}")
                else:
                    logger.error(f"Request {request_id} error: {status_code}")
                    
                return response
            except Exception as exc:
                # Log exceptions
                log_record["exception"] = str(exc)
                log_record["response_time_ms"] = (datetime.utcnow() - start_time).total_seconds() * 1000
                logger.error(f"Request {request_id} exception: {str(exc)}")
                raise
            
        return custom_route_handler