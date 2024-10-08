from typing import List
from .. import models, schemas, utils
from fastapi import  Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from sqlalchemy.orm import Session
from ..database import  get_db

router = APIRouter(
    prefix = "/banners",
    tags=['Banners']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Banner)
def add_banner(banner: schemas.BannerCreate, image_upload: UploadFile = File(...), db: Session = Depends(get_db)):
    image_url = utils.upload_image(image_upload)
    new_banner = models.Banner(image = image_url, ** banner.model_dump())
    db.add(new_banner)
    db.commit()
    db.refresh(new_banner)
    return new_banner

@router.get("/", response_model=schemas.Banner)
def get_banners(db: Session = Depends(get_db)):
    banners = db.query(models.Banner).filter(models.Banner.published == True).all()
    return banners

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_banner(id: int, db: Session = Depends(get_db)):
    banner_query = db.query(models.Banner).filter(models.Banner.id == id)
    banner = banner_query.first()
    if banner  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Banner with id = {id} does not exits")
    
    banner_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Banner)
def update_image_banner(id: int, image_upload: UploadFile = File(...), db: Session = Depends(get_db)):
    image_url = utils.upload_image(image_upload)
    banner_query = db.query(models.Banner).filter(models.Banner.id == id)
    banner = banner_query.first()
    if banner == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Banner with id = {id} does not exits")
    
    banner_query.update({"image": image_url}, synchronize_session=False)
    db.commit()
    return  banner_query.first()