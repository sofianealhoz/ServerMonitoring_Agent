"""This module defines an exemple of test"""
import threading
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Test-only values: the real ones come from the environment, never from the code
os.environ.setdefault("AGENT_DATABASE_URL", "postgresql://test:test@localhost:5432/test")
os.environ.setdefault("AGENT_JWT_SECRET", "test-secret-not-used-in-production")

import pytest
from fastapi.testclient import TestClient
from core.security import create_access_token
from dependencies import get_current_user, get_db_connection, get_monitor
from domain.schemas.auth import CurrentUserSchema
from server import app
from monitor import MonitorTask
from src.monitor.LogFunction import count_unique_users, error404
from src.domain.models.hdd import Hdd


class MonitorTaskFake(MonitorTask):
    """
    Monitor class to mock the real monitor
    Instead of using the real monitor that fetch data on the host
    we use a monitor that provide "fake" values to control the output
    and make deterministic test (deterministic = repeatable and known values)
    """
    interval: int = 0
    harddrive_usage: Hdd = Hdd(
        total=62.688777923583984,
        used=8.715827941894531,
        free=50.75762939453125,
        percent=14.7
    )
    cpu_frequency = "1830.00"
    cpu_percent: list[float] = ["10", "12"]
    num_cores: int = 3

    def monitor(self):
        pass


# Launching the real monitor for test involving the real monitor
client = TestClient(app)
thread = threading.Thread(target=app.state.monitortask.monitor, daemon=True)
thread.start()


@pytest.fixture(autouse=True)
def authenticated_admin(request):
    """
    By default every test runs as an authenticated admin, without database or real token.

    Tests about authentication itself opt out with @pytest.mark.real_auth.
    """
    if "real_auth" in request.keywords:
        yield
        return
    app.dependency_overrides[get_current_user] = lambda: CurrentUserSchema(username="admin", role="admin")
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture
def fake_monitor():
    """
    Inject a fake monitor instead of the real one, through FastAPI's dependency overrides.

    Every route asking for Depends(get_monitor) receives this instance during the test.
    """
    monitor = MonitorTaskFake()
    app.dependency_overrides[get_monitor] = lambda: monitor
    yield monitor
    app.dependency_overrides.pop(get_monitor, None)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_get_cpu_usage(fake_monitor):
    response = client.get("/metrics/v1/cpu/usage")
    assert response.status_code == 200
    assert response.json() == [{"id": 0, "usage": "10", "frequency": 1830.00}, {"id": 1, "usage": "12", "frequency": 1830.00}]


def test_get_hdd(fake_monitor):
    
    response = client.get("/usageHdd")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response format
    assert isinstance(response.json(), dict), f"Expected a dictionary in response: {response.json()}"
    
    # Check keys in the response
    expected_keys = ["total", "used", "free", "percent"]
    assert all(key in response.json() for key in expected_keys), f"Expected keys {expected_keys} in the response: {response.json()}"
    
    # Access the Hdd instance directly
    hdd_instance = fake_monitor.harddrive_usage
    
    # Check the type of the created instance
    assert isinstance(hdd_instance, Hdd), f"Expected an instance of Hdd, but got {type(hdd_instance)}"
    


def test_get_cpu_core():
    response = client.get("/metrics/v1/cpu/core")
    # we can test types but not values because they will change at each test.
    assert response.status_code == 200
    assert isinstance(response.json()["number"], int)


def test_get_ram_usage(fake_monitor):
    response = client.get("/usageRam")

    # Check status code
    assert response.status_code == 200

    # Check response format
    assert isinstance(response.json(), list), f"Expected a list in response: {response.json()}"

    # Check each object in the list
    for ram_info in response.json():
        assert isinstance(ram_info, dict), f"Expected each item in the list to be a dictionary: {response.json()}"
        assert all(key in ram_info for key in ["total", "available", "used", "percent"]), f"Expected keys 'total', 'available', 'used', 'percent' in each item: {ram_info}"
        
        # Check the type of values in each object
        for key, value in ram_info.items():
            assert isinstance(value, (int, float)), f"Expected '{key}' to be an int or float: {ram_info}"
    


