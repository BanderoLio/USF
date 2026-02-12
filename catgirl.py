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
        try:
            if nsfw:
                res = requests.get("https://api.nekosapi.com/v4/images/"
                                "random?rating=explicit,borderline,suggestive&"
                                "tags=kemonomimi,girl&limit=1", timeout=15)
                res.raise_for_status()
                url = res.json()[0]['url']
            else:
                res = requests.get("https://api.nekosapi.com/v4/images/"
                                "random?rating=safe&suggestive&"
                                "tags=kemonomimi,girl&limit=1", timeout=15)
                res.raise_for_status()
                url = res.json()[0]['url']
                
            if url is None:
                return None
            
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            return r.content
        except Exception as e:
            print(f"Error in get_image: {e}")
            return None

    @staticmethod
    def get_cat():
        try:
            r = requests.get("https://cataas.com/cat", timeout=15)
            r.raise_for_status()
            return r.content
        except Exception as e:
            print(f"Error in get_cat: {e}")
            return None

    @staticmethod
    def get_furry():
        try:
            s = f'https://furbooru.org/api/v1/json/search/images' \
                f'?per_page=1&page={randint(1, 24000)}&q=safe,female,oc+only'
            r = requests.get(s, timeout=15)
            r.raise_for_status()
            page = json.loads(r.text)
            if not page.get('images') or len(page['images']) == 0:
                return None
            url = page['images'][0]['representations']['full']
            img_r = requests.get(url, timeout=15)
            img_r.raise_for_status()
            return img_r.content
        except Exception as e:
            print(f"Error in get_furry: {e}")
            return None
