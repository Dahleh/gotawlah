from datetime import datetime
from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Optional
import json



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

class UserUpdate(BaseModel):
    phone: str
    first_name: str
    last_name: str

class Category(BaseModel):
    id: int
    name: str
    content: str
    image: str
    published: bool
    parent_id: int
    created_at: datetime

class CategoryCreate(BaseModel):
    name: str
    content: str
    parent_id: int = 0
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
    timings: str = "24h"
    location: str = "maps.google.com"

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
    

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
    user: UserOut
    resturant: Resturant

class BookingCreate(BaseModel):
    resturant_id: int
    valid: bool
    time: datetime = datetime.now()
    people_count: int

class BookingUpdate(BaseModel):
    valid: bool
    time: datetime
    people_count: int

class Banner(BaseModel):
    id:int
    published: bool
    image: str
    resturant_id: int
    created_at: datetime

class BannerCreate(BaseModel):
    resturant_id: int
    published: bool

class OTP(BaseModel):
    id: int
    user_id: int
    otp: str
    valid: bool

class Favorite(BaseModel):
    id: int
    resturant_id: int
    user_id: int

class FavoriteCreate(BaseModel):
    resturant_id: int

class FavoriteOut(BaseModel):
    resturant_id: int
    resturant: Resturant
    user: UserOut

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None