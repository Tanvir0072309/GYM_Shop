# myapp/models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name
from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description1 = models.TextField()
    description2 = models.TextField()
    rating = models.FloatField(default=5.0)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
