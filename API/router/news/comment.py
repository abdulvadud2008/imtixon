from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.post import PostComment, Post
from models.users import UserTable
from database import get_session
from dependencies.users.user import user_handler
from schemas.news.comment import CommentCreateSchema

router = APIRouter(
    prefix="/comment",
    tags=['comment']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_comment(
    data: CommentCreateSchema, 
    user: UserTable = Depends(user_handler.user), 
    session: Session = Depends(get_session)
):
    post = session.query(Post).filter(Post.id == data.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")

    comment = PostComment(
        post_id=data.post_id,
        user_id=user.id,
        text=data.text
    )

    try:
        session.add(comment)
        session.commit()
        session.refresh(comment)
        return {"message": "Comment created!"}
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occurred during comment creation")


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int, 
    user: UserTable = Depends(user_handler.user), 
    session: Session = Depends(get_session)
):
    comment = session.query(PostComment).filter(PostComment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found!")
    
    if comment.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete comment, because it was created by another user.")

    session.delete(comment)
    session.commit()
