import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ResponseTimeMiddleware(BaseHTTPMiddleware):
    """
    Middleware para registrar el tiempo de respuesta de cada request.
    """
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # registrar el tiempo de inicio
        start_time = time.time()
        
        # procesar la request
        response = await call_next(request)
        
        # calcular el tiempo de respuesta
        process_time = time.time() - start_time
        
        # Agrega el header con el tiempo de respuesta
        response.headers["X-Process-Time"] = str(process_time)
        
        # logging del request
        logger.info(
            f"Path: {request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Duration: {process_time:.4f}s"
        )
        
        return response
