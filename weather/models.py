from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100, unique=True)

class ZipCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    zip_code = models.CharField(max_length=10)
