from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()


def lazy_relationship(*args, **kwargs):
    return relationship(*args, uselist=True, **kwargs)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    name = Column(String(16), unique=True, index=True)

    account = lazy_relationship("UserAccount", back_populates="user")



class UserAccount(Base):
    __tablename__ = "accounts"

    id = Column(String(36), primary_key=True, index=True, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    username = Column(String(16), unique=True, index=True)
    password = Column(String(256))

    user_id = Column(String(36), ForeignKey("users.id"))
    user = lazy_relationship("User", back_populates="account")
    
    posts_author = lazy_relationship('Post', back_populates='author')

# -------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------ #
from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Post(Base):
    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), index=True, nullable=False)
    content = Column(Text, nullable=False)
    img_url = Column(Text, nullable=False)
    author_id = Column(String(36), ForeignKey('accounts.id'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    author = relationship('UserAccount', back_populates='posts_author')
    

# class User(Base):
#     __tablename__ = 'users'
#     __table_args__ = {'extend_existing': True}

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(16), unique=True, index=True, nullable=False)
#     password = Column(String(256), nullable=False)

#     posts = lazy_relationship('Post', back_populates='author')
#     account = lazy_relationship("UserAccount", back_populates="user")
# ------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------- #