from typing import List
from .. import models, schemas, utils, oauth2
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db


router = APIRouter(
    prefix = "/resturants",
    tags=['resturants']
)

@router.get("/", response_model=List[schemas.Resturant])
def all_resturants(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    resturants = db.query(models.Resturant).filter(models.Resturant.published == True).all()
    return resturants


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Resturant)
def create_resturant(resturant: schemas.ResturantCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_resturant = models.Resturant(**resturant.model_dump())
    db.add(new_resturant)
    db.commit()
    db.refresh(new_resturant)
    return  new_resturant

@router.get("/{id}", response_model=schemas.Resturant)
def get_resturant(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,
    #                 (str(id), ))
    # post = cursor.fetchone()
    resturant = db.query(models.Resturant).filter(models.Resturant.id == id and models.Resturant.published == True).first()
    if not resturant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Resturant with id: {id} was not found")
    return resturant

@router.get("/category/{id}", response_model=List[schemas.Resturant])
def get_resturant_by_category(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    resturants = db.query(models.Resturant).filter(models.Resturant.category_id == id and models.Resturant.published == True).all()
    return resturants

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resturant(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    resturant_query = db.query(models.Resturant).filter(models.Resturant.id == id)
    resturant = resturant_query.first()
    if resturant  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resturant with id = {id} does not exits")
    
    resturant_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Resturant)
def updatePost(id: int, updatedResturant: schemas.ResturantCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    resturant_query = db.query(models.Resturant).filter(models.Resturant.id == id)
    resturant = resturant_query.first()
    if resturant == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Resturant with id = {id} does not exits")
    
    resturant_query.update(updatedResturant.model_dump(), synchronize_session=False)
    db.commit()
    return  resturant_query.first()

