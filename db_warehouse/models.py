from sqlalchemy import Column,Integer,String,DateTime
from .db_engine import Base

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    readIntent = Column(String)
    startDate = Column(DateTime)
    endDate = Column(DateTime)
    pageMarker = Column(Integer)
    