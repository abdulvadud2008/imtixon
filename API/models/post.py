from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from generale.models import BaseModel

class PostFiles(BaseModel):
    __tablename__ = 'news_postfiles'
    file: Mapped[str] = mapped_column(String)
    post_id: Mapped[int] = mapped_column(ForeignKey('news_post.id'))

    post: Mapped["Post"] = relationship(back_populates="files")


class PostCategory(BaseModel):
    __tablename__ = 'news_postcategory'
    title: Mapped[str] = mapped_column(String(25))

    posts: Mapped["Post"] = relationship(back_populates="category")

class Post(BaseModel):
    __tablename__ = 'news_post'
    title: Mapped[str] = mapped_column(String(64))
    description: Mapped[str] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey('news_postcategory.id'), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users_user.id'), nullable=True)

    files: Mapped[list["PostFiles"]] = relationship(back_populates="post", lazy="joined")
    category: Mapped["PostCategory"] = relationship(back_populates="posts")
    user: Mapped["UserTable"] = relationship(back_populates="posts")
    comments: Mapped[list["PostComment"]] = relationship(back_populates="post")
    favorites: Mapped[list["PostFavorites"]] = relationship(back_populates="post")



class PostComment(BaseModel):
    __tablename__ = 'news_postcomment'
    user_id: Mapped[int] = mapped_column(ForeignKey('users_user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('news_post.id'))  
    text: Mapped[str] = mapped_column(String(48))

    user: Mapped["UserTable"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")


class PostFavorites(BaseModel):
    __tablename__ = 'news_postfavorites'
    user_id: Mapped[int] = mapped_column(ForeignKey('users_user.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('news_post.id'))

    user: Mapped["UserTable"] = relationship(back_populates="favorites")
    post: Mapped["Post"] = relationship(back_populates="favorites") 