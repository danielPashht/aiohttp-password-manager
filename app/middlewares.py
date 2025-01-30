from aiohttp import web
from .utils import decode_jwt
import logging


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
