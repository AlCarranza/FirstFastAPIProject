# 1. Import fastapi
from fastapi import APIRouter, HTTPException

from models.user import (
    UserCreate,
    UserResponse,
    UserUpdate
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

users_db = {}
current_id = 1

# 3. Create my endpoints

# ------------
# READ
# ------------
# response_model ensures validate and serialization, where:
# - Validate is if UserResponse not include password then if it is include it FastAPI, PyDantic removes it
# - Serialization is transform python objects in JSON format
# Query params: Come after ? in the form of /users?skip=1&limit=10
@router.get("/", response_model=list[UserResponse])
def get_users(skip: int=0, limit: int = 10):
    users = list(users_db.values())

    return users[skip:skip+limit]

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    
    user = users_db.get(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return user

# ------------
# CREATE
# ------------
# It is important to mention that response_model from FastAPI validate output, filter fields and generate docs
# for example: password if for error is writen, it is not returned
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    global current_id

    new_user = {
        "id": current_id,
        **user.model_dump()
    }

    users_db[current_id] = new_user
    current_id += 1

    return new_user

# ------------
# UPDATE
# ------------
@router.put("/{user_id}", response_model=UserResponse)
def update_users(user_id: int, user_update: UserUpdate):

    user = users_db.get(user_id)

    if not user:
        raise HTTPException(
            status_code= 400,
            detail="User not found"
        )
    
    # only update the provided fields
    # model_dump builds a dictionary from the pydantic Model
    update_data = user_update.model_dump(exclude_unset=True)

    user.update(update_data)

    users_db[user_id] = user

    return user

# ------------
# DELETE
# ------------
@router.delete("/{user_id}")
def delete_user(user_id: int):

    user = users_db.get(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    del users_db[user_id]

    return {
        "message": f"User {user_id} deleted successfully"
    }
