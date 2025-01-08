import requests
import json


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
        r = requests.get(CatgirlDownloader.get_page_url(
            CatgirlDownloader.get_page(nsfw)),
                         timeout=15)
        return r.content

    @staticmethod
    def get_cat():
        return requests.get("https://cataas.com/cat", timeout=15).content
