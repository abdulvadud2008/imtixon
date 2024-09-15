from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_session
from schemas.comment import CommentCreateSchema
from models.post import PostComment, Post
from dependencies.users.user import user_handler, UserTable

router = APIRouter(
    prefix="/comments",
    tags=['comments']
)

@router.post("/", response_model=CommentCreateSchema, status_code=201)
def create_comment(comment: CommentCreateSchema, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):
    # Check if the post exists
    db_post = session.query(Post).filter(Post.id == comment.post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    db_comment = PostComment(
        user_id=user.id,
        post_id=comment.post_id,
        text=comment.text
    )
    
    session.add(db_comment)
    session.commit()
    session.refresh(db_comment)
    
    return CommentCreateSchema.from_orm(db_comment)

@router.delete("/{comment_id}", status_code=204)
def delete_comment(comment_id: int, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):
    db_comment = session.query(PostComment).filter(PostComment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Check if the current user is the author of the comment or an admin
    if db_comment.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

    session.delete(db_comment)
    session.commit()
    
    return None
