from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_session
from schemas.post import FavoritesResponseSchema
from models.post import PostFavorites, Post
from dependencies.users.user import user_handler, UserTable

router = APIRouter(
    prefix="/favorites",
    tags=['favorites']
)

@router.post("/", response_model=FavoritesResponseSchema, status_code=201)
def add_favorite(favorite: FavoritesResponseSchema, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):
    # Check if the post exists
    db_post = session.query(Post).filter(Post.id == favorite.post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Check if the favorite already exists
    db_favorite = session.query(PostFavorites).filter(
        PostFavorites.user_id == user.id,
        PostFavorites.post_id == favorite.post_id
    ).first()

    if db_favorite:
        raise HTTPException(status_code=400, detail="Post already favorited")

    db_favorite = PostFavorites(
        user_id=user.id,
        post_id=favorite.post_id
    )
    
    session.add(db_favorite)
    session.commit()
    session.refresh(db_favorite)
    
    return FavoritesResponseSchema.from_orm(db_favorite)

@router.delete("/", status_code=204)
def remove_favorite(favorite: FavoritesResponseSchema, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):
    db_favorite = session.query(PostFavorites).filter(
        PostFavorites.user_id == user.id,
        PostFavorites.post_id == favorite.post_id
    ).first()

    if not db_favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    session.delete(db_favorite)
    session.commit()
    
    return None
