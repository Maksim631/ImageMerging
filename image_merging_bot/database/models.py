from enum import Enum

from django.db import models


class Photo(models.Model):
    user_id = models.CharField(max_length=100, verbose_name="User id")
    photo_id = models.CharField(max_length=1000, verbose_name="Photo id")


class Way(models.Model):
    user_id = models.CharField(max_length=100, verbose_name="User id")
    way = models.CharField(max_length=10, verbose_name="Way")


Ways = {
    "DEFAULT": "default",
    "FOURIER": "fourier",
    "FEATURE": "feature"
}
