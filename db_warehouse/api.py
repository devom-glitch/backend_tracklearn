from typing import List
from fastapi import FastAPI,status,Response
from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from starlette.status import HTTP_404_NOT_FOUND
from . import models
from . import schemas
from .db_engine import SessionLocal, engine
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .hashing import Hash


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

# validation for text comming from request string
def validate(date_text):
    try: 
        return bool(datetime.strptime(date_text,'%d/%m/%y'))
    except ValueError:
        return False
    
# date time validation 
def validate_t(date_time_text):
    try:
        return bool(datetime.strptime(date_time_text,'%d/%m/%y %M:%H:%S'))
    except ValueError:
        return False
# db session maker & connector to db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/read/{book_id}',status_code=status.HTTP_201_CREATED,tags=['Reads'])
def create_read(id,request:schemas.Read,db: Session = Depends(get_db)):
    if(validate_t(request.readStartTime) and validate_t(request.readStopTime)):
        read_start_time_obj = datetime.strptime(request.readStartTime,'%d/%m/%y %H:%M:%S')
        read_stop_time_obj = datetime.strptime(request.readStopTime,'%d/%m/%y %H:%M:%S')
        duration = int((read_stop_time_obj - read_start_time_obj).total_seconds()/60) 
        new_read = models.Read(book_id = id,readStartTime = read_start_time_obj,readStopTime = read_stop_time_obj,duration = duration)
        db.add(new_read)
        db.commit()
        db.refresh(new_read)
        return new_read
    else:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail=f"wrong format of readStartTime or readStopTime : {request.readStartTime} or {request.readStopTime}")
        

#fetch all the books available
@app.get('/all-book',status_code=status.HTTP_200_OK,tags=['Blogs']) #response_model=List[schemas.ShowBook])
def all_book(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

#create book with title,read intent and start date
@app.post('/create-book',status_code=status.HTTP_201_CREATED,tags=['Blogs'])
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
    
@app.get('/book/{id}',status_code=status.HTTP_200_OK,response_model=schemas.ShowBook,tags=['Blogs'])
def get_a_book(id,response:Response,db: Session = Depends(get_db)):
    showbook = db.query(models.Book).filter(models.Book.id == id).first()
    if not showbook:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Book with id {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {
        #     'message' : f"Book with id {id} is not available"
        # }
    return showbook



@app.delete('/book/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['Blogs'])
def del_book(id,db: Session = Depends(get_db)):
    del_book = db.query(models.Book).filter(models.Book.id == id)
    if not del_book.first():
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail=f"Book with id {id} not found")
    del_book.delete(synchronize_session=False)
    db.commit()

@app.put('/book/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['Blogs'])
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
     
     
     
   
        
@app.post('/user',response_model=schemas.ShowUser,tags=['Users'])
def create_user(request: schemas.User,db:Session=Depends(get_db)):
    new_user = models.User(name=request.name,email=request.email,password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}',response_model=schemas.ShowUser,tags=['Users'])
def get_user(id:int,db:Session = Depends(get_db)):
    user= db.query(models.User).filter(models.User.id==id).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with the id {id} is not available")
    return user

    