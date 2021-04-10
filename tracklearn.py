import uvicorn
from fastapi import FastAPI
import datetime

backend = FastAPI()


@backend.get('/')
async def data():
    data = {
        "book_data": {
            1: {"name": "algorithm manual design", "start_date": datetime.date.today()},
            2: {"name": "attitude is everything", "start_date": datetime.date.today()}
        }
    }
    return data

@backend.get('/book/{id}')
def getbook(id: int):
    data = {
        "book_data": {
            1: {"name": "algorithm manual design", "start_date": datetime.date.today()},
            2: {"name": "attitude is everything", "start_date": datetime.date.today()}
        }
    }
    return data['book_data'][id]


@backend.get('/about')
def about():
    respons = {"data": {"about": "this is backend for track learning app"}}
    return respons['data']['about']

if __name__ == "__main__":
    uvicorn.run(backend, host="0.0.0.0", port=8000)