from sqlalchemy import Column, Integer, LargeBinary, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String)
    users = relationship("Image", back_populates="images")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    data = Column(LargeBinary)
    user_id = Column(Integer, ForeignKey("Users.id"))
    images = relationship("User", back_populates="users")
