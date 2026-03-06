from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class VacancyBase(BaseModel):
    # баг: timetable_mode_name и tag_name были обязательными (str), но в БД колонки nullable, что вызывало ошибки при парсинге
    title: str
    timetable_mode_name: Optional[str] = None
    tag_name: Optional[str] = None
    city_name: Optional[str] = None
    published_at: datetime
    is_remote_available: bool
    is_hot: bool
    external_id: Optional[int] = None


class VacancyCreate(VacancyBase):
    pass


class VacancyUpdate(VacancyBase):
    pass


class VacancyRead(VacancyBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
