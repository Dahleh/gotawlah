from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ARRAY
from sqlalchemy.sql.sqltypes import TIMESTAMP, DateTime
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.orm import relationship



class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer,primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    image = Column(String, nullable=False, server_default="Image Not Found")
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    parent_id = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    # updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_onupdate=text('NOW()'), server_default=text('NOW()'))

class Resturant(Base):
    __tablename__ = "resturants"

    id = Column(Integer,primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    Images = Column(ARRAY(String), server_default="{}")
    logo = Column(String, nullable=False, server_default="Image Not Found")
    menu = Column(String, nullable=False, server_default="PDF")
    timings = Column(String, nullable=False, server_default="24h")
    location = Column(String, nullable=False, server_default="maps.google.com")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    # updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_onupdate=text('NOW()'), server_default=text('NOW()'))



class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resturant_id = Column(Integer, ForeignKey("resturants.id"), nullable=False)
    valid = Column(Boolean, nullable=False, server_default="FALSE")
    time = Column(DateTime, nullable=False, server_default=text('NOW()'))
    people_count = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    user = relationship("User")
    resturant = relationship("Resturant")
    # updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_onupdate=text('NOW()'), server_default=text('NOW()'))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False, server_default="user")
    verified = Column(Boolean, nullable=False, server_default="FALSE")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    # updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_onupdate=text('NOW()'), server_default=text('NOW()'))

class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True, nullable=False)
    image = Column(String, nullable=False, server_default="Image Not Found")
    published = Column(Boolean, server_default='TRUE', nullable=False)
    resturant_id = Column(Integer, ForeignKey("resturants.id"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    # updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_onupdate=text('NOW()'), server_default=text('NOW()'))


class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer,primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, server_default="0")
    otp = Column(String, nullable=False, server_default="123")
    valid = Column(Boolean, nullable=False, server_default="FALSE")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer,primary_key=True, nullable=False)
    resturant_id = Column(Integer, ForeignKey("resturants.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resturant = relationship("Resturant")
    user = relationship("User")


