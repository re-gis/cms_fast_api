import bcrypt
import jwt
from datetime import datetime, timedelta
from cms.auth.models import CustomUser

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


SECRET_KEY = "your_secret_key" 
ALGORITHM = "HS256"  
ACCESS_TOKEN_EXPIRE_HOURS = 24

def generate_jwt_token(user: CustomUser) -> str:
    expiration = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    
    payload = {
        "sub": user.email,
        "exp": expiration,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token