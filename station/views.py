import pytz
from django.shortcuts import render
from django.views import View
from datetime import datetime
import requests
from decouple import config
from .models import Cidade

class IndexView(View):
    def get(self, request):
        
        #########################  REQUISIÇÃO DA API DO WEATHERAPI ####################
        API_KEY = config('API_KEY')
        local =  request.GET.get('local', 'São Paulo')
        dias = 7
        URL = f'http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={local}&days={dias}&aqi=no&alerts=yes&lang=pt'
        response = requests.get(URL)

        if response.status_code == 400:
            context = {"local": local}
            return render(request, 'local_inexistente.html', context)

        dados = response.json()
        agora = dados['current'] #Tempo agora
        
        previsao = dados['forecast']['forecastday'] #Previsão do tempo para hoje e próximos dias

        ultima_atualizacao_sem_tz = agora['last_updated'] #Obtém horário da última atualização
        ultima_atualizacao_sem_tz = datetime.strptime(ultima_atualizacao_sem_tz, "%Y-%m-%d %H:%M") #Transforma string em data
        
        timezone = dados["location"]["tz_id"] #Obtém fuso-horário da estação
        fuso_estacao = pytz.timezone(timezone)
        ultima_atualizacao_com_tz = fuso_estacao.localize(ultima_atualizacao_sem_tz) #Adiciona fuso-horário ao horário

        fuso_universal = pytz.timezone("UTC") #Converte para UTC
        ultima_atualizacao_UTC = ultima_atualizacao_com_tz.astimezone(fuso_universal)

        umidade = agora['humidity'] #Obtém humidade atual

        # Classifica umidade como Alta, Moderad, Baixa ou Muito Baixa
        if umidade >= 60:
            tipo_umidade = 'Alta'

        elif umidade < 60 and umidade >= 30:
            tipo_umidade = 'Moderada'
        
        elif umidade < 30 and umidade >= 20:
            tipo_umidade = 'Baixa'
        
        else:
            tipo_umidade = 'Muito baixa'
        
        angulo_vento = agora['wind_degree'] - 45 # Faz correção (a imagem do ícone já é inclinada 45º)

        def obter_icone_svg(code, is_day): #Obtém ícone SVG com base no código do tempo atual
            mapa = {
                1000: ['clear-day' if is_day else 'clear-night', 'Céu limpo'],
                1003: ['partly-cloudy-day' if is_day else 'partly-cloudy-night', 'Parcialmente nublado'],
                1006: ['cloudy', 'Nublado'],
                1009: ['overcast-day' if is_day else 'overcast-night', 'Encoberto'],
                1030: ['mist', 'Névoa'],
                1063: ['drizzle', 'Possibilidade de Garoa'],
                1066: ['snow', 'Neve'],
                1069: ['sleet', 'Possibilidade de Chuva com granizo'],
                1072: ['drizzle', 'Possibilidade de Garoa congelante'],
                1087: ['thunderstorms-day' if is_day else 'thunderstorms-night', 'Possibilidade de trovoadas'],
                1114: ['snow', 'Neve soprada'],
                1117: ['snow', 'Nevasca'],
                1135: ['fog-day' if is_day else 'fog-night', 'Nevoeiro'],
                1147: ['fog-day' if is_day else 'fog-night', 'Nevoeiro congelante'],
                1150: ['drizzle', 'Garoa fraca'],
                1153: ['drizzle', 'Garoa'],
                1168: ['drizzle', 'Garoa congelante'],
                1171: ['extreme-rain', 'Garoa congelante forte'],
                1180: ['rain', 'Chuva fraca e intermitente'],
                1183: ['rain', 'Chuva fraca'],
                1186: ['rain', 'Chuva'],
                1189: ['rain', 'Chuva'],
                1192: ['extreme-rain', 'Chuva forte intermitente'],
                1195: ['extreme-rain', 'Chuva forte'],
                1198: ['rain', 'Chuva congelante fraca'],
                1201: ['extreme-rain', 'Chuva congelante forte'],
                1204: ['sleet', 'Granizo leve'],
                1207: ['sleet', 'Granizo moderado ou forte'],
                1210: ['snow', 'Neve leve'],
                1213: ['snow', 'Neve'],
                1216: ['snow', 'Neve moderada'],
                1219: ['snow', 'Neve'],
                1222: ['snow', 'Neve pesada e esparsa'],
                1225: ['snow', 'Neve pesada'],
                1237: ['hail', 'Granizo'],
                1240: ['rain', 'Pancada de chuva leve'],
                1243: ['rain', 'Pancada de chuva moderada ou forte'],
                1246: ['extreme-rain', 'Pancada de chuva torrencial'],
                1249: ['sleet', 'Pancada de granizo leve'],
                1252: ['sleet', 'Pancada de granizo moderada ou forte'],
                1255: ['snow', 'Pancada de neve leve'],
                1258: ['snow', 'Pancada de neve moderada ou forte'],
                1261: ['hail', 'Pancada leve de granizo'],
                1264: ['hail', 'Pancada forte de granizo'],
                1273: ['thunderstorms-day-rain' if is_day else 'thunderstorms-night-rain', 'Chuva fraca com trovoadas'],
                1276: ['thunderstorms-day-extreme-rain' if is_day else 'thunderstorms-night-extreme-rain', 'Chuva forte com trovoadas'],
                1279: ['thunderstorms-day-snow' if is_day else 'thunderstorms-night-snow', 'Neve fraca com trovoadas'],
                1282: ['thunderstorms-day-extreme-snow' if is_day else 'thunderstorms-night-extreme-snow', 'Neve forte com trovoadas'],
            }
            return mapa.get(code, ['not-available', 'Condição não disponível'])

        lista_tempo = obter_icone_svg(agora['condition']['code'], agora['is_day'])
        
        dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        dia_index = datetime.now().weekday()
        dias_semana = dias_semana[dia_index + 1:] + dias_semana[:dia_index] #Obtém nomes dos 6 próximos dias da semana

        chances_chuva = [] # Obtém chances de chuva, ícones do tempo e máximas e mínimas de temperatura
        icones = [] # dos próximos 6 dias
        max_temps = []
        min_temps = []

        for i in range(1, 7): #Popula as listas com as informações do tempo dos próximos dias
            chances_chuva.append(previsao[i]['day']["daily_chance_of_rain"])

            codigo_tempo = previsao[i]['day']["condition"]['code']
            icone_tempo = obter_icone_svg(codigo_tempo, True)
            icones.append(icone_tempo[0])

            max_temps.append(previsao[i]['day']["maxtemp_c"])
            min_temps.append(previsao[i]['day']["mintemp_c"])

        context = {
            "lugar": local,
            "ultima_atualizacao": ultima_atualizacao_UTC,
            "icone_tempo": lista_tempo[0],
            "texto_tempo": lista_tempo[1],
            "ag": agora,
            "previsao_hoje": previsao[0],
            "umidade": tipo_umidade,
            "angulo_vento": angulo_vento,
            "previsao": zip(dias_semana, chances_chuva, icones, max_temps, min_temps),
            "cidades": Cidade.objects.all(),
        }
        return render(request, 'index.html', context)
    
    def post(self, request):
        pass