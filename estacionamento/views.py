import stripe
from django.conf import settings 
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Veiculo
from django.utils import timezone
from .forms import VeiculoForm

stripe.api_key = settings.STRIPE_SECRET_KEY

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

def calcular_valor(horario_entrada):
    # Valor fictício: R$ 5,00 por hora
    tempo_estacionado = timezone.now() - horario_entrada
    horas = tempo_estacionado.total_seconds() / 3600
    return round(max(1, horas) * 5, 2)  # Mínimo de 1 hora

def tela_pagamento(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
    
    if request.method == 'POST':
        # Processar pagamento com Stripe
        try:
            valor_centavos = int(float(request.POST.get('valor_total')) * 100)
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'brl',
                        'product_data': {
                            'name': f'Saída do Veículo - {veiculo.placa}',
                        },
                        'unit_amount': valor_centavos,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('estacionamento:registrar_saida', args=[veiculo_id])
                ) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri('/'),
            )

            return redirect(checkout_session.url)
        except Exception as e:
            return render(request, 'estacionamento/erro_pagamento.html', {'erro': str(e)})
    
    valor_total = calcular_valor(veiculo.horario_entrada)
    horas_estacionado = (timezone.now() - veiculo.horario_entrada).total_seconds() / 3600
    
    context = {
        'veiculo': veiculo,
        'valor_total': valor_total,
        'horas_estacionado': round(horas_estacionado, 2),
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'estacionamento/pagamento.html', context)

def registrar_saida(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, pk=veiculo_id)
    session_id = request.GET.get('session_id')
    
    try:
        # Verificar o pagamento no Stripe
        if session_id:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                veiculo.horario_saida = timezone.now()
                veiculo.save()
                
                context = {
                    'veiculo': veiculo,
                    'valor_pago': session.amount_total / 100,  # Convertendo de centavos para reais
                    'horas_estacionado': round((veiculo.horario_saida - veiculo.horario_entrada).total_seconds() / 3600, 2),
                    'data_saida': veiculo.horario_saida,
                }
                return render(request, 'estacionamento/confirmacao_saida.html', context)
    
    except Exception as e:
        # Log do erro (opcional)
        print(f"Erro ao verificar pagamento: {str(e)}")
    
    return redirect('estacionamento:lista_veiculos')

def confirmacao_saida(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    data_saida = timezone.now()
    horas_estacionado = calcular_horas(veiculo.horario_entrada, data_saida)
    valor_pago = calcular_valor(horas_estacionado)

    # Atualiza o veículo como "saiu"
    veiculo.horario_saida = data_saida
    veiculo.save()

    context = {
        'veiculo': veiculo,
        'data_saida': data_saida,
        'horas_estacionado': horas_estacionado,
        'valor_pago': valor_pago,
    }
    return render(request, 'estacionamento/confirmacao_saida.html', context)
