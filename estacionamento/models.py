from django.db import models

class CarroEstacionado(models.Model):
    placa = models.CharField(max_length=10)
    nome_motorista = models.CharField(max_length=100)
    numero_contato = models.CharField(max_length=15)
    hora_estacionado = models.DateTimeField(auto_now_add=True)
    codigo_verificacao = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.placa
