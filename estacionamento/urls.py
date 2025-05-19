from django.urls import path
from . import views

app_name = 'estacionamento'

urlpatterns = [
    path('', views.lista_veiculos, name='lista_veiculos'),
    path('adicionar/', views.adicionar_veiculo, name='adicionar_veiculo'),
    path('saida/<int:veiculo_id>/', views.registrar_saida, name='registrar_saida'),
    path('veiculos/', views.lista_veiculos, name='lista_veiculos'),
    path('historico/', views.historico_veiculos, name='historico'),
    path('historico/', views.historico_veiculos, name='historico'),
]
