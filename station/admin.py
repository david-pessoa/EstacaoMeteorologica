from django.contrib import admin
from .models import Cidade

@admin.register(Cidade)
class AdminCidade(admin.ModelAdmin):
    list_display = ('pk', 'nome', 'nomeAPI', 'regiao', 'pais', 'timezone')