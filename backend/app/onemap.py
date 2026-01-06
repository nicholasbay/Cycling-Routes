from datetime import datetime, timedelta
import threading
from typing import Optional

from fastapi import HTTPException, status
import requests

from app.config import get_settings


class ApiKeyManager:
    def __init__(self):
        self._key: Optional[str] = None
        self._expiry_datetime: Optional[datetime] = None
        self._lock = threading.Lock()
        self.REFRESH_BUFFER_S = 300

    def get_api_key(self) -> str:
        current_datetime = datetime.now()

        # Check if current key is valid
        if self._key and self._expiry_datetime:
            if current_datetime < (self._expiry_datetime - timedelta(seconds=self.REFRESH_BUFFER_S)):
                return self._key

        # Refresh with lock
        with self._lock:
            if self._key and self._expiry_datetime:
                if current_datetime < (self._expiry_datetime):
                    return self._key
            self._refresh_api_key()
            return self._key


    def _refresh_api_key(self):
        settings = get_settings()

        try:
            response = requests.post(
                'https://www.onemap.gov.sg/api/auth/post/getToken',
                json={
                    'email': settings.ONEMAP_EMAIL,
                    'password': settings.ONEMAP_PASSWORD
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            self._key = data['access_token']
            expiry_s = int(data['expiry_timestamp'])
            self._expiry_datetime = datetime.fromtimestamp(expiry_s)
        except requests.RequestException as e:
            self._key = None
            self._expiry_datetime = None
            raise HTTPException(status_code=status.HTTP_503, detail=e)


_api_key_manager: Optional[ApiKeyManager] = None

def get_api_key_manager() -> ApiKeyManager:
    global _api_key_manager
    if _api_key_manager is None:
        _api_key_manager = ApiKeyManager()
    return _api_key_manager
