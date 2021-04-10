from fastapi import FastAPI,status,Response
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from . import models
from . import schemas
from .db_engine import SessionLocal, engine
from datetime import datetime
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/all-book',status_code=status.HTTP_200_OK)
def all_book(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

@app.post('/create-book',status_code=status.HTTP_201_CREATED)
def create_book(request: schemas.Book, db: Session = Depends(get_db)):
    datetime_obj = datetime.strptime(request.startDate,'%d/%m/%y %H:%M:%S')
    new_book = models.Book(title=request.title,readIntent=request.readIntent,startDate=datetime_obj)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get('/book/{id}',status_code=status.HTTP_200_OK)
def get_a_book(id,response:Response,db: Session = Depends(get_db)):
    showbook = db.query(models.Book).filter(models.Book.id == id).first()
    if not showbook:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     'message' : f"Book with id {id} is not available"
        # }
    return showbook

