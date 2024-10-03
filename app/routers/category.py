from typing import List
from .. import models, schemas, utils, oauth2
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db


router = APIRouter(
    prefix = "/categories",
    tags=['categories']
)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_category = models.Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return  new_category

@router.get("/", response_model=List[schemas.Category])
def all_main_categories(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    categories = db.query(models.Category).filter(models.Category.published == True and models.Category.parent_id is None).all()
    return categories


@router.get("/{id}", response_model=List[schemas.Category])
def get_child_categories(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    categories = db.query(models.Category).filter(models.Category.parent_id == id and models.Category.published == True).all()
    return categories


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_category(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    category_query = db.query(models.Category).filter(models.Category.id == id)
    category = category_query.first()
    if category  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Category with id = {id} does not exits")
    
    category_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Category)
def updatePost(id: int, updatedCategory: schemas.CategoryCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    category_query = db.query(models.Category).filter(models.Category.id == id)
    category = category_query.first()
    if category == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Category with id = {id} does not exits")
    
    category_query.update(updatedCategory.model_dump(), synchronize_session=False)
    db.commit()
    return  category_query.first()
