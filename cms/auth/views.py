from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cms.config import get_db
from cms.auth import services
from cms.auth.schemas import CustomUserCreate, RegisterUserResponse, ErrorResponse, LoginResponse, Login

router = APIRouter()

@router.post("/register", response_model=RegisterUserResponse)
def register(user: CustomUserCreate, db: Session = Depends(get_db)):
    return services.register_user(db, user)

@router.post("/login", response_model=LoginResponse, response_model_exclude_unset=True)
def login(user: Login, db: Session = Depends(get_db)):
    result = services.login_user(db, user)
    
    if isinstance(result, ErrorResponse):
        raise HTTPException(status_code=400, detail=result.error)
    
    return result