def test_get_network_usage(fake_monitor):
    
    response = client.get("/usageNetwork")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response format
    assert isinstance(response.json(), list), f"Expected a list in response: {response.json()}"
    
    # Check each object in the list
    for network_info in response.json():
        assert isinstance(network_info, dict), f"Expected each item in the list to be a dictionary: {response.json()}"
        assert all(key in network_info for key in ["name", "bytes_sent", "bytes_recv", "packets_sent", "packets_recv", "errin", "errout", "dropin", "dropout"]), f"Expected keys 'name', 'bytes_sent', 'bytes_recv', 'packets_sent', 'packets_recv', 'errin', 'errout', 'dropin', 'dropout' in each item: {network_info}"
        
        # Check the type of values in each object
        for key, value in network_info.items():
            assert isinstance(value, (str, int, float)), f"Expected '{key}' to be a string, int, or float: {network_info}"
    


def test_get_process_usage(fake_monitor):
    
    response = client.get("/usageProcess")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response format
    assert isinstance(response.json(), list), f"Expected a list in response: {response.json()}"
    
    # Check each object in the list
    for process_info in response.json():
        assert isinstance(process_info, dict), f"Expected each item in the list to be a dictionary: {response.json()}"
        assert all(key in process_info for key in ["pid", "name", "rss", "cpu_percent"]), f"Expected keys 'pid', 'name', 'rss', 'cpu_percent' in each item: {process_info}"
        
        # Check the type of values in each object
        assert isinstance(process_info["pid"], int), f"Expected 'pid' to be an int: {process_info}"
        assert isinstance(process_info["name"], str), f"Expected 'name' to be a string: {process_info}"
        assert isinstance(process_info["rss"], float), f"Expected 'rss' to be a float: {process_info}"
        assert isinstance(process_info["cpu_percent"], float), f"Expected 'cpu_percent' to be a float: {process_info}"
    


def test_log_functions(fake_monitor):
    log_file_path = "src/monitor/Documents"
    
    # Test count_unique_users
    unique_users = count_unique_users(log_file_path)
    assert unique_users == 2, f"Expected 2 unique user, but got {unique_users}"

    # Test error404
    count_404 = error404(log_file_path)
    assert count_404 == 2, f"Expected 2 occurrences of 404 errors, but got {count_404}"

    
    response = client.get("/logMessage")
    # Check status code
    assert response.status_code == 200


    





@pytest.fixture
def no_database():
    """Replace the database connection so validation can be tested without PostgreSQL."""
    app.dependency_overrides[get_db_connection] = lambda: None
    yield
    app.dependency_overrides.pop(get_db_connection, None)


def test_create_history_rejects_out_of_range_value(no_database):
    # cpu_usage above 100: Pydantic rejects the body, the route never runs
    response = client.post("/history", json={"cpu_usage": 150, "ram_usage": 40, "disk_usage": 20})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "cpu_usage"]


def test_create_history_rejects_missing_and_unknown_fields(no_database):
    response = client.post("/history", json={"cpu_usage": 10, "unknown": 1})
    assert response.status_code == 422


def test_history_limit_out_of_range(no_database):
    response = client.get("/history?limit=0")
    assert response.status_code == 422


def test_history_sample_id_must_be_positive(no_database):
    response = client.get("/history/0")
    assert response.status_code == 422


# ---------- Authentication and authorization ----------

@pytest.mark.real_auth
def test_no_token_gives_401(no_database):
    response = client.get("/usage")
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


@pytest.mark.real_auth
def test_forged_token_gives_401(no_database):
    response = client.get("/usage", headers={"Authorization": "Bearer not-a-real-token"})
    assert response.status_code == 401


@pytest.mark.real_auth
def test_token_signed_with_another_secret_gives_401(no_database):
    import jwt
    forged = jwt.encode({"sub": "admin"}, "another-secret", algorithm="HS256")
    response = client.get("/usage", headers={"Authorization": f"Bearer {forged}"})
    assert response.status_code == 401


@pytest.mark.real_auth
def test_reader_cannot_write_403(no_database):
    # Authenticated (we know who it is) but not allowed: 403, not 401
    app.dependency_overrides[get_current_user] = lambda: CurrentUserSchema(username="bob", role="reader")
    try:
        response = client.post("/history", json={"cpu_usage": 10, "ram_usage": 20, "disk_usage": 30})
        assert response.status_code == 403
    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_public_routes_need_no_token():
    assert client.get("/health").status_code == 200
    assert client.get("/version").status_code == 200


def test_access_token_is_readable_by_the_server():
    from core.security import decode_access_token
    assert decode_access_token(create_access_token("alice")) == "alice"
