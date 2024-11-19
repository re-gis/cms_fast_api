from pydantic import BaseModel
from typing import Optional

class CustomUserBase(BaseModel):
    email: str
    username: str

class CustomUserCreate(CustomUserBase):
    password: str
    role: str

class CustomUserResponse(CustomUserBase):
    id: int
    role: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    role: str
    token: str

    class Config:
        orm_mode = True  

class ErrorResponse(BaseModel):
    error: str
    
class LoginResponse(BaseModel):
    token: str
    
class RegisterUserResponse(BaseModel):
    message: str