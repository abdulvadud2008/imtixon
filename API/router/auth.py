from fastapi import APIRouter, Depends, HTTPException
from database import get_session
from dependencies.JWT.handlers import JWTHandler
from dependencies.users.user import user_handler
from sqlalchemy.orm import Session
from models.users import UserTable
from sqlalchemy import select
from schemas.users import UserCreateSchema, UserSchema, UserLoginSchema
from utils import hash_password, bcrypt_context
from starlette import status    
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

@router.post("/signup", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def signup(data: UserCreateSchema, session: Session = Depends(get_session)):
    try:
        user = UserTable(
            username=data.username,
            password=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            role=data.role,
            email=data.email,
            gender=data.gender,
            date_of_birth=data.date_of_birth
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "User with username, email, or phone already registered!"}
        )


@router.post("/signin", status_code=status.HTTP_201_CREATED)
def signin(form_data: UserLoginSchema = Depends(), session: Session = Depends(get_session)):
    user = session.query(UserTable).filter(UserTable.username == form_data.username).first()
    if not user or not bcrypt_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password.")

    jwt_handler = JWTHandler()
    access_token = jwt_handler.create_token(username=user.username, user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserSchema, status_code=status.HTTP_200_OK)
def get_user_me(user: UserTable = Depends(user_handler.user)):
    return user