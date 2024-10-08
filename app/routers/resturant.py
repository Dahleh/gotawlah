from io import BytesIO
from typing import List

import boto3.resources
from .. import models, schemas, utils, oauth2
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db
from fastapi import UploadFile, File
import boto3

router = APIRouter(
    prefix = "/resturants",
    tags=['resturants']
)


@router.get("/", response_model=List[schemas.Resturant])
def all_resturants(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    resturants = db.query(models.Resturant).filter(models.Resturant.published == True).all()
    return resturants



@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Resturant)
def create_resturant(resturant: schemas.ResturantCreate, logo_upload: UploadFile = File(...),pdf_upload:UploadFile = File(...), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    logo_url =  utils.upload_image(logo_upload)
    pdf_url = utils.upload_image(pdf_upload)
    # images_list = utils.upload_multi_images(images)
    new_resturant = models.Resturant(logo = logo_url,menu = pdf_url, **resturant.model_dump())
    db.add(new_resturant)
    db.commit()
    db.refresh(new_resturant)
    return  new_resturant

@router.get("/{id}", response_model=schemas.Resturant)
def get_resturant(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
def update_resturant(id: int, updatedResturant: schemas.ResturantCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    resturant_query = db.query(models.Resturant).filter(models.Resturant.id == id)
    resturant = resturant_query.first()
    if resturant == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Resturant with id = {id} does not exits")
    
    resturant_query.update(updatedResturant.model_dump(), synchronize_session=False)
    db.commit()
    return  resturant_query.first()

@router.put("/uploadlogo/{id}",response_model=schemas.Resturant)
def upload_logo(id: int, logo_upload: UploadFile,db: Session = Depends(get_db)):
    logo_url =  utils.upload_image(logo_upload)
    resturant_query = db.query(models.Resturant).filter(models.Resturant.id == id)
    resturant = resturant_query.first()
    if resturant == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Resturant with id = {id} does not exits")
    
    resturant_query.update({"logo": logo_url}, synchronize_session=False)
    db.commit()
    return  resturant_query.first()

@router.put("/uploadmenu/{id}", response_model=schemas.Resturant)
def upload_menu(id: int, pdf_upload: UploadFile,db: Session = Depends(get_db)):
    pdf_url = utils.upload_image(pdf_upload)
    resturant_query = db.query(models.Resturant).filter(models.Resturant.id == id)
    resturant = resturant_query.first()
    if resturant == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Resturant with id = {id} does not exits")
    
    resturant_query.update({"menu": pdf_url}, synchronize_session=False)
    db.commit()
    return  resturant_query.first()

@router.put("/images/{id}", response_model=schemas.Resturant)
def upload_multi_images(id: int,  images: List[UploadFile], db: Session = Depends(get_db)):
    images_list = utils.upload_multi_images(images)
    resturant_query = db.query(models.Resturant).filter(models.Resturant.id == id)
    resturant = resturant_query.first()
    if resturant == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Resturant with id = {id} does not exits")
    
    resturant_query.update({"Images": images_list}, synchronize_session=False)
    db.commit()
    return  resturant_query.first()

