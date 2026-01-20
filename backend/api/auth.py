from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from models.users import User
from schemas.user_schema import UserCreate, UserOut, Token
from core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    # Check if user already exists
    print("Registering user with email:", user_data.password, user_data.email)
    user_exists = await User.filter(email=user_data.email).exists()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and save user
    hashed_pwd = get_password_hash(user_data.password)
    print("Hashed password:", hashed_pwd)
    user = await User.create(
        email=user_data.email,
        hashed_password=hashed_pwd
    )
    return user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(email=form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

# backend/api/auth.py (Add this to the bottom)
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = await User.get_or_none(email=email)
    if user is None:
        raise credentials_exception
    return user

# Add this function to existing auth.py

async def get_current_user_ws(token: str) -> User:
    """
    Verify user for WebSocket connections
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        
        user = await User.get_or_none(email=email)
        return user
    except:
        return None
