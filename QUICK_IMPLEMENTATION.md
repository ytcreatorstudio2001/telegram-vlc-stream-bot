# 🚀 Quick Implementation Guide

This guide provides ready-to-use code for the **highest priority improvements** from the code review.

---

## 1. Rate Limiting (CRITICAL) 🔴

### Create: `server/rate_limiter.py`

```python
"""
Rate Limiting Middleware - Prevents API abuse
"""
import time
import logging
from collections import defaultdict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware to prevent abuse.
    Tracks requests per IP address.
    """
    
    def __init__(self, app, requests_per_minute=60, cleanup_interval=300):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.cleanup_interval = cleanup_interval
        self.requests = defaultdict(list)
        self.last_cleanup = time.time()
    
    def cleanup_old_requests(self):
        """Remove old request records to prevent memory bloat"""
        current_time = time.time()
        if current_time - self.last_cleanup > self.cleanup_interval:
            for ip in list(self.requests.keys()):
                self.requests[ip] = [
                    req_time for req_time in self.requests[ip]
                    if current_time - req_time < 60
                ]
                # Remove empty entries
                if not self.requests[ip]:
                    del self.requests[ip]
            self.last_cleanup = current_time
    
    async def dispatch(self, request: Request, call_next):
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/", "/docs", "/redoc"]:
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean old requests periodically
        self.cleanup_old_requests()
        
        # Filter requests from last minute
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < 60
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Too Many Requests",
                    "message": f"Rate limit exceeded. Maximum {self.requests_per_minute} requests per minute.",
                    "retry_after": 60
                }
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            self.requests_per_minute - len(self.requests[client_ip])
        )
        
        return response
```

### Update: `main.py`

Add this after line 88 (before `app.add_middleware(AIErrorMiddleware)`):

```python
# Add Rate Limiting Middleware
from server.rate_limiter import RateLimitMiddleware
app.add_middleware(RateLimitMiddleware, requests_per_minute=Config.RATE_LIMIT_PER_MINUTE)
```

---

## 2. Input Validation for Batch Command 🔴

### Update: `plugins/commands.py`

Replace lines 377-379 with:

```python
    total_messages = last_msg_id - first_msg_id + 1
    
    # Validate batch size
    MAX_BATCH_SIZE = Config.MAX_BATCH_SIZE
    if total_messages > MAX_BATCH_SIZE:
        await message.reply_text(
            f"❌ **Batch size too large!**\n\n"
            f"**Maximum allowed:** {MAX_BATCH_SIZE} messages\n"
            f"**Requested:** {total_messages} messages\n\n"
            f"💡 **Tip:** Split your request into smaller batches.\n\n"
            f"**Example:**\n"
            f"First batch: `/batch {first_link} https://t.me/c/{first_chat_id}/{first_msg_id + MAX_BATCH_SIZE - 1}`\n"
            f"Second batch: `/batch https://t.me/c/{first_chat_id}/{first_msg_id + MAX_BATCH_SIZE} {last_link}`"
        )
        return
    
    if total_messages <= 0:
        await message.reply_text(
            "❌ **Invalid message range!**\n\n"
            "The first message ID must be less than the last message ID."
        )
        return
```

---

## 3. Enhanced Configuration with Validation 🔴

### Update: `config.py`

Replace entire file with:

```python
"""
Telegram VLC Stream Bot - Configuration Module
Copyright (c) 2025 Akhil TG. All Rights Reserved.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()


class ConfigError(Exception):
    """Configuration validation error"""
    pass


class Config:
    # Core Telegram Settings (Required)
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    
    # Server Settings
    PORT = int(os.getenv("PORT", "8080"))
    HOST = os.getenv("HOST", "0.0.0.0")
    URL = os.getenv("URL", "http://localhost:8080")
    
    # Admin Settings
    ADMINS = [int(x) for x in os.getenv("ADMINS", "").split()] if os.getenv("ADMINS") else []
    FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL", "")
    LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0"))
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    
    # Performance Settings
    MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", "100"))
    CACHE_TTL_HOURS = int(os.getenv("CACHE_TTL_HOURS", "1"))
    MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", "1000"))
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    
    # Directory Settings
    WORK_DIR = os.getenv("WORK_DIR", "work_dir")
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        errors = []
        warnings = []
        
        # Check required fields
        if cls.API_ID == 0:
            errors.append("API_ID is required and must be a valid integer")
        
        if not cls.API_HASH:
            errors.append("API_HASH is required")
        
        if not cls.BOT_TOKEN:
            errors.append("BOT_TOKEN is required")
        
        # Check warnings
        if cls.URL == "http://localhost:8080":
            warnings.append("URL is set to localhost - update for production deployment")
        
        if not cls.DATABASE_URL:
            warnings.append("DATABASE_URL not set - using JSON file storage (not recommended for production)")
        
        if not cls.ADMINS:
            warnings.append("No ADMINS configured - admin panel will be inaccessible")
        
        if cls.LOG_CHANNEL == 0:
            warnings.append("LOG_CHANNEL not set - user activity logging disabled")
        
        # Print warnings
        if warnings:
            print("\n⚠️  Configuration Warnings:")
            for warning in warnings:
                print(f"   • {warning}")
        
        # Raise errors
        if errors:
            error_msg = "\n❌ Configuration Errors:\n" + "\n".join(f"   • {e}" for e in errors)
            error_msg += "\n\n💡 Please check your .env file and ensure all required variables are set."
            raise ConfigError(error_msg)
        
        print("✅ Configuration validated successfully\n")
    
    @classmethod
    def display_info(cls):
        """Display configuration info (without sensitive data)"""
        print("📋 Bot Configuration:")
        print(f"   • Server: {cls.HOST}:{cls.PORT}")
        print(f"   • URL: {cls.URL}")
        print(f"   • Database: {'MongoDB' if cls.DATABASE_URL else 'JSON File'}")
        print(f"   • Admins: {len(cls.ADMINS)} configured")
        print(f"   • Log Channel: {'Enabled' if cls.LOG_CHANNEL else 'Disabled'}")
        print(f"   • Max Batch Size: {cls.MAX_BATCH_SIZE}")
        print(f"   • Rate Limit: {cls.RATE_LIMIT_PER_MINUTE} req/min")
        print()


# Validate configuration on import
try:
    Config.validate()
    Config.display_info()
except ConfigError as e:
    print(e)
    print("\n🔧 Example .env file:")
    print("""
