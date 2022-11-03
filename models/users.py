from pydantic import BaseModel, EmailStr
from typing import List, Optional
from models.events import Event
from beanie import Document, Link


class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[Event]]

    class Settings:
        name = "users"

        class Config:
            schema_extra = {
                "example": {
                    "email": "vast_lover@gmail.com",
                    "password": "Some Name",
                    "events": []
                }
            }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "whatever@gmail.com",
                "password": "some password"
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# dict_format = {}
# sign_in = User(email="trysomething@gmail.com", password="itself")
# dict_format[sign_in.email] = sign_in.dict()
# # print(dict_format.keys())
# if dict_format[sign_in.email] in dict_format:
# print(dict_format[sign_in.email])
