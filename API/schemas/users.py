from pydantic import BaseModel
from datetime import date



class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    role: str
    email: str
    gender: str
    phone: str | None = None
    date_of_birth: date


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None 
    username: str
    role: str
    email: str
    gender: str
    phone: str | None = None