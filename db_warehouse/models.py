from sqlalchemy import Column,Integer,String,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Time
from .db_engine import Base

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    readIntent = Column(String)
    startDate = Column(DateTime)
    endDate = Column(DateTime)
    pageMarker = Column(Integer)
    
    children = relationship("Read")


class Read(Base):
    __tablename__ = 'reads'
    id = Column(Integer,primary_key=True,index=True)
    book_id = Column(Integer,ForeignKey('books.id'))
    readStartTime = Column(DateTime)
    readStopTime = Column(DateTime)
    duration = Column(Integer)