# -------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------ #
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from src.dependencies.auth import get_current_user
from src.dependencies.basic import get_db
from src.schemas.basic import PostCreate, Post
from src.database import models
from src.utils.s3 import upload_file_to_s3
import uuid

router = APIRouter()

@router.post("/create_posts", response_model=Post)
async def create_post(
    title: str,
    content: str,
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 處理圖片上傳
    image_url = None
    if image:
        # 生成唯一的文件名
        file_extension = image.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_extension}"
        
        # 上傳到 S3 並獲取 URL
        try:
            image_url = await upload_file_to_s3(
                file=image,
                file_name=file_name,
                bucket_name="your-bucket-name"  # 請替換為您的 S3 bucket 名稱
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

    # 創建新貼文
    new_post = models.Post(
        title=title,
        content=content,
        image_url=image_url,
        author_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/read_posts", response_model=Post)
async def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/update_posts", response_model=Post)
async def update_post(
    post_id: int,
    title: str,
    content: str,
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_post = db.query(models.Post).filter(
        models.Post.id == post_id, 
        models.Post.author_id == current_user.id
    ).first()
    
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Post not found"
        )
    
    # 處理新圖片上傳
    if image:
        file_extension = image.filename.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_extension}"
        
        try:
            image_url = await upload_file_to_s3(
                file=image,
                file_name=file_name,
                bucket_name="your-bucket-name"
            )
            db_post.image_url = image_url
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Failed to upload image: {str(e)}"
            )
    
    db_post.title = title
    db_post.content = content
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/delete_posts", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.author_id == current_user.id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    db.delete(db_post)
    db.commit()
    return
# ------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------- #