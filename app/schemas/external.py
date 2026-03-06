from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field  # баг: нужен ConfigDict для populate_by_name


class ExternalCity(BaseModel):
    id: int
    name: str


class ExternalTag(BaseModel):
    id: int
    name: str
    description: str


class ExternalTimetableMode(BaseModel):
    id: int
    name: str


class ExternalVacancyItem(BaseModel):
    id: int
    title: str
    timetable_mode: ExternalTimetableMode
    tag: ExternalTag
    city: Optional[ExternalCity]
    published_at: datetime
    is_remote_available: bool
    is_hot: bool


class ExternalVacanciesResponse(BaseModel):
    # баг: Без populate_by_name=True Pydantic не может распарсить поле с alias
    model_config = ConfigDict(populate_by_name=True)

    item_count: int = Field(alias="item_count")
    items: List[ExternalVacancyItem]
    items_per_page: int
    page: int
    page_count: int
