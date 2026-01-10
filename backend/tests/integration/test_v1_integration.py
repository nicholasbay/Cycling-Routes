from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

client = TestClient(app)
prefix = '/api/v1'


class TestSearchEndpoint:
    def test_valid_search_integration(self):
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


    def test_valid_search_integration_no_results(self):
        response = client.get(
            f'{prefix}/search',
            params={'searchVal': 'bhgrt4u2r3qoiwjaskfjnbhuw', 'pageNum': 1}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0


class TestRoutesEndpoint:
    def test_valid_routes_integration(self):
        response = client.get(
            f'{prefix}/routes',
            params={
                'start': '1.29443776056092%2C103.872537189913',  # ECP Area A
                'end': '1.31344532512062%2C103.957814209908',  # ECP Area G
                'intervalMins': 20
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        # Verify structure of first route
        first_route = data[0]
        expected_keys = {"route_geometry", "route_instructions", "route_summary", "parking_spots"}
        assert expected_keys.issubset(first_route.keys())

        assert isinstance(first_route["route_geometry"], str)
        assert isinstance(first_route["route_instructions"], list)
        assert isinstance(first_route["route_summary"], dict)
        assert isinstance(first_route["parking_spots"], list)

        # Verify structure of route summary
        summary_keys = {"start_point", "end_point", "total_time_s", "total_distance_m"}
        assert summary_keys.issubset(first_route["route_summary"].keys())

        # Verify structure of first parking spot, if available
        if len(first_route["parking_spots"]) > 0:
            first_spot = first_route["parking_spots"][0]
            spot_keys = {"id", "description", "coordinates", "rack_type", "rack_count", "shelter_indicator", "deviation_m"}
            assert spot_keys.issubset(first_spot.keys())
            assert isinstance(first_spot["coordinates"], dict)
            assert {"lat", "lon"}.issubset(first_spot["coordinates"].keys())


    def test_routes_invalid_params(self):
        response = client.get(
            f'{prefix}/routes',
            params={
                'start': '1.29443776056092,103.872537189913',
                # Missing 'end' parameter
                'intervalMins': 20
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
