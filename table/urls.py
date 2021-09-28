from django.urls import path, include

from .views import index, ProductView


urlpatterns = [
    path("", index, name="index"),
    path("products/", ProductView.as_view(), name="products"),
]
