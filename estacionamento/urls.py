from django.urls import path
from . import views

app_name = 'estacionamento'

urlpatterns = [
    path('', views.adicionar_veiculo, name='adicionar_veiculo'), 
    path('lista/', views.lista_veiculos, name='lista_veiculos'), 
    path('pagamento/<int:veiculo_id>/', views.tela_pagamento, name='tela_pagamento'), 
    path('adicionar/', views.adicionar_veiculo, name='adicionar_veiculo'),
    path('saida/<int:veiculo_id>/', views.registrar_saida, name='registrar_saida'),
    path('pagamento-concluido/<int:veiculo_id>/', views.pagamento_concluido, name='pagamento_concluido'),
    path('historico/', views.historico_veiculos, name='historico'),
]