from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import JWTError, jwt

# Schama
from app.schema.users import UserInDB

# Model
from app.model.users import User as UserModel

from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str, db):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str, db):
    # user = get_user(username, db)
    user = db.query(UserModel).filter(UserModel.username == username).first()
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

