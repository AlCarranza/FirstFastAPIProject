# 1. Import fastapi
from fastapi import FastAPI
# Extra: Use of pydantic
from pydantic import BaseModel, EmailStr, Field

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

# 3. Create my endpoints
@app.get("/")
def read_root():
    return {"message": "Hello World"}

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

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    return users_db.get(user_id)

