from django.db import models

class Agora(models.Model):
    hora_coleta = models.TimeField('Horário da Coleta')
    temperatura = models.DecimalField('Temperatura', max_digits=3, decimal_places=1)
    sensacao_termica = models.DecimalField('Sensação Térmica', max_digits=3, decimal_places=1)
    direcao_vento = models.CharField('Direção do Vento', max_length=3)
    velocidade_vento = models.DecimalField('Velocidade do Vento', max_digits=4, decimal_places=1)
    umidade = models.DecimalField('Umidade do Ar', max_digits=3, decimal_places=0)
    pressao = models.DecimalField('Pressão Atmosférica', max_digits=5, decimal_places=1)
    cobertura_nuvem = models.DecimalField('Cobertura de Nuvem', max_digits=3, decimal_places=0)

    def __str__(self):
        return f"Agora: {self.hora_coleta}"

    class Meta:
        verbose_name = 'Agora'
        verbose_name_plural = 'Agora'

class Hoje(models.Model):
    dia = models.DateField('Dia de Hoje')
    temp_max = models.DecimalField('Temperatura Máxima', max_digits=3, decimal_places=1)
    temp_min = models.DecimalField('Temperatura Mínima', max_digits=3, decimal_places=1)

    def __str__(self):
        return f"Dia de Hoje {self.dia}"

    class Meta:
        verbose_name = 'Hoje'
        verbose_name_plural = 'Hoje'


class Horario(models.Model):
    dia = models.ForeignKey(Hoje, on_delete=models.CASCADE)
    horario = models.TimeField('Horário')
    temperatura = models.DecimalField('Temperatura', max_digits=3, decimal_places=1)

    def __str__(self):
        return f"Horário {self.horario}"

    class Meta:
        verbose_name = 'Horário'
        verbose_name_plural = 'Horários'

class ProximosDias(models.Model):
    data = models.DateField('Dia')
    chance_chuva = models.DecimalField('Chance de chuva', max_digits=3, decimal_places=1)
    cobertura_nuvem = models.DecimalField('Cobertura de Nuvem', max_digits=3, decimal_places=0)
    temp_max = models.DecimalField('Temperatura Máxima', max_digits=3, decimal_places=1)
    temp_min = models.DecimalField('Temperatura Mínima', max_digits=3, decimal_places=1)

    def __str__(self):
        return f"Dia {self.data}"

    class Meta:
        verbose_name = 'Próximo dia'
        verbose_name_plural = 'Próximos dias'
