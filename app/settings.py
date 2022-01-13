from pydantic import BaseSettings


class Settings(BaseSettings):
    bucket: str = "gilman-finances"
    working_dir: str = "/tmp/bean"
    bean_file: str = "gilman.beancount"


settings = Settings()
