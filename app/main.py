from fastapi import  FastAPI
import psycopg
from psycopg.rows import dict_row
import time
from . import models
from .database import engine
from .routers import resturant, category, booking, user, auth, favorite
from .config import settings



# models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(resturant.router)
app.include_router(category.router)
app.include_router(booking.router)
app.include_router(favorite.router)

@app.get("/")
async def root():
    return {"message": settings.database_name}


