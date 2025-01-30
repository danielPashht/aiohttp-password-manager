import logging
from datetime import datetime, timedelta

import os
import bcrypt
import jwt
import secrets
import string
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for application")


def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())


def generate_jwt(payload, expires_in=60):
    payload["exp"] = datetime.utcnow() + timedelta(minutes=expires_in)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired")
        raise
    except jwt.InvalidTokenError as e:
        logging.error(f"Invalid token: {e}")
        raise


def generate_new_password(length: int):
    return hash_password(
        "".join(secrets.choice(
            string.ascii_letters + string.digits
        ) for _ in range(length))
    )
