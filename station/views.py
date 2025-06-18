from django.shortcuts import render
from django.views import View
from .models import Agora, Hoje, Horario, ProximosDias

class IndexView(View):
    def get(self, request):
        agora = Agora.objects.get(pk=1)
        hoje = Hoje.objects.get(pk=1)
        horarios = Horario.objects.all()
        prox_dias =  ProximosDias.objects.all()

        context = {
            "lugar": "Sao Paulo",
            "ag": agora,
            "hoje": hoje,
            "horarios": horarios,
            "prox_dias": prox_dias
        }

        return render(request, 'index.html', context)
    
    def post(self, request):
        pass