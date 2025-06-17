from django.contrib import admin
from .models import Agora, Hoje, Horario, ProximosDias

@admin.register(Agora)
class AdminAgora(admin.ModelAdmin):
    list_display = (
        'pk', 
        'hora_coleta',
        'temperatura', 
        'sensacao_termica', 
        'direcao_vento', 
        'velocidade_vento', 
        'umidade',
        'pressao',
        'cobertura_nuvem'
        )

@admin.register(Hoje)
class AdminHoje(admin.ModelAdmin):
    list_display = ('pk', 'dia', 'temp_max', 'temp_min')

@admin.register(Horario)
class AdminHorario(admin.ModelAdmin):
    list_display = ('pk', 'dia', 'horario', 'temperatura')

@admin.register(ProximosDias)
class AdminProximosDias(admin.ModelAdmin):
    list_display = ('pk', 'data', 'chance_chuva', 'cobertura_nuvem', 'temp_max', 'temp_min')