import asyncio
import aiohttp
import time
import json
import _utils
from _utils import normalize_text as _
import aiofiles
from fake_useragent import UserAgent


# template_products_url = "https://search.wb.ru/exactmatch/ru/common/v4/" \
#                             "search?appType=1&curr=rub" \
#                             "&emp=0" \
#                             "$lang=ru&locale=ru&page={page}&pricemarginCoeff=1.0" \
#                             "&query={query}&reg=0&resultset=catalog&sort=popular&spp=0"

template_products_url = "https://search.wb.ru/exactmatch/ru/common/v4/search?" \
                        "appType=1&couponsGeo=2,12,7,3,6,18,21&curr=rub&dest=-1029256,-81994,-912503,-941037&emp=0&lang=ru&locale=ru&page={page}&pricemarginCoeff=1.0&query={query}&reg=0&regions=68,64,83,4,38,80,33,70,82,86,30,69,22,66,31,40,1,48&resultset=catalog&sort=popular&spp=0"

template_product_description_url = "https://wbx-content-v2.wbstatic.net/ru/{idx}.json"


class WildParser:
    def __init__(self):
        self._data = []

    async def _collect_from_page(self, session, page, query):
        data = []
        json_ = await _utils.get_products(query, page, session)
        if not json_:
            return []
        products = json_["data"]["products"]
        ids = tuple(map(lambda x: x['id'], products))

        print(f"page - {page}, for query - {query}")

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

    async def _collect_data_by_query(self, query: str) -> list:
        async with aiohttp.ClientSession(headers={
            "user-agent": UserAgent().random,
        }) as session:
            data = []
            page = 0
            while True:
                page += 1
                data_from_page = await self._collect_from_page(session, page, query)
                if not data_from_page:
                    break
                data += data_from_page

        return data

    async def _create_tasks(self, queries):
        tasks = []

        for el in queries:
            task = asyncio.create_task(self._collect_data_by_query(el))
            tasks.append(task)
        return await asyncio.gather(*tasks)

    def collect(self, *queries) -> list:
        """Collecting all products by all queries"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        return loop.run_until_complete(self._create_tasks(queries))



def _save_json(data, path: str) -> str:
    s = _(json.dumps(data, indent=4, ensure_ascii=False))
    with open(path, "w", encoding="cp1251") as f:
        f.write(s)
    return path


# async def _create_tasks(queries):
#     tasks = []
#
#     for el in queries:
#         task = asyncio.create_task(collect_and_save(el))
#         tasks.append(task)
#     return await asyncio.gather(*tasks)

if __name__ == '__main__':
    s_t = time.time()
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # res = loop.run_until_complete(_create_tasks(["iphone"]))
    res = WildParser().collect("iphone", "macbook")
    print(round(time.time() - s_t, 5))
    _save_json(res, "test_source/test.json")

