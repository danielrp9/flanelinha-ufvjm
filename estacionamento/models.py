from django.db import models
from django.utils import timezone

class Veiculo(models.Model):
    placa = models.CharField(max_length=7, unique=True)
    modelo = models.CharField(max_length=50)
    cor    = models.CharField(max_length=20)
    avarias = models.TextField(blank=True)           # ← NOVO
    horario_entrada = models.DateTimeField(default=timezone.now)
    horario_saida   = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.modelo} - {self.placa}"
