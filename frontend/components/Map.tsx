import { MapContainer, TileLayer, ZoomControl } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet-defaulticon-compatibility';
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css';

import { MapContent } from './MapContent';
import { DEFAULT_CENTER, DEFAULT_ZOOM} from '@/constants';

export default function Map(props: any) {
  const { userPosition } = props

  return (
    <MapContainer
      className='h-full w-full'
      center={DEFAULT_CENTER}
      zoom={DEFAULT_ZOOM}
      scrollWheelZoom={true}
      zoomControl={false}
    >
      <ZoomControl position='bottomright' />
      <TileLayer
        maxZoom={19}
        minZoom={11}
        attribution='<a href="https://www.onemap.gov.sg/" target="_blank" rel="noopener noreferrer">OneMap</a>&nbsp;&copy;&nbsp;contributors&nbsp;&#124;&nbsp;<a href="https://www.sla.gov.sg/" target="_blank" rel="noopener noreferrer">Singapore Land Authority</a>'
        url='https://www.onemap.gov.sg/maps/tiles/Default_HD/{z}/{x}/{y}.png'
      />
      <MapContent userPosition={userPosition} />
    </MapContainer>
  );
}
