import { useEffect } from 'react';
import { Marker, Popup, useMap } from 'react-leaflet';

import { StartPointIcon, EndPointIcon, ParkingIcon, UserPositionIcon } from './Icons';
import { DEFAULT_ZOOM } from '@/constants';

interface MapContentProps {
  userPosition: [number, number] | null;
}

export function MapContent({ userPosition }: MapContentProps) {
  const map = useMap();

  useEffect(() => {
    if (userPosition) {
      map.flyTo(userPosition, DEFAULT_ZOOM, { duration: 1.5 });
    }
  }, [userPosition, map]);

  return (
    <>
      {userPosition && (
        <Marker position={userPosition} icon={UserPositionIcon}>
          <Popup>Your Location</Popup>
        </Marker>
      )}

      {/* TODO: Routes, start/end points, parking markers */}
    </>
  );
}