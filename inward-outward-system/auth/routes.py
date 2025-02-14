from .schema import (
    SignUpSchema,
    LoginSchema,
    OtpSchema,
)
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import User
from fastapi import APIRouter, status, Response, Depends, Form, Request, Cookie
from config import engine
from mail import create_message
from .utils import generate_otp, hash_otp, verify_otp, create_jwt_token, decode_jwt_token
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from uuid import uuid4

authRouter = APIRouter()

# Dependency: Get DB session
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

# Send OTP via Email
async def send_otp_email(email: str, otp: str):
    html = f"""
    <h1>Your OTP is {otp}</h1>
    <p>Please use this OTP to verify your email address.</p>
    """
    subject = "Verify Your email"
    emails = [email]
    await create_message(emails, subject, html)

@authRouter.post("/signup")
async def signup(user: SignUpSchema, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.tcet_email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    otp = generate_otp()
    hashed_otp = hash_otp(otp)
    new_user = User(
        id=uuid4(),
        tcet_email=user.email,
        username=user.name,
        department=user.department,
        hashed_otp=hashed_otp,
        isEmailVerified=False,
    )
    db.add(new_user)
    db.commit()

    await send_otp_email(user.email, otp)
    return {"message": "OTP sent to email"}

@authRouter.post("/verify-otp")
async def verify_otp_endpoint(email: str = Form(...), otp: str = Form(...), db: Session = Depends(get_db), response: Response = Response()):
    user = db.query(User).filter(User.tcet_email == email).first()
    if not user or not verify_otp(otp, user.hashed_otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # If it's a new user, mark as verified
    if not user.isEmailVerified:
        user.isEmailVerified = True
        db.commit()
    # Generate JWT Token
    token = create_jwt_token(email)
    response = JSONResponse(
                content={"message": "User is now Authorized"},
                status_code=status.HTTP_200_OK,
            )
    
    response.set_cookie(
        key="access_token",
        value=token,
        max_age=3600 * 24 * 10,
        httponly=True,
        secure=False,
    )
    return response

@authRouter.post("/login")
async def login(body: LoginSchema, db: Session = Depends(get_db), response: Response = Response()):
    user = db.query(User).filter(User.tcet_email == body.email).first()
    if not user:
        return JSONResponse(
            content={"message": "Invalid Credentials"}, status_code=401
        )
    if not user.isEmailVerified:
        return JSONResponse({"message": "Email not verified"}, 401)
    
    otp = generate_otp()
    hashed_otp = hash_otp(otp)
    user.hashed_otp = hashed_otp
    db.commit()

    await send_otp_email(body.email, otp)
    response.set_cookie(key="login_email", value=body.email, httponly=True)
    return {"message": "OTP sent to email"}

@authRouter.post("/verify-login-otp")
async def verify_login_otp(request: Request, otp: str = Form(...), db: Session = Depends(get_db), response: Response = Response()):
    email = request.cookies.get("login_email")
    if not email:
        raise HTTPException(status_code=400, detail="Email not found in session")

    user = db.query(User).filter(User.tcet_email == email).first()
    if not user or not verify_otp(otp, user.hashed_otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # Generate JWT Token
    token = create_jwt_token(email)
    response = JSONResponse(
                content={"message": "User is now Authorized"},
                status_code=status.HTTP_200_OK,
            )
    
    response.set_cookie(
        key="access_token",
        value=token,
        max_age=3600 * 24 * 10,
        httponly=True,
        secure=False,
    )
    return response

@authRouter.post("/verify/{token}")
async def verify_token(token: str, response: Response):
    try:
        payload = decode_jwt_token(token)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
        # Generate new JWT Token
        new_token = create_jwt_token({"sub": email})
        response.set_cookie(key="access_token", value=new_token, httponly=True)
        print(f"New token set in cookie: {new_token}")
        return JSONResponse({"message": "User is now Authorized"})
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in verify_token: {e}")
        raise HTTPException(status_code=400, detail="Invalid token")