from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional




class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone: str
    first_name: str
    last_name: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    phone: str
    first_name: str
    last_name: str
    created_at: datetime

class Category(BaseModel):
    id: int
    name: str
    content: str
    published: bool
    created_at: datetime

class CategoryCreate(BaseModel):
    name: str
    content: str
    published: bool

class Resturant(BaseModel):
    id: int
    name: str
    description: str
    published: bool
    category_id: int
    Images: List[str]
    logo: str
    menu: str
    timings: str
    location: str
    created_at: datetime

class ResturantCreate(BaseModel):
    name: str
    description: str
    published: bool
    category_id: int

class ResturantList(BaseModel):
    id: int
    name: str
    LogoImage: str

class Booking(BaseModel):
    id: int
    user_id: int
    resturant_id: int
    valid: bool
    time: datetime
    people_count: int
    created_at: datetime

class BookingCreate(BaseModel):
    resturant_id: int
    valid: bool
    time: datetime
    people_count: int

class Banner(BaseModel):
    id:int
    published: bool
    image: str
    resturant_id: int
    created_at: datetime


class OTP(BaseModel):
    id: int
    user_id: int
    otp: str
    valid: bool

class Favorite(BaseModel):
    id: int
    resturant_id: int
    user_id: int


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None