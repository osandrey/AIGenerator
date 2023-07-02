from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class QuestionModel(BaseModel):
    response: str = Field(max_length=200)
    language: str = Field(max_length=4, default='uk')

    class Config:
        orm_mode = True

# class QuestionResponseModel(BaseModel):
#     response: str = Field(max_length=3200)
#
#     class Config:
#         orm_mode = True


class QuestionResponse(BaseModel):
    response: str = Field(max_length=3200)
    question: str = Field(max_length=200)
    user_id: int


    class Config:
        orm_mode = True


class QuestionUpdate(BaseModel):
    response: str = Field(max_length=3200)
    question: str = Field(max_length=200)
    user_id: int


class UserModel(BaseModel):
    username: str = Field(min_length=2, max_length=40)
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)
    age: int
    sex: str
    interests: str

class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str
    age: int
    sex: str
    interests: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
