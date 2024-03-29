from pydantic import BaseSettings


class Settings(BaseSettings):
    LOGIN_ACCOUNT_COMPONENT_NAME: str = "default"
    SECRET_KEY: str = "this is a secret key"
    RUNTIME_ENVIRONMENT: str = "dev"
    CSRF_COOKIE_DOMAIN: str = ""
    LOGIN_AUTH_URL: str = ""
    SUPERUSERS: str = ""
    CORS_ALLOWED_HOSTS: str = ""
    FRONTEND_LOGIN_URL: str = "xxx"
    MYSQL_DATABASE_NAME: str = ""
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_HOST: str = ""
    MYSQL_PORT: str = ""

    class Config:
        case_sensitive = True

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                env_settings,
                file_secret_settings,
            )


settings = Settings()
