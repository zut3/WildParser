import asyncio
import aiohttp
import time
import json
import _utils


async def collect_from_page(session, page, query):
    template_products_url = "https://search.wb.ru/exactmatch/ru/common/v4/" \
                            "search?appType=1&curr=rub" \
                            "&emp=0" \
                            "$lang=ru&locale=ru&page={page}&pricemarginCoeff=1.0" \
                            "&query={query}&reg=0&resultset=catalog&sort=popular&spp=0"

    data = []
    async with session.get(template_products_url.format(query=query, page=page)) as response:

        print(f"get page - {page}, for query - {query}")
        text = await response.read()
        json_ = json.loads(text)
        products = json_["data"]["products"]

        for product in products:
            idx = product["id"]
            image_url = _utils.get_image_url(idx)
            name = product["name"]
            price = product["priceU"] // 100
            brand = product["brand"]
            data.append({
                "name": name,
                "image": image_url,
                "price": price,
                "brand": brand
            })
    return data


async def collect_data_by_query(query):

    async with aiohttp.ClientSession() as session:
        data = []
        page = 0
        while True:
            page += 1
            data_from_page = await collect_from_page(session, page, query)
            if not data_from_page:
                break
            data += data_from_page

    with open(f"data/wildberries_{query}.json", "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return f"data/wildberries_{query}.json"


async def create_tasks():
    li = ["iphone", "робот пылесос"]
    tasks = []

    for el in li:
        task = asyncio.create_task(collect_data_by_query(el))
        tasks.append(task)
    return await asyncio.gather(*tasks)

if __name__ == '__main__':
    s_t = time.time()
    asyncio.get_event_loop().run_until_complete(create_tasks())
    print(time.time() - s_t)
