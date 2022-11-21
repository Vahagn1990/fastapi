from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Request and Response model for Post creating/updating/getting API
class PostBase(BaseModel): # BASE model
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase): # Create post body
    pass

class UserCreate(BaseModel): # Create USER body
    email: EmailStr
    password: str

class ResponseCreateUser(BaseModel): # Respone of created USER
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostResponse(PostBase): # Respone of created post
    id: int
    created_at: datetime
    owner_id : int
    owner : ResponseCreateUser

    class Config:
        orm_mode = True # To be able to convert the response from SQL into JSON (for pydentic mode, in this case for response)

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Request and Response model for User Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)