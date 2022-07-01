import time

import requests
import json


template_products_url = "https://search.wb.ru/exactmatch/ru/common/v4/" \
               "search?appType=1&curr=rub" \
               "&emp=0" \
               "$lang=ru&locale=ru&page={page}&pricemarginCoeff=1.0" \
               "&query={query}&reg=0&resultset=catalog&sort=popular&spp=0"

template_images_url = "https://images.wbstatic.net/c516x688/new/{collection}/{idx}.jpg"


def collect_data_from_page(query, page):
    response = requests.get(template_products_url.format(query=query, page=page))

    data = response.json()

    if not data:
        return []

    products = data["data"]["products"]

    print(f"get page - {page}, for query - {query}")

    d_page = []

    for product in products:
        idx = product["id"]
        image_url = _get_image_url(idx)
        name = product["name"]
        price = product["priceU"] // 100
        brand = product["brand"]
        d_page.append({
            "name": name,
            "image": image_url,
            "price": price,
            "brand": brand
        })

    return d_page


def collect_data(query):
    data = []
    page = 0

    while True:
        page += 1

        data_from_page = collect_data_from_page(query, page)

        if not data_from_page:
            break

        data += data_from_page

    normalized_query = "_".join(query.split(" "))
    filename = f"sync_wildberries_{normalized_query}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return filename


def _get_image_url(index: str) -> str:
    return template_images_url.format(collection=str(index)[:4] + "0000", idx=str(index) + "-1")


if __name__ == '__main__':
    t_s = time.time()

    queries = ["iphone", "робот пылесос"]
    for query in queries:
        file = collect_data(query)
        print(file)

    print(time.time() - t_s)
