from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DEBUG: bool = False

    # APIService
    APISERVICE_URL: AnyUrl = 'https://jsonplaceholder.typicode.com/todos/'
    APISERVICE_PATH: str = 'storage'
    APISERVICE_OVERRIDE_FILES: bool = True


settings = Settings()
