# myapp/urls.py
from django.urls import path
from . import views
from django.contrib import admin
from .models import Student
from .models import Product

urlpatterns = [
    path('', views.home, name='contact'),
]

# myapp/admin.py


admin.site.register(Student)

from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "price", "rating")

