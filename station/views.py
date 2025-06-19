from django.shortcuts import render
from django.views import View
from .models import Agora, Hoje, Horario, ProximosDias
from datetime import datetime, time

class IndexView(View):
    def get(self, request):
        agora = Agora.objects.get(pk=1)
        hoje = Hoje.objects.get(pk=1)
        horarios = Horario.objects.all()
        prox_dias =  ProximosDias.objects.all()

        hora_atual = datetime.now().strftime('%H:%M')
        if hora_atual > '6:00' and hora_atual < '18:00':
            eh_dia = True
        else:
            eh_dia = False

        if agora.codigo_tempo == 1000 and eh_dia:
            icone_tempo = 'clear-day'
            texto_tempo = 'Céu limpo'
        
        elif agora.codigo_tempo == 1000 and not eh_dia:
            icone_tempo = 'clear-night'
            texto_tempo = 'Céu limpo'

        elif agora.codigo_tempo in [1003, 1006] and eh_dia:
            icone_tempo = 'overcast-day'
            texto_tempo = 'Parcialmente nublado'
        
        elif agora.codigo_tempo in [1003, 1006] and not eh_dia:
            icone_tempo = 'overcast-night'
            texto_tempo = 'Parcialmente nublado'
        
        elif agora.codigo_tempo == 1009:
            icone_tempo = 'clouy'
            texto_tempo = 'Nublado'
        
        elif agora.codigo_tempo in [1063, 1069, 1072] and eh_dia:
            icone_tempo = 'overcast-day-drizzle'
            texto_tempo = 'Chuva'
        
        elif agora.codigo_tempo in [1063, 1069, 1072] and not eh_dia:
            icone_tempo = 'overcast-night-drizzle'
            texto_tempo = 'Chuva'
        
        #TODO: Colocar mais imagens

        else:
            icone_tempo = 'outra coisa'
            texto_tempo = 'Tempo não configurado'
        


        context = {
            "lugar": "Sao Paulo",
            "icone_tempo": icone_tempo,
            "texto_tempo": texto_tempo,
            "ag": agora,
            "hoje": hoje,
            "horarios": horarios,
            "prox_dias": prox_dias
        }

        return render(request, 'index.html', context)
    
    def post(self, request):
        pass