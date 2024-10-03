from typing import List
from .. import models, schemas, utils, oauth2
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db


router = APIRouter(
    prefix = "/bookings",
    tags=['bookings']
)

@router.get("/user", response_model=List[schemas.Booking])
def get_user_bookings(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    bookings = db.query(models.Booking).filter(models.Booking.user_id == current_user.id and models.Booking.valid == True).all()

    return bookings

# Get specfic booking

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_booking = models.Booking(user_id = current_user.id, **booking.model_dump())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    booking_query = db.query(models.Booking).filter(models.Booking.id == id)
    booking = booking_query.first()
    if booking  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with id = {id} does not exits")
    booking_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Booking)
def update_booking(id: int,udpatedBooking: schemas.BookingUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    booking_query = db.query(models.Resturant).filter(models.Resturant.id == id)
    booking = booking_query.first()
    if booking == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Booking with id = {id} does not exits")
    
    booking_query.update(udpatedBooking.model_dump(), synchronize_session=False)
    db.commit()
    return  booking_query.first()
    