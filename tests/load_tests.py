from locust import HttpUser, TaskSet, task, between


class VehicleAllocation(TaskSet):
    @task
    def allocate_vehicle(self):
        self.client.post("/api/vehicle/allocate/", json={
            "employeeId": "6716a333b8ba7ed1ed766d2e",
            "vehicleId": "6718cd58ea9bc3c2075be5ca"
        })


class BulkUser(HttpUser):
    tasks = [VehicleAllocation]
    wait_time = between(1, 3)  # decrease time later
