from typing import List, Dict


def transform_route_data(route_data: Dict, parking_spots: List[Dict]) -> Dict:
    """
    Transform OneMap route response data to application format.
    
    Args:
        route_data: Raw route data from OneMap API.
        parking_spots: List of parking spots along the route.
    """
    # Keep only top-level instructions
    route_instructions = route_data.get('route_instructions', [])
    filtered_instructions = [ri[-1] for ri in route_instructions]

    route_summary = route_data.get('route_summary', {})

    return {
        'route_geometry': route_data.get('route_geometry', ''),
        'route_instructions': filtered_instructions,
        'route_summary': {
            'start_point': route_summary.get('start_point', 'N/A'),
            'end_point': route_summary.get('end_point', 'N/A'),
            'total_time_s': route_summary.get('total_time', 0),
            'total_distance_m': route_summary.get('total_distance', 0),
        },
        'parking_spots': [
            {
                'id': spot.get('id', 'N/A'),
                'description': spot.get('description', 'N/A'),
                'coordinates': {
                    'lat': spot.get('coord', (0.0, 0.0))[1],
                    'lon': spot.get('coord', (0.0, 0.0))[0]
                },
                'rack_type': spot.get('rack_type', 'N/A'),
                'rack_count': spot.get('rack_count', 0),
                'shelter_indicator': spot.get('shelter_indicator', 'N/A'),
                'deviation_m': spot.get('deviation', 0.0)
            }
            for spot in parking_spots
        ]
    }