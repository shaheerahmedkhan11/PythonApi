from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware
from app import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from app import schemas, utils
from typing import List
from app.routers import posts, users, auth, votes





app = FastAPI()

@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
async def root():
    return {"message": "Hello World!"}




