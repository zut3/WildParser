import aiohttp
import json
from typing import Optional

template_products_url = "https://search.wb.ru/exactmatch/ru/common/v4/" \
                            "search?appType=1&curr=rub" \
                            "&emp=0" \
                            "$lang=ru&locale=ru&page={page}&pricemarginCoeff=1.0" \
                            "&query={query}&reg=0&resultset=catalog&sort=popular&spp=0"


template_product_description_url = "https://wbx-content-v2.wbstatic.net/ru/{idx}.json"


def get_image_url(index: str) -> str:
    template_images_url = "https://images.wbstatic.net/c516x688/new/{collection}/{idx}.jpg"
    return template_images_url.format(collection=str(index)[:4] + "0000", idx=str(index) + "-1")


def normalize_text(text: str | None) -> Optional[str]:
    """Преобразует русским текстом, для нормального отображения"""
    if text:
        return text.encode("cp1251", "ignore").decode("cp1251", "ignore")


async def get_products(query: str, page: int, session: aiohttp.ClientSession) -> dict:
    async with session.get(template_products_url.format(query=query, page=page)) as response:
        text = await response.read()
        return json.loads(text)


async def get_product_description(product_id: int, session: aiohttp.ClientSession) -> Optional[dict]:
    async with session.get(template_product_description_url.format(idx=product_id)) as response:
        text = await response.read()
        if not text:
            return None
        return json.loads(text)


