from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
import os
import aiofiles
from starlette import status
from config import MEDIA_ROOT
from database import get_session
# from descriptions.files import *
from sqlalchemy.orm import Session
from models.users import UserTable

from models.post import PostFiles, Post
from dependencies.users.user import user_handler
from dirocteries.posts import create_dir

router = APIRouter(
    prefix="/post-files",
    tags=['post-files']
)


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_file(
    file: UploadFile = File(...), post_id: int = Form(...),
    user: UserTable = Depends(user_handler.employee), 
    session: Session = Depends(get_session)
):
    
    if file is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file provided")

    post = session.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} not found")

    file_data = await create_dir(post_id=post_id, filename=file.filename)
    file_full_path = file_data['file_full_path']
    file_dir_for_django = file_data['file_dir'] + file.filename

    content = await file.read()
    async with aiofiles.open(file_full_path, 'wb') as out_file:
        await out_file.write(content)

    post_files = PostFiles(
        post_id=post_id,
        file=file_dir_for_django
    )
    
    session.add(post_files)
    session.commit()
    session.refresh(post_files)

    return {"message": "Post File Created!"}




@router.put("/update/{file_id}", status_code=status.HTTP_200_OK)
async def update_file(
    file_id: int,
    file: UploadFile = File(...),
    user: UserTable = Depends(user_handler.employee), 
    session: Session = Depends(get_session)
):
    
    post_files = session.query(PostFiles).filter(PostFiles.id == file_id).first()
    if not post_files:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    old_file_path = f"{MEDIA_ROOT}{post_files.file}"
    if os.path.exists(old_file_path):
        os.remove(old_file_path)

    file_data = await create_dir(post_id=post_files.post_id, filename=file.filename)
    content = await file.read()
    async with aiofiles.open(file_data['file_full_path'], 'wb') as out_file:
        file_dir_for_django = file_data['file_dir'] + file.filename
        await out_file.write(content)

    post_files.file = file_dir_for_django
    session.commit()
    session.refresh(post_files)

    return {"message": "Post File Updated!"}



@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id: int, user: UserTable = Depends(user_handler.employee), session: Session = Depends(get_session)):

    post_files = session.query(PostFiles).filter(PostFiles.id == file_id).first()
    if not post_files:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    file_path = f"{MEDIA_ROOT}{post_files.file}"
    if os.path.exists(file_path):
        os.remove(file_path)

    session.delete(post_files)
    session.commit()