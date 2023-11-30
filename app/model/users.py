from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    disabled = Column(Boolean, default=False)