from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import User, UserAccount, Post

# 替换为您的数据库 URL
DATABASE_URL = "mysql+pymysql://admin:admin1234@3306/template_db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# 查询用户数据
users = session.query(User).all()
for user in users:
    print(user.name)

# 查询账户数据
accounts = session.query(UserAccount).all()
for account in accounts:
    print(account.username)

# 查询帖子数据
posts = session.query(Post).all()
for post in posts:
    print(post.title)

# DB_HOST=mysql
# DB_USER=admin
# DB_PASS=admin1234
# DB_PORT=3306
# DB_NAME=template_db