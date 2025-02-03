from django.db import models

class Gasto(models.Model):
    data = models.DateField()  # Data do gasto
    descricao = models.CharField(max_length=255)  # Descrição do gasto
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor do gasto

    def __str__(self):
        return f"{self.data} - {self.descricao} - {self.valor}"
