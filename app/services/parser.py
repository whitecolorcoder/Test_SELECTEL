import logging

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.vacancy import upsert_external_vacancies
from app.schemas.external import ExternalVacanciesResponse

logger = logging.getLogger(__name__)


async def fetch_page(client: httpx.AsyncClient, page: int) -> ExternalVacanciesResponse:
    response = await client.get(
        settings.api_url,
        params={"per_page": 1000, "page": page},
    )
    response.raise_for_status()
    return ExternalVacanciesResponse.model_validate(response.json())


async def parse_and_store(session: AsyncSession) -> int:
    logger.info("Старт парсинга вакансий")
    created_total = 0

    # баг: httpx.AsyncClient не использовался с async with (утечка ресурсов)
    timeout = httpx.Timeout(10.0, read=20.0)
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            page = 1
            while True:
                payload = await fetch_page(client, page)
                parsed_payloads = []
                for item in payload.items:
                    # баг: Без проверок на None падало при отсутствии city/timetable_mode/tag
                    parsed_payloads.append(
                        {
                            "external_id": item.id,
                            "title": item.title,
                            "timetable_mode_name": item.timetable_mode.name if item.timetable_mode else None,
                            "tag_name": item.tag.name if item.tag else None,
                            "city_name": item.city.name.strip() if item.city and item.city.name else None,
                            "published_at": item.published_at,
                            "is_remote_available": item.is_remote_available,
                            "is_hot": item.is_hot,
                        }
                    )

                created_count = await upsert_external_vacancies(session, parsed_payloads)
                created_total += created_count

                if page >= payload.page_count:
                    break
                page += 1
    except (httpx.RequestError, httpx.HTTPStatusError) as exc:
        logger.exception("Ошибка парсинга вакансий: %s", exc)
        return 0

    logger.info("Парсинг завершен, новых вакансий: %s", created_total)
    return created_total
