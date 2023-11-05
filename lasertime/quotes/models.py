from django.db import models

class Material(models.Model):
    name = models.CharField(max_length=100)
    thickness = models.FloatField()
    price = models.FloatField()
    cutting_speed = models.FloatField()

    def __str__(self):
        return self.name
