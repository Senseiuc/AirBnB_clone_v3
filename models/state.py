#!/usr/bin/python3
""" holds class State"""
import models
import sqlalchemy
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Representation of state """
    if models.storage_t == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
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
        """initializes state"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def cities(self):
            """getter for list of city instances related to the state"""
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
