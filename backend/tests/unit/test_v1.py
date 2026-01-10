from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from fastapi import status

from app.main import app

client = TestClient(app)
prefix = '/api/v1'


class TestSearchEndpoint:
    def test_valid_search(self):
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


    def test_search_missing_searchVal(self):
        response = client.get(f'{prefix}/search')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


    def test_search_invalid_method(self):
        response = client.post(f'{prefix}/search', json={"searchVal": "test"})
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

class TestRoutesEndpoint:
    def test_valid_routes(self):
        mock_onemap_response = {
            'route_geometry': 'ay{Fkr~xRAM?[AY?]CO?GAE?E@C?CDKLUHQFOJUNa@?A@??EBM@E@EZ[HGHIHIPQJIHKPQRQJIRUVULMDEFGDEBG@CDIBIBK@K@K?GAIAIAGAICEAEAECEEEEGEEGE??AAKGCAGCUI]MUGYKKEKEMEKEECICIGKGIGEEGEEECCEECEEGIMGKEGCEEKCECGCIAC?E?E?EA_AAk@AgAAq@?_AC}@CaBAs@A_AAiAAmAAi@?gC?G?s@Am@?]?g@?o@?]?W?Y@O?I@CBa@Dw@Bq@DWBMJg@DcA@gAASI?QAg@Am@AiCB_AC_DBiB?eAAe@Ae@AeAA[AwCK{DKk@Na@RUPQPc@b@s@d@w@LgDLh@k@D_AE{A}ADsAD_CF]@iELG?I@G@EBQJ?CCAAA[K??q@sHC[_@eE]sDI{@AMIk@GMKWKMIKSUA?EESM_@Oe@Ge@Ce@D_G~@L|@dBY^G?BwCb@mBXm@JK@QBcDf@uGjA?@Fb@Fj@UBQBOiAAME@_CZI@I?A?I@OAKAMCKCQIIGIGAAGGEIGKIUOi@Ki@McA??Im@AMk@aFCOOsAE_@AGw@Aq@CO?C?C?CWqAKiAO_C_@c@A}@D_ALOiBYwDI_AOgBEc@[{DMuAQsB}C\\WBEWqA}Kq@aG??TE@?fC[AO?ACWa@mDyAeMIo@Ik@C][}AEY??AKAEEW?ACSCQCU?G?AAKm@iIUgC??E[g@_E??KaAIg@m@gECY??Kw@[cC??a@eDUmBRCLCHA?Ai@eDQBEYWwCS@CQC]AQEo@AE?GAIMeBGmB?a@?g@?O?Q@ABk@Ci@?M?WFq@FE?CDgBAq@Q{AU_AIWSMAK?MEGEMACGEYLcAJyAJS?S@C?_@Dm@DS?w@?_@ASCq@Gq@MgAUSAg@Ai@He@LQHeAf@IFA@SJA?KFKFCDWPm@l@}@hAE?G?[Ui@o@s@}@}@{BGUEa@EQKOQc@K_@AEQcBAQCi@AQAg@?GAUAW?C?MA]?O?a@@_@D_@DC?SAGFo@NkBAEHm@Hg@Ha@LCHAh@Fb@@n@JP@BS?KMCgBUMECCAC?C@QNOPKHCbA_@L@NK@KDCRSRWR]JOFOL]J_@D[DY?Q@Y?U?IB]?I?A?AB]CMBeC@E@IL}@B]Fy@@o@CE@MAME]AKYcAGOEO??]aAa@kAaAqCMi@KBK@A???M@C@CB?B?BA@A@C@G@wC\\GBCBeAJC?UCU@UNyAPAEmANC@G@oANG?EAc@_DuBgOG?Ik@[DUBCSCKEO?CAEIk@ACCUAEOSEWDUKy@CQAMUyAIaAA_@Ag@?i@DcAFe@Di@ULiC?MAIECC_@uCEKWBE_@e@uCTCEOu@yDAGCKS}@QaBOmAEa@CSACAKMw@?GUBOsAI]MWU[c@Yu@QuBS?C_@E@A@K?C@I^D?E?ABU|Dc]?GLaArBqAJKFGDCLKfTeMBAHEHGJGt@bA??JJHE????@A??DCZQJI`@S`@_@TS@A@??ATMb@W\\S@Ab@WDCTMFELGVQRKb@WNKh@YZQ?Ap@_@b@Wz@g@LIHGHIJKNQ??JOd@m@NQLOh@q@V]Za@HKf@m@\\c@BEJE@CHSRU@C??RW??h@o@??b@k@@A@A@?@ADCBADCBEBC@C@C?E@A?CBCHMRUPU@ABA@?@ABADCDGDGBEBE@C?C@C@AJO@AFGBELSFIJMJMFGHMBADGBAJMPU@CBA@ADA@A@ABA@CBCBGBGBG@CBC^e@DEBCB?BCDEDEBG@A@C@EBE@CBCJMl@w@?AFCB?@A@@B@B@?@@@BFRd@P\\@BBFHNBFXl@JTb@|@FLLTTd@BDFJNX@BNZDJHNNXBF@B@@@@??@@@@DB@?F@?@JBB@@?@@@?B@?B@?BFJRBF@B@B@B@D?@@@@@@@BB@D@D@B@D@BBBB?AH?BEX@@B??@@HDF@B@DFPDJL`@HRFPDL@BBD?@@@?@JRL\\DL@D?@BJ@F?@@@?@Pd@DLDLBNHNFNFPDHBHBJBD@DBL@@BJ@DBH@B@FHPBF@D@BBF@DBDDFDHBFDF@@BDL@F?J@F@H@B?PBRBD@D?F@RBT@RBF@PBrVhCD@DDB@BBBBBBHLFF??DFFHBDHJLNLPJNNPRTBD@?LCHCHCRGTGHCJED?IYSq@Qi@aBqFc@wACKEMCGEKAGCGGSCIK_@GUIUMc@EKCG?GAOAEACGWOe@K_@Ma@IYc@qAAECKCKKYGQGSYaA]iA]mAK]Wy@]gACIxBu@`@MRIDAAAIo@EYE[EU?AZTVTHFHHLJLJHDDDFBDBB?@@B?B@B?@?@?B@B?@?BAB?R?NAB?B?@@@?@?@@@?@@?@B?@B@?@@BBBB@@BB@BBB@DBDBDFHBDBFDFBFBFDDBFFLFLBHDHBJBH@NBJ@L@L@H@D@H',  # Sample encoded polyline as per OneMap response
            'route_instructions': [
                ['...'],
                ['...']
            ],
            'route_summary': {
                'start_point': 'Start Point',
                'end_point': 'End Point',
                'total_time': 1800,
                'total_distance': 5000
            }
        }
        mock_parking_spots = [
            {
                'id': 1,
                'description': 'Parking Spot 1',
                'coordinates': {'lat': 1.3000, 'lon': 103.9000},
                'rack_type': 'Type A',
                'rack_count': 10,
                'shelter_indicator': 'Y',
                'deviation_m': 50.0
            }
        ]
        mock_transformed_data = {
            'route_geometry': mock_onemap_response['route_geometry'],
            'route_instructions': ['...','...'],
            'route_summary': {
                'start_point': 'Start Point',
                'end_point': 'End Point',
                'total_time_s': 1800,
                'total_distance_m': 5000
            },
            'parking_spots': mock_parking_spots
        }

        with (
            patch('requests.get') as mock_get,
            patch('app.versions.v1.find_parking_spots_along_route') as mock_find_parking,
            patch('app.versions.v1.transform_route_data') as mock_transform_data
        ):
            mock_get.return_value.json = MagicMock(return_value=mock_onemap_response)
            mock_get.return_value.status_code = 200
            mock_find_parking.return_value = mock_parking_spots
            mock_transform_data.return_value = mock_transformed_data

            response = client.get(f'{prefix}/routes', params={
                'start': '1.29443776056092%2C103.872537189913',
                'end': '1.31344532512062%2C103.957814209908',
            })

            assert response.status_code == status.HTTP_200_OK
            mock_get.assert_called_once()
            mock_find_parking.assert_called()  # To find the parking spots for a given route
            mock_transform_data.assert_called()  # To transform the route data into the expected format
