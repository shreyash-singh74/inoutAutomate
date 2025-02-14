import random
import hashlib
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from config import JWT_SECRET, JWT_ALGORITHM

# Generate OTP (6-digit)
def generate_otp():
    return str(random.randint(100000, 999999))

# Hash OTP (for security)
def hash_otp(otp):
    return hashlib.sha256(otp.encode()).hexdigest()

# Verify OTP
def verify_otp(input_otp, stored_hashed_otp):
    return hash_otp(input_otp) == stored_hashed_otp

# Generate JWT Token
def create_jwt_token(email: str, expires_delta: timedelta = timedelta(hours=1)):
    """Generate a JWT token using email as 'sub'."""
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": email,  # ✅ Store email instead of user ID
        "exp": expire
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


# Decode JWT Token
def decode_jwt_token(token: str):
    """Decode JWT token and return the payload."""
    try:
        decoded_payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Get JWT Token from Cookie
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return decode_jwt_token(token)