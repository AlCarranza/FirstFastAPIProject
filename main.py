# 1. Import fastapi
from fastapi import FastAPI, HTTPException
# Extra: Use of pydantic
from pydantic import BaseModel, EmailStr, Field

from typing import Optional

# 2. Create the instance of FastAPI
app = FastAPI()

# dict to store my data locally
users_db = {}
current_id = 1

# Create classes idealy this should go on other file
# In real backend we separte input and output. UserCreate is what client sends, UserResponse is what API returns
class UserCreate(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    age: int = Field(gt=0)
    password: str = Field(min_length=6)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    password: Optional[int] = None

# 3. Create my endpoints
@app.get("/")
def read_root():
    return {"message": "Hello World"}


# ------------
# CREATE
# ------------
# It is important to mention that response_model from FastAPI validate output, filter fields and generate docs
# for example: password if for error is writen, it is not returned
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    global current_id

    new_user = {
        "id": current_id,
        "name": user.name,
        "email": user.email,
        "age": user.age
        # password intentionally excluded
    }

    users_db[current_id] = new_user
    current_id += 1

    return new_user

# ------------
# READ
# ------------
# Query params: Come after ? in the form of /users?skip=1&limit=10
@app.get("/users", response_model=list[UserResponse])
def get_users(skip: int=0, limit: int = 10):
    users = list(users_db.values())

    return users[skip:skip+limit]

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    
    user = users_db.get(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return user

# ------------
# UPDATE
# ------------
@app.put("/users/{user_id}", response_model=UserResponse)
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

    for key, value in update_data.items():
        user[key] = value

    users_db[user_id] = user

    return user

# ------------
# DELETE
# ------------
@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    if user_id not in users_db:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    del users_db[user_id]

    return {
        "message": "User deleted successfully"
    }
