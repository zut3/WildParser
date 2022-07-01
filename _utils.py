from functools import lru_cache


@lru_cache
def get_image_url(index: str) -> str:
    template_images_url = "https://images.wbstatic.net/c516x688/new/{collection}/{idx}.jpg"
    return template_images_url.format(collection=str(index)[:4] + "0000", idx=str(index) + "-1")
