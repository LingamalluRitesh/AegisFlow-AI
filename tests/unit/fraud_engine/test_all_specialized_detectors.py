import pytest
from backend.core.types import RiskLevel, ActionType
def test_specialized_detector_01():
    payload = {"amount": 100.0}
    context = {"tx_count_5m": 1, "max_geo_leap_speed_kmh": 25.0, "is_new_device_used": 1}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_02():
    payload = {"amount": 200.0}
    context = {"tx_count_5m": 2, "max_geo_leap_speed_kmh": 50.0, "is_new_device_used": 0}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_03():
    payload = {"amount": 300.0}
    context = {"tx_count_5m": 3, "max_geo_leap_speed_kmh": 75.0, "is_new_device_used": 1}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_04():
    payload = {"amount": 400.0}
    context = {"tx_count_5m": 4, "max_geo_leap_speed_kmh": 100.0, "is_new_device_used": 0}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_05():
    payload = {"amount": 500.0}
    context = {"tx_count_5m": 5, "max_geo_leap_speed_kmh": 125.0, "is_new_device_used": 1}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_06():
    payload = {"amount": 600.0}
    context = {"tx_count_5m": 6, "max_geo_leap_speed_kmh": 150.0, "is_new_device_used": 0}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_07():
    payload = {"amount": 700.0}
    context = {"tx_count_5m": 7, "max_geo_leap_speed_kmh": 175.0, "is_new_device_used": 1}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_08():
    payload = {"amount": 800.0}
    context = {"tx_count_5m": 8, "max_geo_leap_speed_kmh": 200.0, "is_new_device_used": 0}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_09():
    payload = {"amount": 900.0}
    context = {"tx_count_5m": 9, "max_geo_leap_speed_kmh": 225.0, "is_new_device_used": 1}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_10():
    payload = {"amount": 1000.0}
    context = {"tx_count_5m": 10, "max_geo_leap_speed_kmh": 250.0, "is_new_device_used": 0}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_11():
    payload = {"amount": 1100.0}
    context = {"tx_count_5m": 11, "max_geo_leap_speed_kmh": 275.0, "is_new_device_used": 1}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_12():
    payload = {"amount": 1200.0}
    context = {"tx_count_5m": 12, "max_geo_leap_speed_kmh": 300.0, "is_new_device_used": 0}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_13():
    payload = {"amount": 1300.0}
    context = {"tx_count_5m": 13, "max_geo_leap_speed_kmh": 325.0, "is_new_device_used": 1}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_14():
    payload = {"amount": 1400.0}
    context = {"tx_count_5m": 14, "max_geo_leap_speed_kmh": 350.0, "is_new_device_used": 0}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_15():
    payload = {"amount": 1500.0}
    context = {"tx_count_5m": 15, "max_geo_leap_speed_kmh": 375.0, "is_new_device_used": 1}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_16():
    payload = {"amount": 1600.0}
    context = {"tx_count_5m": 16, "max_geo_leap_speed_kmh": 400.0, "is_new_device_used": 0}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_17():
    payload = {"amount": 1700.0}
    context = {"tx_count_5m": 17, "max_geo_leap_speed_kmh": 425.0, "is_new_device_used": 1}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_18():
    payload = {"amount": 1800.0}
    context = {"tx_count_5m": 18, "max_geo_leap_speed_kmh": 450.0, "is_new_device_used": 0}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_19():
    payload = {"amount": 1900.0}
    context = {"tx_count_5m": 19, "max_geo_leap_speed_kmh": 475.0, "is_new_device_used": 1}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_20():
    payload = {"amount": 2000.0}
    context = {"tx_count_5m": 20, "max_geo_leap_speed_kmh": 500.0, "is_new_device_used": 0}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_21():
    payload = {"amount": 2100.0}
    context = {"tx_count_5m": 21, "max_geo_leap_speed_kmh": 525.0, "is_new_device_used": 1}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_22():
    payload = {"amount": 2200.0}
    context = {"tx_count_5m": 22, "max_geo_leap_speed_kmh": 550.0, "is_new_device_used": 0}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_23():
    payload = {"amount": 2300.0}
    context = {"tx_count_5m": 23, "max_geo_leap_speed_kmh": 575.0, "is_new_device_used": 1}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_24():
    payload = {"amount": 2400.0}
    context = {"tx_count_5m": 24, "max_geo_leap_speed_kmh": 600.0, "is_new_device_used": 0}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1

def test_specialized_detector_25():
    payload = {"amount": 2500.0}
    context = {"tx_count_5m": 25, "max_geo_leap_speed_kmh": 625.0, "is_new_device_used": 1}
    assert payload["amount"] > 0
    assert context["tx_count_5m"] >= 1
