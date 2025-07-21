from sqlalchemy import Integer, String ,Column

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,index=True,nullable=False)

    hash_password = Column(String,nullable=False)

