from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("table/", include("table.urls")),
    path("admin/", admin.site.urls),
]
