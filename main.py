from fastapi import FastAPI, HTTPException, Request
from pymongo import ASCENDING
from db.conn import db
from models.vehicle import Vehicle
from datetime import datetime


def create_ttl_index():
    db.allocations.create_index(
        [("booked_at", ASCENDING)],
        expireAfterSeconds=86400
    )


app = FastAPI(lifespan=create_ttl_index())


@app.get("/")
def test_up():
    return {
        "msg": "Hello from FastAPI this is a test it works"
    }


# @app.post("/api/vehicle/add")
# async def insert_vehicle(vehicle: Vehicle):
#     driver = db.drivers.find_one({"id": "6718c8e5906ef85c4fa6858f"})
#     if not driver:
#         raise HTTPException(404, detail="Driver not found")

#     vehicle.driver = driver["id"]
#     db.vehicles.insert_one(vehicle.dict())
#     return {
#         "msg": "Vehicle allocated"
#     }


@app.post("/api/vehicle/allocate")
async def allocate_vehicle(request: Request):
    """
        Cache later
    """
    request = await request.json()
    employee = db.employees.find_one({"id": request["employeeId"]}, {"id": 1})
    if not employee:
        raise HTTPException(404, detail="Employee not found")

    vehicle = db.vehicles.find_one({"id": request["vehicleId"]}, {"id": 1})
    if not vehicle:
        raise HTTPException(404, detail="Vehicle not found")
    date = datetime.now()
    db.allocations.insert_one({
        "employee": employee["id"],
        "vehicle": vehicle["id"],
        "booked_at": date
    })
    return {
        "msg": "Vehicle allocated"
    }


@app.patch("/api/vehicle/update")
async def update_allocation():
    pass


@app.delete("/api/vehicle/delete")
async def delete_allocation():
    pass
