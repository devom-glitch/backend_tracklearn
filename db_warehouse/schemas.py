from pydantic import BaseModel
from sqlalchemy import orm

# request schemas for creating book


class Book(BaseModel):
    title: str
    readIntent: str
    startDate: str

# request schemas for updating book


class UpdateBook(BaseModel):
    pageMarker: int
    endDate: str

# response schema for getting all book & getting one book


class ShowBook(BaseModel):
    title: str
    readIntent: str

    class Config():
        orm_mode = True


class Read(BaseModel):
    readStartTime: str
    readStopTime: str


class User(BaseModel):
    name: str
    email: str
    password: str
    
class ShowUser(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True
        
