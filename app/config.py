from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    bucket_name: str
    aws_access_key_id: str
    aws_secret_access_key: str
    
    class Config:
        env_file = ".env"


settings = Settings()