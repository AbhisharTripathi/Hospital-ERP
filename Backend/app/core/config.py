from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
   
    MONGO_URI: str = "mongodb://127.0.0.1:27017/"
    DB_NAME: str = "dev_hospital_erp"
    SECRET_KEY: str = "dev_secret_key_for_local_only"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    
    MAIL_USERNAME: str = "example@gmail.com"
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = "example@gmail.com"

    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"

    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    MAIL_FROM_NAME: str = "Hospital ERP"  
    
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" 
    )

settings = Settings()

# basesetting pydantic ka ek special class hai jo env ko automatic read aur validate karne ke liye bana hota hai
#setting config dict ye setting ki configuration ko set karne ke kaam aata hai
