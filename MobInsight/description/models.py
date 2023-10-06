from django.db import models

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=256)
    comment = models.TextField()
    price = models.IntegerField()
    performance = models.TextField()
    display = models.TextField()
    camera = models.TextField()
    battery = models.TextField()

    def __str__(self):
        return self.name
