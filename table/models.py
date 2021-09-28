from django.db import models


class Product(models.Model):
    url = models.CharField(max_length=200)
    consult_date = models.DateTimeField()
    image = models.CharField(max_length=200)
    store_url = models.CharField(max_length=200)
    c = models.IntegerField()
    created_at = models.DateTimeField()
