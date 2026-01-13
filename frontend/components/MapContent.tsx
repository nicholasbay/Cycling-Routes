import { useEffect } from 'react';
import { Marker, Polyline, Popup, useMap } from 'react-leaflet';

import { StartPointIcon, EndPointIcon, ParkingIcon, UserPositionIcon } from './Icons';
import { DEFAULT_ZOOM } from '@/constants';

var polyUtil = require('polyline-encoded');

interface MapContentProps {
  userPosition: [number, number] | null;
}

const polylineStr = 'ay{Fkr~xRAM?[AY?]CO?GAE?E@C?CDKLUHQFOJUNa@?A@??EBM@E@EZ[HGHIHIPQJIHKPQRQJIRUVULMDEFGDEBG@CDIBIBK@K@K?GAIAIAGAICEAEAECEEEEGEEGE??AAKGCAGCUI]MUGYKKEKEMEKEECICIGKGIGEEGEEECCEECEEGIMGKEGCEEKCECGCIAC?E?E?EA_AAk@AgAAq@?_AC}@CaBAs@A_AAiAAmAAi@?gC?G?s@Am@?]?g@?o@?]?W?Y@O?I@CBa@Dw@Bq@DWBMJg@DcA@gAAS??ASAQA]AYEgAMo@@s@@[BG?MAIB]@U@a@@_@@S@O@WBW??@S@WB[@UBe@???S@a@@W@U?C?O?W@W?G@Y?I@a@AQ?WAQ?MAOAI?KAMAIAQ?MASAYCUAUAUA[@IAKEI??AMCQESAIAIESCSAC???GAEAICWEg@AEAMAUEc@CWAWC[AK@IAYCKAWCWAO?KAKCm@AUAE?AAQAO?QC]CWAS?IAUAQAM?G?GAGCQEUESEQIe@GWGSCKG]CICOCQAKAIAI?IAM?G?I?K?I?K?I?KAQ?IAKAIAIAQ@CE[EWCCEYCSAG?CACAGCIIUEKIUIWK[M_@CIEK?KCKEGCY?K?M?M?M?O@K?K?G?MAA?GAOAECIAECIK_@ESIW?IEKCGK[Qs@Mc@IYGW??CQGYCOIc@?EI[AICKEGEKEQEOGOCOCMCKCKCMCQAGAQCQCQCQAQCQ?IAMEGAIAIAGCGCICCCECEEEKMKOGKEECEAGCGEIAECG???AAGCOAIESCOAQCK@E?CAKCICQ?EAGAE?ACGCICGAG?A?EAG?GA[AQAYC_@AGAKAKAEAEQm@EOESC[CWAC?A@C?EBQ?E@C?CACAOE]Ec@CQ?KIUCUEWIe@EOCISg@MYISGMCIIQCG?AISEKCICIGWCMCOCSCIAICIAICIEQAICMCMCKAGAAAGAIAGAE???A??AM?K?A?OAMAKCKCKEOGMEKIOEIIMAAOYGKCEGMCEEKCGAG?AAEAGAG?MAI?ECGCGSa@IQKQCIOWGQCSES?CCKCGEICCIQCEECGKMOACCEEUIe@G[?C?CFMBIBG@I@G??AIEW?CAA?AEKEIOYO]IO?AAO?A?AACQWEGGIMQEGSYAACGCMCMAA??CKCI?EAAAACAEIEOGSG[Ia@?IIk@E]?AAEGa@Gc@EU?ICMEGAG?A??G[??EOAICGCICGEKGKIO?CACE]EWGYEYE]CUAY?EAAAOGc@Ea@EUCO?CAC?CACA?AA?CACACCIAGAECEEEKWAEACAAACACGSEKCICGEMCKCIAKCI?A?AACEUAEAKCK??@EAKCE?CAIAOAIAQAO?C?_@?UAO?[?[?U?S?m@Gm@Ge@AIE[CUACCIAECEEKGK?AEEGMCGACACAA?CAA?C?E?I?W?G?G?A?]AMAWAWAOCMAOCQAECQ?CCI??AEACAEAICKCICKGSGSMi@Su@MaAEiAMiBOKEGEEGEIEICEAGAI?IAE?A@I?A?GAGACACACAEAEEECOOQMEE??CC???AAA???A@C?A?A@C@CDKBK@G?E?M?IAKAEAKACC_@ACEMCGAEEIAGCKCCCAEMKYCAACAE?G?CGBE@QHs@q@UT[ZkAkAqBiB[PSLs@aDk@sEEaADu@Lo@~AuDDYHw@A_@IaAI]c@_Aa@e@SS]YKIiAs@mAw@[[a@i@Se@Mc@Q_Aa@aC}@eFBiCIOKEWMOS}CwPYsBUaC?cACuBEiFB}@~A{K?k@Mk@uVoy@Oe@AEAG`@MRIDAAAIo@EYE[EU?AZTVTHFHHLJLJHDDDFBDBB?@@B?B@B?@?@?B@B?@?BAB?R?NAB?B?@@@?@?@@@?@@?@B?@B@?@@BBBB@@BB@BBB@DBDBDFHBDBFDFBFBFDDBFFLFLBHDHBJBH@NBJ@L@L@H@D@H';
const latlngs = polyUtil.decode(polylineStr);
console.log(latlngs[0], latlngs[latlngs.length - 1]);

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
      {/* Placeholder */}
      <Polyline positions={latlngs} color='red' weight={8}/>

      <Marker position={latlngs[0]} icon={StartPointIcon}>
        <Popup>Start Point</Popup>
      </Marker>

      <Marker position={latlngs[latlngs.length - 1]} icon={EndPointIcon}>
        <Popup>End Point</Popup>
      </Marker>

      <Marker position={latlngs[Math.floor(latlngs.length / 2)]} icon={ParkingIcon}>
        <Popup>Bike Parking</Popup>
      </Marker>
    </>
  );
}