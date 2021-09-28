import datetime

from table.models import Product
from table.src.pastebin import get_data


def insert_data():
    response = get_data()

    for row in response["data"]:
        q = Product(
            url=row["product_url"],
            consult_date=row["consult_date"],
            image=row["product_url__image"],
            store_url=row["store_url"],
            c=row["c"],
            created_at=row["product_url__created_at"],
        )
        q.save()
