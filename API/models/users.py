from generale.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date, datetime
from models.post import Post, PostComment, PostFavorites


class UserTable(BaseModel):
    __tablename__ = "users_user"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    role: Mapped[str]
    gender: Mapped[str]
    date_of_birth: Mapped[date]
    date_joined: Mapped[date] = mapped_column(default=datetime.now)
    is_superuser: Mapped[bool] = mapped_column( default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)


    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    comments: Mapped[list["PostComment"]] = relationship(back_populates="user")
    favorites: Mapped[list["PostFavorites"]] = relationship(back_populates="user")