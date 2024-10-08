from .. import models, schemas, utils, oauth2
from fastapi import  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db


router = APIRouter(
    prefix = "/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashedPassword = utils.hash(user.password)
    user.password = hashedPassword
    newUser = models.User(**user.model_dump())
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return  newUser


@router.get("/", response_model=schemas.UserOut)
def get_user(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id: {id} was not found")
    return user

@router.put("/{id}", response_model=schemas.UserOut)
def update_user(id: int, userUpdated: schemas.UserUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id = {id} does not exits")
    user_query.update(userUpdated.model_dump(), synchronize_session=False)
    db.commit()
    return  user_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id = {id} does not exits")
    # if user.id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User is Forbidden")
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

