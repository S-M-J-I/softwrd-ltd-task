# Vehicle Allocation Aystem

To run this project, clone the repository:
```sh
git clone https://github.com/S-M-J-I/softwrd-ltd-task
```
or use SSH
```sh
git clone git@github.com:S-M-J-I/softwrd-ltd-task.git
```

## Running the application

**NOTE: [Docker](https://docs.docker.com/engine/install/) must be installed for this step.**

#### Step 1: Enviroment vairables

Create a `.env` file and set the following environment variables:
```sh
MONGO_CONN_STR=
MONGO_DB=
```

*NOTE: The owner of this repository has deployed his database to a MongoDB Atlas Cluster. If you need access to it, feel free to reach out to him at [jishanlion@gmail.com](mailto:jishanlion@gmail.com)*

#### Step 2: Docker pull and run

Open up the terminal pointing to the root directory and enter the command:
```sh
docker pull smji14/softwrd-ltd-app:latest
```

Wait for the build to be finished. Next, run the app using the following command:
```sh
docker run -p 8000:8000 softwrd-ltd-app
```

## Hitting the API endpoints

#### 1. Allocate a vehicle
**Enpoint**: `/api/vehicle/allocate`\
**Method**: `POST`\
**Body (JSON)**:
```json
{
  "employee": "--",
  "vehicle": "--"
}
```
The `employee` key takes the unique id of the employee. The `vehicle` key takes the unique id of the vehicle.
\
**Returns**:
```json
{
    "message": "Vehicle allocated"
}
```

#### 2. Update a vehicle allocation
**Enpoint**: `/api/vehicle/update/{allocation_id}`\
**Method**: `PATCH`\
**Parameters**: `allocation_id` - the unique id of the allocation to be updated\
**Body (JSON)**:
```json
{
  "employee": "--",
  "vehicle": "--"
}
```
The `employee` key takes the unique id of the employee. The `vehicle` key takes the unique id of the vehicle.
\
**Returns**:
```json
{
    "message": "Allocation updated successfully"
}
```


#### 3. Delete a vehicle allocation
**Enpoint**: `/api/vehicle/delete/{allocation_id}`\
**Method**: `DELETE`\
**Parameters**: `allocation_id` - the unique id of the allocation to be updated\
**Returns**:
```json
{
    "message": "Allocation deleted"
}
```


#### 4. Get vehicle allocation history
**Enpoint**: `/api/vehicle/allocate/history`\
**Method**: `GET`\
**Returns**: A list of all allocations made.


#### 5. Add a vehicle
**Enpoint**: `/api/vehicle/add`\
**Method**: `POST`\
**Body (JSON)**:
```json
{
  "driver_id": "--",
  "vehicle": {
    "num_plate": "---",
    "name": "---",
    "type": "---"
  }
}
```

#### Credits
Done by S M Jishanul Islam