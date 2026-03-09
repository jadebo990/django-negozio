from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prodotti/', views.prodotti, name='prodotti'),
    path('ordini/', views.ordini, name='ordini'),
    path('api/clienti/', views.getClienti, name='getClienti'),
    path('api/prodotti/', views.getProdotti, name='getProdotti'),

    path('api/ordini/<int:pk>/', views.detailOrdini, name='detailOrdini'),
    path('api/ordini/', views.postOrdine, name='postOrdine'),
]
