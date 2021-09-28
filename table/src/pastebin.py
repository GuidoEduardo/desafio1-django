import requests
import datetime

from django.utils import timezone

from core.settings import DATA_URL


def get_data() -> dict:
    url = DATA_URL

    r = requests.get(url)
    content = eval("{ 'data': " + r.text.replace("<UTC>", "timezone.utc") + " }")

    return content
