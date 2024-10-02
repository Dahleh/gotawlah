from typing import List
from .. import models, schemas, utils, oauth2
from fastapi import  status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db


router = APIRouter(
    prefix = "/bookings",
    tags=['bookings']
)

@router.get("/user/{id}", response_model=List[schemas.Booking])
def get_user_bookings(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    bookings = db.query(models.Booking).filter(models.Booking.user_id == id and models.Booking.valid == True).all()

    return bookings

@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    newBook = models.Booking(user_id = current_user.id, **booking.model_dump())
    db.add(newBook)
    db.commit()
    db.refresh(newBook)

    return newBook