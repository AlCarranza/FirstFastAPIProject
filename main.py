# 1. Import fastapi
from fastapi import FastAPI

from routers.auth import router as auth_router

# 2. Create the instance of FastAPI
app = FastAPI()

app.include_router(auth_router)

"""
What we've learned:

    FastAPI pipeline: That’s the full backend request lifecycle.

        HTTP Request
              ↓
        FastAPI Route
              ↓
        Pydantic Validation
              ↓
        Python Objects
              ↓
        Business Logic
              ↓
        Serialization
              ↓
        JSON Response

Backend engineering is mostly:
    - moving data safely
    - validating data
    - transforming data
    - exposing data through APIs
"""
