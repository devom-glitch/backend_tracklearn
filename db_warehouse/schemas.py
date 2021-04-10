from pydantic import BaseModel
class Book(BaseModel):
    title : str
    readIntent: str
    startDate: str
    
class UpdateBook(BaseModel):
    pageMarker: int
    endDate: str