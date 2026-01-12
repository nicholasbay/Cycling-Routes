import L from 'leaflet';

export const UserPositionIcon = L.icon({
  iconUrl: '/icons/position.png',
  iconSize: [32, 32],
  iconAnchor: [16, 16],
  popupAnchor: [0, -16]
})

export const StartPointIcon = L.icon({
  iconUrl: '/icons/location-blue.png',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32]
})

export const EndPointIcon = L.icon({
  iconUrl: '/icons/location-red.png',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32]
})

export const ParkingIcon = L.icon({
  iconUrl: '/icons/bike-parking.png',
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32]
})
