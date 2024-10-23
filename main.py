from fastapi import FastAPI, HTTPException, Request
from db.conn import db
from models.vehicle import Vehicle
from datetime import datetime

app = FastAPI()


@app.get("/")
def test_up():
    return {
        "msg": "Hello from FastAPI this is a test it works"
    }


@app.post("/api/vehicle/add")
async def insert_vehicle(vehicle: Vehicle):
    driver = db.drivers.find_one({"id": "6718c8e5906ef85c4fa6858f"})
    if not driver:
        raise HTTPException(404, detail="Driver not found")

    vehicle.driver = driver["id"]
    db.vehicles.insert_one(vehicle.dict())
    return {
        "msg": "Vehicle allocated"
    }


@app.post("/api/vehicle/allocate")
async def allocate_vehicle(request: Request):
    request = await request.json()
    employee = db.employees.find_one({"id": request["employeeId"]})
    if not employee:
        raise HTTPException(404, detail="Employee not found")

    vehicle = db.vehicles.find_one({"id": request["vehicleId"]})
    if not vehicle:
        raise HTTPException(404, detail="Vehicle not found")
    date = datetime.now()
    db.allocations.insert_one({
        "employeeId": employee["id"],
        "vehicleId": vehicle["id"],
        "date": date
    })
    return {
        "msg": "Vehicle allocated"
    }
