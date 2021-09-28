from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import ListView
from django.core import serializers
from django.db.models import Sum

import json
from datetime import datetime

from table.models import Product


def index(request):
    return render(request, "index.html")


class ProductView(ListView):

    model = Product

    def get_queryset(self):
        filter_text = (
            self.request.GET.get("filters")
            if self.request.GET.get("filters") != None
            else ""
        )

        total_products = (
            self.model.objects.filter(url__icontains=filter_text)
            .values("url", "created_at")
            .annotate(total_c=Sum("c"))
            .order_by("url")
        )

        date_products = (
            self.model.objects.filter(url__icontains=filter_text)
            .values("url", "consult_date", "c")
            .order_by("-consult_date")
        )

        products = []

        for product in total_products:

            products.append(
                {
                    "url": f"""<a href='{product['url']}'>{product['url']}</a>""",
                    "created_at": product["created_at"].strftime("%Y-%m-%d"),
                    "c": product["total_c"],
                }
            )

            for date in date_products:
                if date["url"] == product["url"]:
                    products[-1][date["consult_date"].strftime("%Y-%m-%d")] = date["c"]

        print(len(products))

        return products

    def get(self, request):
        if request.is_ajax():
            columns = []
            columns_name = ["Produto", "Data de inserção na loja", "Total de Vendas"]
            columns_date = []

            products = self.get_queryset()

            order_column = self.request.GET.get("column")
            order_dir = self.request.GET.get("dir")

            if order_column != None:
                for product in products:
                    if order_column not in product:
                        product[order_column] = 0

                products = sorted(
                    products,
                    key=lambda k: k[order_column],
                    reverse=True if order_dir == "desc" else False,
                )

            try:
                start = int(request.GET.get("start"))
                limit = int(request.GET.get("limit"))
            except:
                start = 0
                limit = len(products)

            list_products = []

            for i, val in enumerate(products[start : start + limit], start):
                for key, value in val.items():
                    if {"data": key} not in columns:
                        if key not in ("url", "created_at", "c"):
                            columns_date.append(key)
                        columns.append({"data": key})

                list_products.append(val)

            columns_date.sort(reverse=True)

            columns = sorted(columns, key=lambda k: k["data"], reverse=True)

            data = {
                "recordsTotal": len(products),
                "objects": list_products,
                "columnsName": columns_name,
                "columnsDateName": columns_date,
                "columns": columns,
            }

            return HttpResponse(json.dumps(data), "application/json")
        else:
            return redirect("/table/")