API_ID=12345
API_HASH=your_api_hash_here
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
URL=https://your-domain.com
DATABASE_URL=mongodb+srv://user:pass@cluster.mongodb.net/
ADMINS=123456789 987654321
LOG_CHANNEL=-1001234567890
    """)
    sys.exit(1)

# Create work directory
if not os.path.exists(Config.WORK_DIR):
    os.makedirs(Config.WORK_DIR)
```

---

## 4. Enhanced Health Check 🔴

### Update: `server/routes_improved.py`

Replace the health check endpoint (lines 165-172) with:

```python
@router.get("/health")
async def health_check():
    """Comprehensive health check endpoint."""
    from datetime import datetime
    import psutil
    from server.dc_manager import dc_clients
    from database import db
    
    try:
        # Calculate uptime
        import time
        uptime_seconds = time.time() - getattr(bot, 'start_time', time.time())
        
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        # Get database status
        db_status = "disconnected"
        if db:
            try:
                db_connected = await db._check_connection()
                db_status = "connected" if db_connected else "disconnected"
            except:
                db_status = "error"
        
        # Get DC client status
        dc_status = {f"dc_{dc_id}": "connected" for dc_id in dc_clients.keys()}
        
        # Get cache stats
        cache_size = 0
        try:
            from server.byte_streamer import byte_streamer
            if byte_streamer:
                cache_size = len(byte_streamer.cached_file_ids)
        except:
            pass
        
        # Determine overall health
        is_healthy = (
            bot.is_connected and
            (db_status in ["connected", "disconnected"]) and  # DB optional
            cpu_percent < 90 and
            memory.percent < 90
        )
        
        health_data = {
            "status": "healthy" if is_healthy else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": int(uptime_seconds),
            "bot": {
                "connected": bot.is_connected,
                "status": bot.boot_status if hasattr(bot, 'boot_status') else "Unknown"
            },
            "database": {
                "status": db_status,
                "type": "mongodb" if db and Config.DATABASE_URL else "json"
            },
            "system": {
                "cpu_percent": round(cpu_percent, 2),
                "memory_percent": round(memory.percent, 2),
                "memory_available_mb": round(memory.available / (1024 * 1024), 2)
            },
            "cache": {
                "file_properties_cached": cache_size
            },
            "dc_clients": dc_status
        }
        
        return health_data
    
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "error",
            "error": str(e),
            "bot_connected": bot.is_connected if bot else False
        }
```

Add this to the top of the file (after imports):

```python
# Track bot start time
if not hasattr(bot, 'start_time'):
    import time
    bot.start_time = time.time()
```

---

## 5. Improved Error Messages 🔴

### Update: `server/routes_improved.py`

Replace error handling in `stream_media` function:

```python
# Line 42-45
try:
    msg = await bot.get_messages(chat_id, message_id)
except Exception as e:
    logger.error(f"Failed to get message {message_id} from chat {chat_id}: {e}")
    raise HTTPException(
        status_code=404,
        detail={
            "error": "Message Not Found",
            "message": "The requested message could not be found. It may have been deleted or you don't have access to it.",
            "chat_id": chat_id,
            "message_id": message_id,
            "suggestion": "Please verify the message link and try again."
        }
    )

# Line 47-48
if not msg or not msg.media:
    raise HTTPException(
        status_code=404,
        detail={
            "error": "No Media Found",
            "message": "The message exists but does not contain any media files.",
            "chat_id": chat_id,
            "message_id": message_id,
            "suggestion": "Please ensure you're requesting a message with media (video, audio, or document)."
        }
    )

# Line 79-83
if start >= file_size or start < 0 or end >= file_size:
    return Response(
        status_code=416,
        headers={
            "Content-Range": f"bytes */{file_size}",
            "X-Error-Message": "Range Not Satisfiable"
        },
        content=json.dumps({
            "error": "Range Not Satisfiable",
            "message": f"Requested range {start}-{end} is invalid for file size {file_size}",
            "file_size": file_size
        })
    )
```

---

## 6. Add psutil to Requirements 🔴

### Update: `requirements.txt`

Add this line:

```
psutil
```

Final file should look like:

```
pyrogram
tgcrypto
fastapi
uvicorn
python-dotenv
requests
motor
dnspython
psutil
```

---

## 7. Update .env.sample 🔴

### Update: `.env.sample`

```env
# Telegram API Credentials (Required)
API_ID=12345
API_HASH=your_api_hash_here
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Server Configuration (Required for Production)
PORT=8080
HOST=0.0.0.0
URL=https://your-domain.com

# Database (Optional but Recommended)
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/database

# Admin Configuration (Optional)
ADMINS=123456789 987654321
FORCE_SUB_CHANNEL=@your_channel
LOG_CHANNEL=-1001234567890

# Performance Settings (Optional)
MAX_BATCH_SIZE=100
CACHE_TTL_HOURS=1
MAX_CACHE_SIZE=1000
RATE_LIMIT_PER_MINUTE=60

# Working Directory (Optional)
WORK_DIR=work_dir
```

---

## 📋 Implementation Checklist

Follow these steps in order:

### Step 1: Update Dependencies
```bash
# Add psutil to requirements.txt
echo "psutil" >> requirements.txt

# Install new dependency
pip install psutil
```

### Step 2: Create Rate Limiter
```bash
# Create the rate limiter file
# Copy the code from section 1 above
```

### Step 3: Update Config
```bash
# Update config.py with validation
# Copy the code from section 3 above
```

### Step 4: Update Main
```bash
# Add rate limiting middleware to main.py
# Add the import and middleware line from section 1
```

### Step 5: Update Commands
```bash
# Add batch validation to commands.py
# Replace the section mentioned in section 2
```

### Step 6: Update Routes
```bash
# Update health check and error messages
# Copy code from sections 4 and 5
```

### Step 7: Update Environment
```bash
# Update .env.sample
# Copy from section 7

# Update your .env file with new variables
```

### Step 8: Test
```bash
# Run the bot locally
python main.py

# Test endpoints
curl http://localhost:8080/health
curl http://localhost:8080/
```

---

## 🧪 Testing the Improvements

### Test Rate Limiting
```bash
# Send multiple requests quickly
for i in {1..70}; do curl http://localhost:8080/health; done

# Should see 429 error after 60 requests
```

### Test Batch Validation
```
# In Telegram, try:
/batch https://t.me/c/123/1 https://t.me/c/123/200

# Should get error if > 100 messages
```

### Test Health Check
```bash
curl http://localhost:8080/health | jq

# Should see detailed health information
```

### Test Configuration Validation
```bash
# Remove API_ID from .env
python main.py

# Should see validation error
```

---

## 🚀 Deployment

After implementing these changes:

1. **Commit to Git:**
```bash
git add .
git commit -m "Add rate limiting, validation, and enhanced health checks"
git push
```

2. **Update Koyeb Environment Variables:**
   - Add `MAX_BATCH_SIZE=100`
   - Add `RATE_LIMIT_PER_MINUTE=60`
   - Add `CACHE_TTL_HOURS=1`
   - Add `MAX_CACHE_SIZE=1000`

3. **Redeploy on Koyeb:**
   - Koyeb will auto-deploy from Git
   - Monitor logs for validation messages
   - Check health endpoint

4. **Monitor:**
```bash
# Check health
curl https://your-domain.com/health

# Check logs in Koyeb dashboard
```

---

## 📊 Expected Results

After implementation:

✅ **Rate limiting active** - Prevents abuse  
✅ **Batch validation** - Prevents excessive requests  
✅ **Config validation** - Catches errors early  
✅ **Better health checks** - Easier monitoring  
✅ **Improved errors** - Better user experience  

---

## 🆘 Troubleshooting

### Issue: Rate limiting too strict
**Solution:** Increase `RATE_LIMIT_PER_MINUTE` in .env

### Issue: Batch size too small
**Solution:** Increase `MAX_BATCH_SIZE` in .env

### Issue: Health check fails
**Solution:** Check if psutil is installed: `pip install psutil`

### Issue: Config validation fails
**Solution:** Check .env file has all required variables

---

## 📞 Support

If you encounter issues:
1. Check the logs
2. Verify .env configuration
3. Test locally first
4. Review error messages

---

**Ready to implement? Start with Step 1! 🚀**
