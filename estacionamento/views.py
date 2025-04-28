from django.shortcuts import render, redirect
from .models import CarroEstacionado
from django.utils import timezone
import random

def home(request):
    return render(request, 'estacionamento/home.html')

def estacionar_carro(request):
    if request.method == 'POST':
        placa = request.POST['placa']
        nome = request.POST['nome']
        contato = request.POST['contato']
        codigo = str(random.randint(100000, 999999))  # gerar código de verificação
        CarroEstacionado.objects.create(
            placa=placa,
            nome_motorista=nome,
            numero_contato=contato,
            codigo_verificacao=codigo
        )
        # Aqui futuramente você poderá enviar SMS com o código
        return redirect('home')
    return render(request, 'estacionamento/formulario_estacionar.html')

def retirar_carro(request):
    if request.method == 'POST':
        placa = request.POST['placa']
        codigo = request.POST['codigo']
        try:
            carro = CarroEstacionado.objects.get(placa=placa, codigo_verificacao=codigo)
            hora_saida = timezone.now()
            tempo_estacionado = hora_saida - carro.hora_estacionado
            minutos = tempo_estacionado.total_seconds() / 60
            valor_a_pagar = round(minutos * 0.1, 2)  # exemplo: R$0,10 por minuto
            return render(request, 'estacionamento/resultado.html', {
                'placa': carro.placa,
                'valor': valor_a_pagar
            })
        except CarroEstacionado.DoesNotExist:
            return render(request, 'estacionamento/formulario_retirar.html', {'erro': 'Placa ou código inválido.'})

    return render(request, 'estacionamento/formulario_retirar.html')
