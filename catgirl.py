import requests
import json

from random import randint


class CatgirlDownloader:
    __endpoint = "https://nekos.moe/api/v1/random/image?nsfw="

    @staticmethod
    def get_page(nsfw=False):
        try:
            res = requests.get(f'{CatgirlDownloader.__endpoint}'
                               f'{str(nsfw).lower()}', timeout=15)
            return res.text if res.status_code == 200 else None
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_page_url(response):
        data = json.loads(response)
        return "https://nekos.moe/image/" + data["images"][0]['id']

    @staticmethod
    def get_image(nsfw=False):
        url = None
        if nsfw and randint(0, 100) <= 50:
            res = requests.get("https://api.nekosapi.com/v4/images/"
                               "random?rating=suggestive,borderline&"
                               "tags=kemonomimi,girl&limit=1", timeout=15)
            res.raise_for_status()
            url = res.json()[0]['url']
        else:
            url = CatgirlDownloader.get_page_url(
                CatgirlDownloader.get_page(nsfw)
            )
        try:
            r = requests.get(url,
                             timeout=15)
            return r.content
        except Exception:
            ...

    @staticmethod
    def get_cat():
        try:
            return requests.get("https://cataas.com/cat", timeout=15).content
        except Exception:
            ...

    @staticmethod
    def get_furry():
        s = f'https://furbooru.org/api/v1/json/search/images' \
            f'?per_page=1&page={randint(1, 24000)}&q=safe,female,oc+only'
        r = requests.get(s, timeout=15)
        page = json.loads(r.text)
        url = page['images'][0]['representations']['full']
        try:
            return requests.get(url, timeout=15).content
        except Exception:
            ...
