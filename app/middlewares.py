import logging
import time
from aiohttp import web
from .utils import decode_jwt


rate_limit = {}


@web.middleware
async def rate_limiter(request, handler):
    user_ip = request.remote
    current_time = time.time()
    if user_ip in rate_limit:
        last_request_time = rate_limit[user_ip]
        if current_time - last_request_time < 1:  # 1 request per second
            return web.Response(status=429, text="Too Many Requests")
    rate_limit[user_ip] = current_time
    return await handler(request)


@web.middleware
async def jwt_auth_middleware(request, handler):
    if request.path in ["/login", "/register"]:
        return await handler(request)

    token = request.cookies.get("token")
    if not token:
        logging.error("Token is missing")
        raise web.HTTPUnauthorized(text="Authorization header is missing or invalid")

    try:
        user_payload = decode_jwt(token)
        if "user_id" not in user_payload:
            logging.error("Token decoding failed: 'user_id' is missing")
            raise web.HTTPUnauthorized(text="Invalid token payload")
        request["user_id"] = user_payload["user_id"]
    except Exception as e:
        logging.error(f"Token decoding failed: {e}")
        raise web.HTTPUnauthorized(text=str(e))
    print(user_payload)
    return await handler(request)
