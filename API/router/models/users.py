from generale.models import BaseModel
from sqlalchemy import Column, String, Boolean, DateTime, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from models.post import Post, PostComment, PostFavorites

class UserTable(BaseModel):
    __tablename__ = "users_user"

    username = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    role = Column(String)
    gender = Column(String)
    date_of_birth = Column(Date)
    date_joined = Column(DateTime, default=datetime.now)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="user")
    comments = relationship("PostComment", back_populates="user")
    favorites = relationship("PostFavorites", back_populates="user")
