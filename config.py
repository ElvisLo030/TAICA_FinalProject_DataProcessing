import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self._api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    @property
    def api_key(self) -> str:
        if not self._api_key:
            raise ValueError("GOOGLE_MAPS_API_KEY not found in environment variables.")
        return self._api_key

