from fastapi.testclient import TestClient
from main import app

test_client = TestClient(app)


def test_allocations():
    test_payload = {
        "vehicle": "671a48a4283c151e01527870",
        "employee": "671a56a96eb936bd884bc442"
    }

    response = test_client.post("/api/vehicle/allocate", json=test_payload)

    print("Starting TC 1: Allocate free vehicle")
    assert response.status_code == 200
    response = response.json()

    assert response["message"] == "Vehicle allocated"
    print("Passed TC 1")


def test_allocations_on_prebooked_vehicle():
    test_payload = {
        "vehicle": "671a48a4283c151e01527870",
        "employee": "6716a333b8ba7ed1ed766d2e"
    }

    response = test_client.post("/api/vehicle/allocate", json=test_payload)

    print("Starting TC 2: Allocate booked vehicle")
    response = response.json()

    assert response["detail"] == "vehicle already allocated"
    assert response["status_code"] == 409
    print("Passed TC 2")