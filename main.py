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
    db.vehicles.create_index(
        [("allocated", ASCENDING)],
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
        raise HTTPException(status_code=404, detail="driver not found")

    vehicle.driver = driver["id"]
    db.vehicles.insert_one(vehicle.dict())
    return {
        "message": "Vehicle allocated"
    }


@app.get("/api/vehicle/allocate/history")
async def get_all_allocations():
    res = db.allocations.aggregate([
        {
            "$lookup": {
                "from": "vehicles",
                "let": {"vehicle_id": {"$toObjectId": "$vehicle"}},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$_id", "$$vehicle_id"]}}}
                ],
                "as": "vehicle_info"
            }
        },
        {
            "$lookup": {
                "from": "employees",
                "let": {"employee_id": {"$toObjectId": "$employee"}},
                "pipeline": [
                    {"$match": {"$expr": {"$eq": ["$_id", "$$employee_id"]}}}
                ],
                "as": "employee_info"
            }
        },
        {
            "$unwind": "$vehicle_info"
        },
        {
            "$unwind": "$employee_info"
        },
        {
            "$project": {
                "_id": 1,
                "booked_at": 1,
                "driver": 1,
                "vehicle": {
                    "name": "$vehicle_info.name",
                    "type": "$vehicle_info.type",
                    "num_plate": "$vehicle_info.num_plate",
                },
                "employee": {
                    "name": "$employee_info.name"
                }
            }
        }
    ])
    res = res.to_list()
    for result in res:
        result["_id"] = str(result["_id"])
    return res


@app.post("/api/vehicle/allocate")
async def allocate_vehicle(allocation: Allocation):
    """
        Cache later
    """
    allocation = allocation.model_dump()

    employee = db.employees.find_one(
        {"_id": ObjectId(allocation["employee"])})
    if not employee:
        raise HTTPException(status_code=404, detail="employee not found")

    vehicle = db.vehicles.find_one(
        {"_id": ObjectId(allocation["vehicle"])})
    if not vehicle:
        raise HTTPException(status_code=404, detail="vehicle not found")
    if vehicle["allocated"]:
        return HTTPException(status_code=409, detail="vehicle allocated")

    if allocation["booked_at"] is None:
        allocation["booked_at"] = datetime.now()

    res = db.allocations.insert_one(allocation)
    if res.inserted_id:
        vehicle["allocated"] = True
        db.vehicles.update_one(
            {"_id": ObjectId(vehicle['_id'])}, {"$set": vehicle})
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
