import logging
from src.Application.settings import settings

from src.Services.ApiService import ApiService

# can move this logger config to another module so it can be reuse in other services
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class App:
    def __init__(self, url: str = str(settings.APISERVICE_URL), path: str = settings.APISERVICE_PATH):
        self._api_service = ApiService(url=url, path=path, override_files=settings.APISERVICE_OVERRIDE_FILES)

    def api_service(self) -> ApiService:
        return self._api_service
