from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # баг: Без extra="ignore" Pydantic v2 выбрасывал ошибку при неизвестных полях
        extra="ignore",
    )

    # баг: Опечатка в validation_alias, было "DATABSE_URL" вместо "DATABASE_URL"
    database_url: str = Field(
        "postgresql+asyncpg://postgres:postgres@db:5432/postgres",
        validation_alias="DATABASE_URL",
    )
    # баг: Отсутствовала настройка api_url парсер не мог получить URL
    api_url: str = Field(
        "https://api.selectel.ru/proxy/public/employee/api/public/vacancies",
        validation_alias="API_URL",
    )
    log_level: str = "INFO"
    parse_schedule_minutes: int = 5


settings = Settings()
