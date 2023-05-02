#!/usr/bin/python
""" holds class City"""
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of city """
    if models.storage_t == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities",
                               cascade="all, delete")
    else:
        state_id = ""
        name = ""

    def to_dict(self):
        """returns a dictionary representation of the instance"""
        dict = {}
        for key, value in self.__dict__.items():
            if key == "_sa_instance_state":
                continue
            if key == "created_at" or key == "updated_at":
                dict[key] = value.isoformat()
            else:
                dict[key] = value
        dict["__class__"] = self.__class__.__name__
        return dict

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
