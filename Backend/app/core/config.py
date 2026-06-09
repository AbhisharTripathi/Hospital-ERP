from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URI : str = "mongodb://127.0.0.1:27017/"
    DB_NAME : str = "dev_hospital_erp"
    SECRET_KEY : str = "dev"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()