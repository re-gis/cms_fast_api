from sqlalchemy.orm import Session
from cms.auth.models import CustomUser
from cms.auth.schemas import CustomUserCreate
from cms.utils import hash_password, generate_jwt_token
from passlib.context import CryptContext
from .schemas import ErrorResponse, LoginResponse, RegisterUserResponse
from fastapi import HTTPException, status




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def register_user(db: Session, user: CustomUserCreate):
    db_user = db.query(CustomUser).filter(CustomUser.email == user.email).first()
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    db_user_email = db.query(CustomUser).filter(CustomUser.username == user.username).first()
    if db_user_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this name already exists.")
    
    role = user.role if user.role else "volunteer"
    
    db_user = CustomUser(
        email=user.email,
        username=user.username,
        password_hash=hash_password(user.password),
        role=role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return RegisterUserResponse(message="User registered successfully, login to continue.")



def login_user(db: Session, user: CustomUserCreate):
    db_user = db.query(CustomUser).filter(CustomUser.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        return ErrorResponse(error="Invalid email or password")

    token = generate_jwt_token(db_user)

    return LoginResponse(
        token=token
    )
