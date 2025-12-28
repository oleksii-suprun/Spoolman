"""Integration tests to verify ID serialization as strings (fixes CockroachDB precision issue)."""

import httpx

from .conftest import URL


def test_vendor_id_is_string():
    """Test that vendor IDs are serialized as strings to prevent JavaScript precision loss."""
    # Create a vendor
    result = httpx.post(
        f"{URL}/api/v1/vendor",
        json={"name": "Test Vendor"},
    )
    result.raise_for_status()
    vendor = result.json()

    # Verify ID is a string
    assert isinstance(vendor["id"], str), f"Vendor ID should be string, got {type(vendor['id'])}"

    # Clean up
    httpx.delete(f"{URL}/api/v1/vendor/{vendor['id']}").raise_for_status()


def test_filament_id_is_string():
    """Test that filament IDs are serialized as strings to prevent JavaScript precision loss."""
    # Create a vendor first
    vendor_result = httpx.post(
        f"{URL}/api/v1/vendor",
        json={"name": "Test Vendor"},
    )
    vendor_result.raise_for_status()
    vendor = vendor_result.json()

    # Create a filament
    result = httpx.post(
        f"{URL}/api/v1/filament",
        json={
            "vendor_id": vendor["id"],
            "density": 1.25,
            "diameter": 1.75,
        },
    )
    result.raise_for_status()
    filament = result.json()

    # Verify ID is a string
    assert isinstance(filament["id"], str), f"Filament ID should be string, got {type(filament['id'])}"

    # Verify nested vendor ID is also a string
    assert isinstance(
        filament["vendor"]["id"],
        str,
    ), f"Nested vendor ID should be string, got {type(filament['vendor']['id'])}"

    # Clean up
    httpx.delete(f"{URL}/api/v1/filament/{filament['id']}").raise_for_status()
    httpx.delete(f"{URL}/api/v1/vendor/{vendor['id']}").raise_for_status()


def test_spool_id_is_string():
    """Test that spool IDs are serialized as strings to prevent JavaScript precision loss."""
    # Create a vendor
    vendor_result = httpx.post(
        f"{URL}/api/v1/vendor",
        json={"name": "Test Vendor"},
    )
    vendor_result.raise_for_status()
    vendor = vendor_result.json()

    # Create a filament
    filament_result = httpx.post(
        f"{URL}/api/v1/filament",
        json={
            "vendor_id": vendor["id"],
            "density": 1.25,
            "diameter": 1.75,
        },
    )
    filament_result.raise_for_status()
    filament = filament_result.json()

    # Create a spool
    result = httpx.post(
        f"{URL}/api/v1/spool",
        json={
            "filament_id": filament["id"],
        },
    )
    result.raise_for_status()
    spool = result.json()

    # Verify ID is a string
    assert isinstance(spool["id"], str), f"Spool ID should be string, got {type(spool['id'])}"

    # Verify nested filament ID is also a string
    assert isinstance(
        spool["filament"]["id"],
        str,
    ), f"Nested filament ID should be string, got {type(spool['filament']['id'])}"

    # Verify nested vendor ID is also a string
    assert isinstance(
        spool["filament"]["vendor"]["id"],
        str,
    ), f"Nested vendor ID should be string, got {type(spool['filament']['vendor']['id'])}"

    # Clean up
    httpx.delete(f"{URL}/api/v1/spool/{spool['id']}").raise_for_status()
    httpx.delete(f"{URL}/api/v1/filament/{filament['id']}").raise_for_status()
    httpx.delete(f"{URL}/api/v1/vendor/{vendor['id']}").raise_for_status()


def test_vendor_list_ids_are_strings():
    """Test that vendor IDs in list responses are serialized as strings."""
    # Create a vendor
    create_result = httpx.post(
        f"{URL}/api/v1/vendor",
        json={"name": "Test Vendor"},
    )
    create_result.raise_for_status()
    vendor = create_result.json()

    # Get vendor list
    list_result = httpx.get(f"{URL}/api/v1/vendor")
    list_result.raise_for_status()
    vendors = list_result.json()

    # Verify all IDs in the list are strings
    assert len(vendors) > 0, "Vendor list should not be empty"
    for v in vendors:
        assert isinstance(v["id"], str), f"Vendor ID in list should be string, got {type(v['id'])}"

    # Clean up
    httpx.delete(f"{URL}/api/v1/vendor/{vendor['id']}").raise_for_status()
