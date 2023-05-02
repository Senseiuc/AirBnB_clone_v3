#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        _password = Column('password', String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    def to_dict(self, save_pass=False):
        """returns a dictionary representation of the instance"""
        dict = {}
        for key, value in self.__dict__.items():
            if key == "_sa_instance_state":
                continue
            if key == "created_at" or key == "updated_at":
                dict[key] = value.isoformat()
            elif key == "_password" and save_pass is False:
                continue
            else:
                dict[key] = value
        dict["__class__"] = self.__class__.__name__
        return dict

    @property
    def password_hash(self):
        """get password"""
        return self._password

    @password_hash.setter
    def set_password(self, passwd):
        """hash password"""
        self._password = hashlib.md5(passwd.encode()).hexdigest()

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
