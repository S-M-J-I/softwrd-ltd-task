from fastapi import FastAPI, HTTPException, Request, Body
from pymongo import ASCENDING
from db.conn import db
from datetime import datetime
from models import Allocation, Vehicle, Driver, Employee
from bson import ObjectId


def create_ttl_index():
    db.allocations.create_index(
        [("booked_at", ASCENDING)],
        expireAfterSeconds=86400
    )


app = FastAPI(lifespan=create_ttl_index())


@app.get("/")
def test_up():
    return {
        "message": "Hello from FastAPI this is a test it works"
    }


@app.post("/api/vehicle/add")
async def insert_vehicle(vehicle: Vehicle, driver_id: str = Body(...)):
    driver = db.drivers.find_one({"_id": ObjectId(driver_id)})
    if not driver:
        raise HTTPException(404, detail="Driver not found")

    vehicle.driver = driver["id"]
    db.vehicles.insert_one(vehicle.dict())
    return {
        "message": "Vehicle allocated"
    }


@app.post("/api/vehicle/allocate")
async def allocate_vehicle(allocation: Allocation):
    """
        Cache later
    """
    allocation = allocation.model_dump()

    employee = db.employees.find_one(
        {"_id": ObjectId(allocation["employee"])}, {"_id": 1})
    if not employee:
        raise HTTPException(404, detail="Employee not found")

    vehicle = db.vehicles.find_one(
        {"_id": ObjectId(allocation["vehicle"])}, {"_id": 1})
    if not vehicle:
        raise HTTPException(404, detail="Vehicle not found")

    if allocation["booked_at"] is None:
        allocation["booked_at"] = datetime.now()

    res = db.allocations.insert_one(allocation)
    if res.inserted_id:
        return {
            "message": "Vehicle allocated"
        }
    else:
        raise HTTPException(
            status_code=500, detail="failed to allocate vehicle")


@app.patch("/api/vehicle/update/{allocation_id}")
async def update_allocation(allocation_id, updated_allocation: Allocation):
    updated_allocation = updated_allocation.model_dump()
    if updated_allocation["booked_at"] is None:
        updated_allocation["booked_at"] = datetime.now()

    res = db.allocations.update_one(
        {"_id": ObjectId(allocation_id)}, {"$set": updated_allocation})

    if not res.matched_count:
        raise HTTPException(status_code=500, detail="update failed")

    return {"message": "Allocation updated successfully"}


@app.delete("/api/vehicle/delete/{allocation_id}")
async def delete_allocation(allocation_id):
    res = db.allocations.delete_one({"_id": ObjectId(allocation_id)})
    if not res.deleted_count:
        raise HTTPException(status_code=500, detail="could not delete entity")
    return {
        "message": "Allocation deleted"
    }
