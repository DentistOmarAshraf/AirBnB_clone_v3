#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from models.place import Place
from models.review import Review
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

        @property
        def places(self):
            to_ret = []
            all_places = models.storage.all(Place).values()
            for place in all_places:
                if self.id == place.user_id:
                    to_ret.append(place)
            return to_ret

        @property
        def reviews(self):
            to_ret = []
            all_reviews = models.storage.all(Review).values()
            for review in all_reviews:
                if review.user_id == self.id:
                    to_ret.append(review)
            return to_ret

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
