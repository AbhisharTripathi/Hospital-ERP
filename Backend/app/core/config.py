from pydantic_settings import BaseSettings, SettingsConfigDict







class Settings(BaseSettings):
   
    MONGO_URI: str = "mongodb://127.0.0.1:27017/"
    DB_NAME: str = "dev_hospital_erp"
    SECRET_KEY: str = "dev_secret_key_for_local_only"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
   
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" 
    )

settings = Settings()