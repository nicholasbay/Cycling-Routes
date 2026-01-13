import { useEffect } from 'react';
import { Marker, Polyline, Popup, useMap } from 'react-leaflet';

import { DEFAULT_ZOOM } from '@/constants';
import { useRoutes } from '@/contexts/RoutesContext';
import { decodePolyline } from '@/utils';

import { StartPointIcon, EndPointIcon, ParkingIcon, UserPositionIcon } from './Icons';

interface MapContentProps {
  userPosition: [number, number] | null;
}

export function MapContent({ userPosition }: MapContentProps) {
  const map = useMap();
  const { currentRoute } = useRoutes();

  useEffect(() => {
    if (userPosition) {
      map.flyTo(userPosition, DEFAULT_ZOOM, { duration: 1.5 });
    }
  }, [userPosition, map]);

  const routeCoords: [number, number][] = decodePolyline(currentRoute?.route_geometry || '');

  return (
    <>
      {userPosition && (
        <Marker position={userPosition} icon={UserPositionIcon}>
          <Popup>Current Location</Popup>
        </Marker>
      )}

      {currentRoute && (
        <>
          <Polyline positions={routeCoords} color='red' weight={8} />

          <Marker 
            position={routeCoords[0]} 
            icon={StartPointIcon}
          >
            <Popup>
              <div>
                <h3 className='font-semibold'>Start Point</h3>
                <p>{currentRoute.route_summary.start_point}</p>
              </div>
            </Popup>
          </Marker>

          <Marker 
            position={routeCoords[routeCoords.length - 1]} 
            icon={EndPointIcon}
          >
            <Popup>
              <div>
                <h3 className='font-semibold'>End Point</h3>
                <p>{currentRoute.route_summary.end_point}</p>
              </div>
            </Popup>
          </Marker>
        </>
      )}

      {currentRoute?.parking_spots.map((spot) => (
        <Marker 
          key={spot.id}
          position={[spot.coordinates.lat, spot.coordinates.lon]}
          icon={ParkingIcon}
        >
          <Popup>
            <div>
              <h3 className='font-semibold'>Bike Parking</h3>
              <p>{spot.description}</p>
              <p>Rack Type: {spot.rack_type}</p>
              <p>Rack Count: {spot.rack_count}</p>
              <p>Shelter: {spot.shelter_indicator}</p>
              {spot.deviation_m && (
                <p>Deviation: {spot.deviation_m} m</p>
              )}
            </div>
          </Popup>
        </Marker>
      ))}
    </>
  );
}