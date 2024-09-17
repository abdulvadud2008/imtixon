from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from models.post import Post
from sqlalchemy import select
from database import get_session
from models.users import UserTable
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from dependencies.users.user import user_handler
from schemas.news.post import (PostCreateSchema, PostListSchema, DetailSchema)

router = APIRouter(
    prefix="/news",
    tags=['news']
)


@router.get("/posts", response_model=list[PostListSchema], status_code=status.HTTP_200_OK)
def get_posts(session: Session = Depends(get_session)):
    result = session.execute(
        select(Post)
        .options(joinedload(Post.files), joinedload(Post.category))
    )
    posts = result.unique().scalars().all()

    return [PostListSchema.from_orm(post) for post in posts]


@router.get("/posts/{post_id}", response_model=DetailSchema, status_code=status.HTTP_200_OK)
async def get_post_detail(post_id: int, session: Session = Depends(get_session)):
    result = session.execute(
        select(Post).where(Post.id == post_id)
        .options(
            joinedload(Post.category),  
            joinedload(Post.user),
            joinedload(Post.files),
            joinedload(Post.comments),
            joinedload(Post.favorites)))
    post = result.unique().scalar_one_or_none()

    if not post: raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(data: PostCreateSchema, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):
    post = Post(
        title=data.title,
        description=data.description,
        category_id=data.category_id,
        user_id=user.id)
    try:
        session.add(post)
        session.commit()
        session.refresh(post)
        return {"message": "Post created!"}
    except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occurred")


@router.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
def update_post(post_id: int, data: PostCreateSchema, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):
    post = session.query(Post).filter(Post.id == post_id, Post.user_id == user.id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or access denied.")
    
    # Update post fields
    post.title = data.title
    post.description = data.description
    post.category_id = data.category_id

    try:
        session.commit()
        session.refresh(post)
        return {"message": "Post updated !"}
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occurred during the update.")



@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):
    # Fetch the post with the given ID
    post = session.query(Post).filter(Post.id == post_id).first()
    
    # If the post does not exist, raise a 404 error
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
    
    # Check if the user is authorized to delete the post
    if post.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this post.")
    
    # Delete the post
    session.delete(post)
    session.commit()

    return {"detail": "Post deleted successfully"}
