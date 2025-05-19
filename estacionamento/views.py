from django.shortcuts import render, redirect, get_object_or_404
from .models import Veiculo
from django.utils import timezone
from .forms import VeiculoForm

def lista_veiculos(request):
    veiculos = Veiculo.objects.all()
    return render(request, 'estacionamento/lista.html', {'veiculos': veiculos})

def adicionar_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('estacionamento:lista_veiculos')
    else:
        form = VeiculoForm()
    return render(request, 'estacionamento/adicionar.html', {'form': form})

def registrar_saida(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    veiculo.horario_saida = timezone.now()
    veiculo.save()
    return redirect('estacionamento:lista_veiculos')

def lista_veiculos(request):
    veiculos_ativos = Veiculo.objects.filter(horario_saida__isnull=True).order_by('-horario_entrada')
    return render(request, 'estacionamento/lista.html', {'veiculos_ativos': veiculos_ativos})

def historico_veiculos(request):
    veiculos = Veiculo.objects.all().order_by('-horario_entrada')
    return render(request, 'estacionamento/historico.html', {'veiculos': veiculos})

def historico_veiculos(request):
    veiculos = Veiculo.objects.all().order_by('-horario_entrada')
    return render(request, 'estacionamento/historico.html', {'veiculos': veiculos})