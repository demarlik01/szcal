from database import Base
from sqlalchemy import Column, Integer, String, DateTime


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    zipcode = Column(String(6), nullable=False)
    address = Column(String(255), nullable=False)
    add_fee = Column(Integer, nullable=False)
