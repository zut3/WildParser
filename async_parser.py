import asyncio
import aiohttp
import time
import json
import _utils
from _utils import normalize_text as _
import aiofiles
from fake_useragent import UserAgent


template_products_url = "https://search.wb.ru/exactmatch/ru/common/v4/" \
                            "search?appType=1&curr=rub" \
                            "&emp=0" \
                            "$lang=ru&locale=ru&page={page}&pricemarginCoeff=1.0" \
                            "&query={query}&reg=0&resultset=catalog&sort=popular&spp=0"


template_product_description_url = "https://wbx-content-v2.wbstatic.net/ru/{idx}.json"


async def _collect_from_page(session, page, query):
    data = []
    json_ = await _utils.get_products(query, page, session)
    products = json_["data"]["products"]
    ids = tuple(map(lambda x: x['id'], products))

    for i, idx in enumerate(ids):
        product_description = await _utils.get_product_description(idx, session)
        if not product_description:
            continue
        str_description = _(product_description.get("description", ""))
        photo_count = product_description.get("media", {"photo_count": None}).get('photo_count')
        image_url = _utils.get_image_url(idx)
        name = _(product_description.get('imt_name') or products[i].get("name"))
        prev_price = products[i]["priceU"] // 100
        price_now = products[i]["salePriceU"] // 100
        diff_price = prev_price - price_now
        brand = _(product_description.get("selling", {"brand_name": None}).get("brand_name"))

        data.append({
            "name": name,
            "image": image_url,
            "prev_price": prev_price,
            "price": price_now,
            "price_diff": diff_price,
            "brand": brand,
            "photo_count": photo_count,
            "description": str_description
        })
    return data


async def collect_data_by_query(query: str) -> list:

    async with aiohttp.ClientSession(headers={
        "user-agent": UserAgent().random,
    }) as session:
        data = []
        page = 0
        print(session.headers)
        while True:
            page += 1
            data_from_page = await _collect_from_page(session, page, query)
            if not data_from_page:
                break
            data += data_from_page

    return data


async def _save_json(data, path: str) -> str:
    s = _(json.dumps(data, indent=4, ensure_ascii=False))
    async with aiofiles.open(path, "w", encoding="cp1251") as f:
        await f.write(s)
    return path


async def _create_tasks():
    li = ["iphone"]
    tasks = []

    for el in li:
        task = asyncio.create_task(collect_data_by_query(el))
        tasks.append(task)
    return await asyncio.gather(*tasks)

if __name__ == '__main__':
    s_t = time.time()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(_create_tasks())
    print(res)
    print(round(time.time() - s_t, 5))
