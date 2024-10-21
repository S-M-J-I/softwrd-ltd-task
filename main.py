from fastapi import FastAPI
from db.conn import db
from schema.employee import Employee

app = FastAPI()


@app.get("/")
def test_up():
    # emp = Employee(name="John")
    # db.employees.insert_one(emp.dict())
    return {
        "msg": "Hello from FastAPI this is a test it works"
    }
