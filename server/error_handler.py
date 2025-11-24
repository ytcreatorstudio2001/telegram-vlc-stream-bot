import logging
import traceback
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class AIErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            # Capture the full traceback
            tb_str = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            
            # Analyze the error (Simple AI Simulation)
            diagnosis = "Unknown Error"
            recommendation = "Check logs for details."
            
            if "FileMigrate" in str(exc) or "FILE_MIGRATE" in str(exc):
                diagnosis = "Data Center Migration Error"
                recommendation = "The file is on a different server (DC). The bot attempted to switch DCs but failed."
            elif "AUTH_KEY_UNREGISTERED" in str(exc):
                diagnosis = "Authentication Key Error"
                recommendation = "The bot's session key is invalid for the current DC. Re-login or session regeneration required."
            elif "Client has not been started yet" in str(exc):
                diagnosis = "Client State Error"
                recommendation = "The Pyrogram client is disconnected or wasn't started properly before use."
            elif "FloodWait" in str(exc):
                diagnosis = "Telegram Rate Limit"
                recommendation = "Too many requests. The bot must wait before retrying."
            
            # Log the structured report
            log_report = (
                f"\n{'='*40}\n"
                f"🚨 AI ERROR DIAGNOSIS SYSTEM 🚨\n"
                f"{'='*40}\n"
                f"📍 Request: {request.method} {request.url}\n"
                f"❌ Error Type: {type(exc).__name__}\n"
                f"💬 Message: {str(exc)}\n"
                f"🧐 Diagnosis: {diagnosis}\n"
                f"💡 Recommendation: {recommendation}\n"
                f"{'-'*40}\n"
                f"📜 Traceback:\n{tb_str}\n"
                f"{'='*40}\n"
            )
            
            # Print to stdout/logs so it appears in Koyeb
            print(log_report)
            logger.error(log_report)
            
            # Re-raise to let FastAPI handle the 500 response
            raise exc
