from django.db import models


class Photo(models.Model):
    group = models.CharField(verbose_name="Group")
    photo_id = models.CharField(max_length=1000, verbose_name="Photo id")
