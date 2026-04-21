from fastapi import APIRouter
from models import UserCreate, UserLogin
from auth import create_token

router = APIRouter(prefix="/api/user")

fake_users = []

@router.post("/register")
def register(user: UserCreate):
    fake_users.append(user)
    return {"msg": "User created"}

@router.post("/login")
def login(user: UserLogin):
    for u in fake_users:
        if u.username == user.username and u.password == user.password:
            token = create_token({"sub": u.username})
            return {"access_token": token}
    return {"error": "Login gagal"}