from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date, datetime


class UserTable(Base):
    __tablename__ = 'users_user'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    first_name: Mapped[str]
    last_name: Mapped[str]
    username: Mapped[str]
    phone: Mapped[str] = mapped_column(unique=True)
    role: Mapped[str]
    gender: Mapped[str]
    date_of_birth: Mapped[date]
    password: Mapped[str]
    is_active: Mapped[bool]
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_staff: Mapped[bool] = mapped_column(default=False)
    email: Mapped[str]
    date_joined: Mapped[date] = mapped_column(default=datetime.now)