from sqlalchemy import Column, String, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from generale.models import BaseModel

class PostFiles(BaseModel):
    __tablename__ = 'news_postfiles'
    file = Column(String)
    post_id = Column(Integer, ForeignKey('news_post.id'))

    post = relationship("Post", back_populates="files")


class PostCategory(BaseModel):
    __tablename__ = 'news_postcategory'
    title = Column(String(25))

    posts = relationship("Post", back_populates="category")


class Post(BaseModel):
    __tablename__ = 'news_post'
    title = Column(String(64))
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('news_postcategory.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users_user.id'), nullable=True)

    files = relationship("PostFiles", back_populates="post", lazy="joined", cascade="all, delete-orphan")
    category = relationship("PostCategory", back_populates="posts")
    user = relationship("UserTable", back_populates="posts")
    comments = relationship("PostComment", back_populates="post", cascade="all, delete-orphan")
    favorites = relationship("PostFavorites", back_populates="post", cascade="all, delete-orphan")


class PostComment(BaseModel):
    __tablename__ = 'news_postcomment'
    user_id = Column(Integer, ForeignKey('users_user.id'))
    post_id = Column(Integer, ForeignKey('news_post.id'))  
    text = Column(String(48))

    user = relationship("UserTable", back_populates="comments")
    post = relationship("Post", back_populates="comments")


class PostFavorites(BaseModel):
    __tablename__ = 'news_postfavorites'
    user_id = Column(Integer, ForeignKey('users_user.id'))
    post_id = Column(Integer, ForeignKey('news_post.id'))

    user = relationship("UserTable", back_populates="favorites")
    post = relationship("Post", back_populates="favorites")
