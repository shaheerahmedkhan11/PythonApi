from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from datetime import datetime


class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class PostCreate(Post):
    pass


class PostUpdate(Post):
    pass


class ResponsePost(Post):
    id: int
    user_id: int
    created_at: datetime
    owner: "ResponseUser"

    class ConfigDict:
        from_attributes = True


class PostOut(BaseModel):
    Post: ResponsePost
    votes: int

    class ConfigDict:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class ConfigDict:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
