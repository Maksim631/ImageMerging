from django.db import models


class Photo(models.Model):
    group = models.CharField(max_length=100, verbose_name="Group")
    photo_id = models.CharField(max_length=1000, verbose_name="Photo id")
