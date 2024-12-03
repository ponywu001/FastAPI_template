from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class TextOnly(BaseModel):
    text: str = Field(..., title="Text", description="Text content")


class Token(BaseModel):
    access_token: str = Field(default='example_token')
    token_type: str = Field(default='bearer')


class UploadedFile(BaseModel):
    path: str = Field(..., title="Local Path")
    original_file_name: str = Field(..., title="Original File Name")
    extension: str = Field(..., title="File Extension")
    content_type: str = Field(..., title="Content Type")


# -------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------ #
from pydantic import BaseModel, Field
from typing import Optional

class PostCreate(BaseModel):
    title: str = Field(..., title="Title", description="The title of the post")
    content: str = Field(..., title="Content", description="Content of the post")
    image_url: Optional[str] = Field(None, title="Image URL", description="URL of the attached image")
    author_id: str = Field(..., title="ID of the Author")

class Post(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    image_url: Optional[str]
    created_at: str
    updated_at: Optional[str]

    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    username: str = Field(..., title="Username", description="The username for the new account")
    password: str = Field(..., title="Password", description="Password for the new account")
# ------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------- #