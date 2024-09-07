from django.contrib.auth.models import User
from django.db import models

class Address(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    street = models.CharField(max_length=100)

    def __str__(self):
        return self.name