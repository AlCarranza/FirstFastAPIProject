
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.user import fake_user_db
from core.security import create_access_token

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/token")
def login(data: LoginRequest):

    user = fake_user_db.get(data.username)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if user["password"] != data.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid Credentials"
        )
    
    token = create_access_token(
        {"sub": user["username"]}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
