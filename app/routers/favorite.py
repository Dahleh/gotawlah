from typing import List
from .. import models, schemas, utils, oauth2
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db


router = APIRouter(
    prefix = "/favorite",
    tags=['Favorite']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Favorite)
def add_favorite(favorite: schemas.FavoriteCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_favorite = models.Favorite(user_id = current_user.id, **favorite.model_dump())
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)
    return new_favorite


@router.get("/", response_model=List[schemas.FavoriteOut])
def get_favorite(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    favorites = db.query(models.Favorite).filter(models.Favorite.user_id == current_user.id).all()
    return favorites

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    favorite_query = db.query(models.Favorite).filter(models.Favorite.id == id)
    favorite = favorite_query.first()
    if favorite  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Favorite with id = {id} does not exits")
    
    favorite_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




