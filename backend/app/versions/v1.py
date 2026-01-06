from typing import Annotated

from dotenv import load_dotenv
from fastapi import (
    APIRouter,
    Depends,
    status
)
from fastapi.responses import JSONResponse
import requests

from app.config import Settings, get_settings
from app.onemap import ApiKeyManager, get_api_key_manager
from app.utils.parking import convert_time_interval_to_distance, find_parking_spots_along_route

load_dotenv()
router = APIRouter(
    prefix='/api/v1',
    tags=['v1']
)
ApiDep = Annotated[ApiKeyManager, Depends(get_api_key_manager)]
SettingsDep = Annotated[Settings, Depends(get_settings)]

@router.get('/search')
def search(
    api_dep: ApiDep,
    settings_dep: SettingsDep,
    searchVal: str,
    pageNum: int = 1
):
    try:
        token = api_dep.get_api_key()
        response = requests.get(
            f'{settings_dep.ONEMAP_BASE_URL}/api/common/elastic/search?searchVal={searchVal}&returnGeom=Y&getAddrDetails=Y&pageNum={pageNum}',
            headers={'Authorization': f'Bearer {token}'}
        )
        response.raise_for_status()
        data = response.json()
        results = data.get('results', [])
        return JSONResponse(
            content=results,
            status_code=status.HTTP_200_OK
        )
    except requests.RequestException as e:
        return JSONResponse(
            content={'error': str(e)},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


@router.get('/routes')
def get_routes(
    api_dep: ApiDep,
    settings_dep: SettingsDep,
    start: str,
    end: str,
    intervalMins: int = 30
) -> JSONResponse:
    """
    Returns a list of routes with its associated bicycle parking spots.
    """
    return {"message": "Routes endpoint"}
