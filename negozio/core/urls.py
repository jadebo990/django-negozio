from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prodotti/', views.prodotti, name='prodotti'),
    path('ordini/', views.ordini, name='ordini'),
    path('api/clienti/', views.getClienti, name='getClienti'),
]
