from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_session
from schemas.post import PostCreateSchema, PostListSchema, DetailSchema
from models.post import Post
from dependencies.users.user import user_handler, UserTable

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

@router.post("/post", status_code=201)
def create_post(post: PostCreateSchema, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):
    db_post = Post(
        title=post.title,
        description=post.description,
        category_id=post.category_id,
        user_id=user.id  # Use the authenticated user's ID
    )
    
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    
    return {"message": "Post created !"}

@router.get("/get", response_model=List[PostListSchema])
def list_posts(session: Session = Depends(get_session)):
    posts = session.query(Post).all()
    return [PostListSchema.from_orm(post) for post in posts]

@router.get("/{post_id}", response_model=DetailSchema)
def read_post(post_id: int, session: Session = Depends(get_session)):
    db_post = session.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return DetailSchema.from_orm(db_post)



@router.put("/{post_id}", response_model=DetailSchema)
def update_post(post_id: int, post: PostCreateSchema, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):
    db_post = session.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if the current user is the owner of the post or an admin
    if db_post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")

    db_post.title = post.title
    db_post.description = post.description
    db_post.category_id = post.category_id
    # Assuming you might want to preserve the user_id, no need to update it.

    session.commit()
    session.refresh(db_post)
    
    return DetailSchema.from_orm(db_post)

@router.delete("/{post_id}", status_code=204)
def delete_post(post_id: int, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):
    db_post = session.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if the current user is the owner of the post or an admin
    if db_post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")

    session.delete(db_post)
    session.commit()
    
    return None
