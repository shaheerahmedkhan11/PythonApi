from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from psycopg2 import IntegrityError
from app import models
from ..database import engine, get_db
from sqlalchemy.orm import Session
from app import schemas, utils

router = APIRouter(tags=["Users"])


@router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=schemas.ResponseUser
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    new_user = models.User(email=user.email, password=hashed_password)
    db.add(new_user)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
        
    db.refresh(new_user)
    return new_user


@router.get("/users/{id}", response_model=schemas.ResponseUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found",
        )
    return user
