from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET = "201232A2jjG15g21532ophThjsn47863s15s4961fd5s41bnmv45gfb5sdfgf1"
router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


# Entidad users
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

class UserDB(User):
    password: str


users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@api.com",       
        "disable": False,
        "password": "$2a$12$BFHNuZon/Ei/sdEWuFPko.frzATYXRJjlZ26RT2VmY/ZlW/7wHjEe"
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderland",
        "email": "alice@api.com",
        "disable": False,
        "password": "$2a$12$kPtne.8aPC.Il8QP09NxPuSEI5xxAUfEP8Z5OxG9RgWFrCvTvYLZi"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    return None

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    return None

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = search_user_db(form.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username")

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,detail="Incorrect password")

    access_token = {"sub": user.username, "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES-60)} # se le resta 60 ya que now da la hora actual pero no UTC

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    
    return user

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
