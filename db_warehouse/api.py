from fastapi import FastAPI,status,Response
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from . import models
from . import schemas
from .db_engine import SessionLocal, engine
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:8000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(engine)

def validate(date_text):
    try: 
        return bool(datetime.strptime(date_text,'%d/%m/%y'))
    except ValueError:
        return False

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
    if(validate(request.startDate)):
        datetime_obj = datetime.strptime(request.startDate,'%d/%m/%y')
        new_book = models.Book(title=request.title,readIntent=request.readIntent,startDate=datetime_obj)
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"wrong format of startDate : {request.startDate}")
    
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



@app.delete('/book/{id}',status_code=status.HTTP_204_NO_CONTENT)
def del_book(id,db: Session = Depends(get_db)):
    db.query(models.Book).filter(models.Book.id == id).delete(synchronize_session=False)
    db.commit()

@app.put('/book/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.UpdateBook,db:Session = Depends(get_db)):
    update_book = db.query(models.Book).filter(models.Book.id == id)
    if not update_book.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Book with id {id} not found")
    if not validate(request.endDate):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"wrong format of startDate : {request.startDate}")
    else:
        datetime_obj = datetime.strptime(request.endDate,'%d/%m/%y')
        update_book.update({models.Book.pageMarker:request.pageMarker, models.Book.endDate:datetime_obj},synchronize_session=False)
        db.commit()
    return db.query(models.Book).filter(models.Book.id == id).first()
        