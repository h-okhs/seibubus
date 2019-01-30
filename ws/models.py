from django.db import models


class BusStatus(models.Model):
    line = models.TextField()
    departureAt = models.TextField()
