from django.db import models


class Pneumonia(models.Model):
    image=models.ImageField(upload_to='images')
    result=models.FloatField()