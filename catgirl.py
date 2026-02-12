import logging
import requests
import json
from random import randint


class CatgirlDownloader:

    @staticmethod
    def get_image_url(nsfw=False):
        """Возвращает URL изображения кошкодевочки (не скачивая его)."""
        try:
            if nsfw:
                res = requests.get(
                    "https://api.nekosapi.com/v4/images/"
                    "random?rating=explicit,borderline,suggestive&"
                    "tags=kemonomimi,girl&limit=1", timeout=10)
            else:
                res = requests.get(
                    "https://api.nekosapi.com/v4/images/"
                    "random?rating=safe&suggestive&"
                    "tags=kemonomimi,girl&limit=1", timeout=10)
            res.raise_for_status()
            url = res.json()[0]['url']
            if url:
                return url
            return None
        except Exception as e:
            logging.error(f"Error in get_image_url: {e}")
            return None

    @staticmethod
    def get_cat_url():
        """Возвращает URL случайного кота (не скачивая его)."""
        # cataas.com отдаёт случайного кота по этому URL.
        # Рандомный параметр предотвращает кеширование URL в Telegram.
        return f"https://cataas.com/cat?_t={randint(0, 999_999_999)}"

    @staticmethod
    def get_furry_url():
        """Возвращает URL фурри-изображения (не скачивая его)."""
        try:
            s = (f'https://furbooru.org/api/v1/json/search/images'
                 f'?per_page=1&page={randint(1, 24000)}&q=safe,female,oc+only')
            r = requests.get(s, timeout=10)
            r.raise_for_status()
            page = r.json()
            if not page.get('images') or len(page['images']) == 0:
                return None
            return page['images'][0]['representations']['full']
        except Exception as e:
            logging.error(f"Error in get_furry_url: {e}")
            return None
