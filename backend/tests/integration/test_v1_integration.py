from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

client = TestClient(app)
prefix = '/api/v1'


def test_valid_search_integration():
    response = client.get(
        f'{prefix}/search',
        params={'searchVal': 'EAST COAST PARK OFFICE', 'pageNum': 1}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Verify result structure (based on OneMap API response)
    first_result = data[0]
    expected_keys = {
        "SEARCHVAL", "BLK_NO", "ROAD_NAME", "BUILDING", "ADDRESS",
        "POSTAL", "X", "Y", "LATITUDE", "LONGITUDE"
    }
    assert expected_keys.issubset(first_result.keys())


def test_valid_search_integration_no_results():
    response = client.get(
        f'{prefix}/search',
        params={'searchVal': 'bhgrt4u2r3qoiwjaskfjnbhuw', 'pageNum': 1}
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
