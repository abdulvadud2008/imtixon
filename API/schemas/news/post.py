from pydantic import BaseModel, Field
from typing import List, Optional
from schemas.users import UserSchema
from API.schemas.news.comment import CommentResponseSchema
from API.schemas.news.favorite import FavoritesResponseSchema

class PostCreateSchema(BaseModel):
    title: str = Field(max_length=64)
    description: str
    category_id: int


class FileSchema(BaseModel):
    file: str


class CategorySchema(BaseModel):
    title: str


class PostListSchema(BaseModel):
    id: int
    title: str
    description: str
    category: CategorySchema
    main_image: Optional[str] = None

    @classmethod
    def from_orm(cls, post):
        main_image = post.files[0].file if post.files else None
        return cls(
            id=post.id,
            title=post.title,
            description=post.description,
            category=CategorySchema.from_orm(post.category),
            main_image=main_image
        )
    

class DetailSchema(BaseModel):
    id: int
    title: str
    description: str
    category: CategorySchema
    user: UserSchema
    files: Optional[List[FileSchema]] = None
    comments: Optional[List[CommentResponseSchema]] = None
    favorites: Optional[List[FavoritesResponseSchema]] = None