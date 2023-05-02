#!/usr/bin/python
""" holds class Amenity"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    """Representation of Amenity """
    if models.storage_t == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def to_dict(self):
        """returns a dictionary representation of the instance"""
        new_dict = super().to_dict()
        return new_dict

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)
