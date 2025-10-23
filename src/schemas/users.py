from pydantic import BaseModel, EmailStr, constr, Field
from uuid import UUID



class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    role: str = "admin"  # admin, catequista, etc.
    

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=72)

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: UUID

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
