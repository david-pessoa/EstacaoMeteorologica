from django.shortcuts import render
from django.views import View
import requests
from datetime import datetime, time
from decouple import config

class IndexView(View):
    def get(self, request):
        API_KEY = config('API_KEY')
        local = 'Sao Paulo'
        dias = 6
        URL = f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={local}&days={dias}&aqi=no&alerts=yes'
        response = requests.get(URL)
        dados = response.json()

        agora = dados['current'] #Tempo agora
        proximos_dias = dados['forecast']['forecastday']

        ultima_atualizacao = agora['last_updated'].split(' ')[-1]
        umidade = agora['humidity']

        if umidade >= 60:
            tipo_umidade = 'Alta'

        elif umidade < 60 and umidade >= 30:
            tipo_umidade = 'Moderada'
        
        elif umidade < 30 and umidade >= 20:
            tipo_umidade = 'Baixa'
        
        else:
            tipo_umidade = 'Muito baixa'
        
        angulo_vento = agora['wind_degree'] - 45 # Faz correção (a imagem do ícone já é inclinada 45º)

        hora_atual = datetime.now().strftime('%H:%M')
        if hora_atual > '6:00' and hora_atual < '18:00':
            eh_dia = True
        else:
            eh_dia = False

        if agora['condition']['code'] == 1000 and eh_dia:
            icone_tempo = 'clear-day'
            texto_tempo = 'Céu limpo'
        
        elif agora['condition']['code'] == 1000 and not eh_dia:
            icone_tempo = 'clear-night'
            texto_tempo = 'Céu limpo'

        elif agora['condition']['code'] in [1003, 1006] and eh_dia:
            icone_tempo = 'overcast-day'
            texto_tempo = 'Parcialmente nublado'
        
        elif agora['condition']['code'] in [1003, 1006] and not eh_dia:
            icone_tempo = 'overcast-night'
            texto_tempo = 'Parcialmente nublado'
        
        elif agora['condition']['code'] == 1009:
            icone_tempo = 'clouy'
            texto_tempo = 'Nublado'
        
        elif agora['condition']['code'] in [1063, 1069, 1072] and eh_dia:
            icone_tempo = 'overcast-day-drizzle'
            texto_tempo = 'Chuva'
        
        elif agora['condition']['code'] in [1063, 1069, 1072] and not eh_dia:
            icone_tempo = 'overcast-night-drizzle'
            texto_tempo = 'Chuva'
        
        #TODO: Colocar mais imagens

        else:
            icone_tempo = 'outra coisa'
            texto_tempo = 'Tempo não configurado'
        

        context = {
            "lugar": local,
            "ultima_atualizacao": ultima_atualizacao,
            "icone_tempo": icone_tempo,
            "texto_tempo": texto_tempo,
            "ag": agora,
            "prox_dias": proximos_dias,
            "umidade": tipo_umidade,
            "angulo_vento": angulo_vento,
        }

        return render(request, 'index.html', context)
    
    def post(self, request):
        pass