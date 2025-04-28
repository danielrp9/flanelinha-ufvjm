from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('estacionar/', views.estacionar_carro, name='estacionar_carro'),
    path('retirar/', views.retirar_carro, name='retirar_carro'),
]
