from unicodedata import name
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db
import models
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

models.Base.metadata.create_all(bind=engine)

class Posts(BaseModel):
    title: str
    name: str
    content: str

# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):
#     post = db.query(models.Post).all()
#     return post
# 

# Get
@app.get("/posts")
def posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# Get one Post
@app.get("/post/{id}")
def post(id:int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id :{id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return post

# Post
@app.post("/create")
def create(create:Posts, db: Session = Depends(get_db)):
    new_post = models.Post(**create.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# Delete
@app.delete("/delete/{id}")
def delete(id:int, db: Session = Depends(get_db), status_code=status.HTTP_204_NO_CONTENT):
    deleted = db.query(models.Post).filter(models.Post.id == id)
    if deleted.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} dose not exist")
    deleted.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update
@app.put("/update/{id}")
def update_post(id:int, updated_post: Posts, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"msg":post_query.first()}