from django.db import models

class Cidade(models.Model):
    nome = models.CharField('Cidade', max_length=100)
    nomeAPI = models.CharField('Nome da cidade na API', max_length=100)
    regiao = models.CharField('Região', max_length=100)
    pais = models.CharField('País', max_length=100)
    timezone = models.CharField('Fuso Horário', max_length=100)

    def __str__(self):
        return self.nome