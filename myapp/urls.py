from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from myapp import views

urlpatterns = [
    path('', views.home),
    path("admin-panel/", views.admin_panel_page),

    path('product/<slug:slug>/', views.product_detail, name='product_detail'), 
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]
