# -*- coding: utf-8 -*-
# Imported to define datatypes.
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
# Imported to create database in app.  Here is where SQLite & PostgreSQL differ.
from sqlalchemy import create_engine





Base = declarative_base() # Necessary class instance for SQLite databases.
# Define Restaurant class that inherits Base class's attributes.
class Restaurant(Base):
  # Name table this Class is creating/representing.
  __tablename__ = 'restaurant'

  # Define columns and their respective datatypes.
  id = Column(Integer, primary_key = True)
  restaurant_name = Column(String)
  restaurant_address = Column(String)
  restaurant_image = Column(String)
  
  
  # Add a property decorator to serialize information from this database.
  # Properties are a simple way to return a computed value from an attribute, 
  # read, or call a function on an attribute write.
  @property # descriptor
  def serialize(self):
    return {
      'restaurant_name': self.restaurant_name,
      'restaurant_address': self.restaurant_address,
      'restaurant_image' : self.restaurant_image,
      'id' : self.id
      
      }

engine = create_engine('sqlite:///restaurants.db')
 
# Create database.
Base.metadata.create_all(engine)
