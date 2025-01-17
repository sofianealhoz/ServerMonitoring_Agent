"""This module defines an exemple of test"""
import threading
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
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


def test_health():
    response = client.get("/health")
    assert response.status_code == 200


def test_get_cpu_usage():
    # backup of the existing monitortask to restore it after the test
    save_app = app.state.monitortask
    # use fake monitor to have deterministic values
    app.state.monitortask = MonitorTaskFake()
    response = client.get("/metrics/v1/cpu/usage")
    assert response.status_code == 200
    assert response.json() == [{"id": 0, "usage": "10", "frequency": 1830.00}, {"id": 1, "usage": "12", "frequency": 1830.00}]
    # restore monitortask for next test
    app.state.monitortask = save_app


def test_get_hdd():
    # backup of the existing monitortask to restore it after the test
    save_app = app.state.monitortask
    # use fake monitor to have deterministic values
    app.state.monitortask = MonitorTaskFake()
    
    response = client.get("/usageHdd")
    
    # Check status code
    assert response.status_code == 200
    
    # Check response format
    assert isinstance(response.json(), dict), f"Expected a dictionary in response: {response.json()}"
    
    # Check keys in the response
    expected_keys = ["total", "used", "free", "percent"]
    assert all(key in response.json() for key in expected_keys), f"Expected keys {expected_keys} in the response: {response.json()}"
    
    # Access the Hdd instance directly
    hdd_instance = app.state.monitortask.harddrive_usage
    
    # Check the type of the created instance
    assert isinstance(hdd_instance, Hdd), f"Expected an instance of Hdd, but got {type(hdd_instance)}"
    
    # restore monitortask for the next test
    app.state.monitortask = save_app


def test_get_cpu_core():
    response = client.get("/metrics/v1/cpu/core")
    # we can test types but not values because they will change at each test.
    assert response.status_code == 200
    assert isinstance(response.json()["number"], int)


def test_get_ram_usage():
    # backup of the existing monitortask to restore it after the test
    save_app = app.state.monitortask
    # use fake monitor to have deterministic values
    app.state.monitortask = MonitorTaskFake()
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
    
    # restore monitortask for the next test
    app.state.monitortask = save_app


def test_get_network_usage():
    # backup of the existing monitortask to restore it after the test
    save_app = app.state.monitortask
    # use fake monitor to have deterministic values
    app.state.monitortask = MonitorTaskFake()
    
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
    
    # restore monitortask for the next test
    app.state.monitortask = save_app


def test_get_process_usage():
    # backup of the existing monitortask to restore it after the test
    save_app = app.state.monitortask
    # use fake monitor to have deterministic values
    app.state.monitortask = MonitorTaskFake()
    
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
    
    # restore monitortask for the next test
    app.state.monitortask = save_app


def test_log_functions():
    log_file_path = "src/monitor/Documents"
    
    # Test count_unique_users
    unique_users = count_unique_users(log_file_path)
    assert unique_users == 2, f"Expected 2 unique user, but got {unique_users}"

    # Test error404
    count_404 = error404(log_file_path)
    assert count_404 == 2, f"Expected 2 occurrences of 404 errors, but got {count_404}"

    # backup of the existing monitortask to restore it after the test
    save_app = app.state.monitortask
    # use fake monitor to have deterministic values
    app.state.monitortask = MonitorTaskFake()
    
    response = client.get("/logMessage")
    # Check status code
    assert response.status_code == 200

    # restore monitortask for the next test
    app.state.monitortask = save_app

    



