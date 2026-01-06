from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

client = TestClient(app)
prefix = '/api/v1'


class TestSearchEndpoint:
    def test_valid_search():
        mock_api_response = {
            "results": [
                {
                    "SEARCHVAL": "EAST COAST PARK OFFICE",
                    "BLK_NO": "906",
                    "ROAD_NAME": "EAST COAST PARKWAY",
                    "BUILDING": "EAST COAST PARK OFFICE",
                    "ADDRESS": "906 EAST COAST PARKWAY EAST COAST PARK OFFICE SINGAPORE 449895",
                    "POSTAL": "449895",
                    "X": "35574.200743217",
                    "Y": "31122.488094667",
                    "LATITUDE": "1.29773431957503",
                    "LONGITUDE": "103.901376105637"
                }
            ]
        }

        with patch('requests.get') as mock_get:
            mock_get.return_value.json = MagicMock(return_value=mock_api_response)
            mock_get.return_value.status_code = 200

            response = client.get(f'{prefix}/search', params={'searchVal': 'EAST COAST PARK OFFICE', 'pageNum': 1})

            assert response.status_code == status.HTTP_200_OK
            assert response.json() == mock_api_response['results']
            mock_get.assert_called_once()


    def test_search_missing_searchVal():
        response = client.get(f'{prefix}/search')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


    def test_search_invalid_method():
        response = client.post(f'{prefix}/search', json={"searchVal": "test"})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

class TestRoutesEndpoint:
    def test_valid_routes():
        mock_api_response = [
            {
                "route_geometry": "...",  # Encoded polyline as per OneMap response
                "route_instructions": [  # Only keep top-level instructions?
                    "...",
                    "..."
                ],
                "route_summary": {  # Summary details as per OneMap response
                    "start_point": "...",
                    "end_point": "...",
                    "total_time_s": ...,  # Renamed from "total_time
                    "total_distance_m": ...,  # Renamed from "total_distance"
                },
                "parking_spots": [  # List of parking spots along the route
                    {
                        "description": "...",
                        "coordinates": { "lat": ..., "lon": ... },
                        "rack_type": "...",
                        "rack_count": ...,
                        "shelter_indicator": "..."
                    },
                ]
            }
        ]

        with patch('requests.get') as mock_get:
            mock_get.return_value.json = MagicMock(return_value=mock_api_response)
            mock_get.return_value.status_code = 200

            response = client.get(f'{prefix}/routes', params={'start': 'start', 'end': 'end', 'intervalMins': 30})
            assert response.status_code == status.HTTP_200_OK


        """
        [  # List of routes
            {
                "route_geometry": "...",  # Encoded polyline as per OneMap response
                "route_instructions": [  # Only keep top-level instructions?
                    "...",
                    "..."
                ],
                "route_summary": {  # Summary details as per OneMap response
                    "start_point": "...",
                    "end_point": "...",
                    "total_time_s": ...,  # Renamed from "total_time
                    "total_distance_m": ...,  # Renamed from "total_distance"
                },
                "parking_spots": [  # List of parking spots along the route
                    {
                        "description": "...",
                        "coordinates": { "lat": ..., "lon": ... },
                        "rack_type": "...",
                        "rack_count": ...,
                        "shelter_indicator": "..."
                    },
                ],
            },
            {...}
        ]
        """
